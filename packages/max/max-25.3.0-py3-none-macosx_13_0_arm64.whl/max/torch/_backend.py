# ===----------------------------------------------------------------------=== #
#
# This file is Modular Inc proprietary.
#
# ===----------------------------------------------------------------------=== #

import os
import pickle
import re
import tempfile
import weakref
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import (
    Any,
    Optional,
    Union,
    cast,
)

import max._torch_mlir.fx as fx
from max._torch_mlir import add_jit_function  # type: ignore
from max._torch_mlir.extras.fx_decomp_util import get_decomposition_table
from max._torch_mlir.extras.fx_importer import WEIGHTS_REGISTRY_ATTR, ExportMeta
from max._torch_mlir.torch_api_compat import (
    dynamo_timed_wrapper,
    maybe_disable_fake_tensor_mode,
)
from max.torch._graph_cache import ModularCompiledFxGraph, ModularFxGraphCache
from max.torch._utils import clone, compare

import torch  # type: ignore
import torch.fx  # type: ignore

# LazyGraphModule is not supported by `torch.jit.script`,
# so disable globally to avoid the following type of error:
# ```
# E       RuntimeError:
# E       method cannot be used as a value:
# ```
import torch.fx._lazy_graph_module as _lazy_graph_module  # type: ignore
from torch._inductor.codecache import (  # type: ignore
    BypassFxGraphCache,
    compiled_fx_graph_hash,
)
from torch._inductor.compile_fx import get_input_idxs_to_check  # type: ignore
from torch._inductor.fx_passes.post_grad import view_to_reshape  # type: ignore
from torch._library.custom_ops import CustomOpDef  # type: ignore
from torch._subclasses.fake_tensor import (  # type: ignore
    FakeTensor,
    FakeTensorMode,
    extract_tensor_metadata,
)
from torch.fx.passes.fake_tensor_prop import FakeTensorProp  # type: ignore

global _lazy_graph_module
_lazy_graph_module._force_skip_lazy_graph_module_flag = True

from functorch.compile import make_boxed_func  # type: ignore
from max import engine
from max.driver import Device, DLPackArray
from max.dtype import DType, torch_to_max_type

from torch._dynamo.backends.common import (  # type: ignore
    AotAutograd,
    aot_autograd,
)
from torch._functorch.aot_autograd import (  # type: ignore
    MutationType,
    make_boxed_compiler,
)
from torch._functorch.compile_utils import fx_graph_cse  # type: ignore
from torch._inductor.fx_passes.post_grad import remove_noop_ops


def max_type_of(object: Any) -> DType:
    """Attempts to convert any Python type to a MAX dtype.DType.

    Args:
        object (Any): Any python type (currently supported: torch.Tensor, float,
            int, bool).

    Returns:
        dtype.DType: The corresponding dtype.DType.

    Raises:
        ValueError: If the dtype is not supported.
    """
    if isinstance(object, torch.Tensor) or isinstance(object, FakeTensor):
        return torch_to_max_type(object.dtype)
    if isinstance(object, float):
        return DType.float64
    if isinstance(object, int):
        return DType.int64
    if isinstance(object, bool):
        return DType.bool
    raise ValueError(f"{type(object)} currently not supported")


def to_modular_torch_load_spec(
    object: Any, dynamic: bool = False, use_devices: bool = False
) -> engine.TorchInputSpec:
    """
    Convert spec of given object to a Max engine.TorchInputSpec.

    Args:
        object: Object whose spec needs to be converted.
        dynamic: A flag specifying whether we should use static shapes of the
            input tensor as spec, or if we should consider all dims dynamic. In
            the latter case we still use the rank and dtype of the input
            tensor. Symbolic dimensions in FakeTensors will also be represented
            as dynamic dims in the input spec.
        use_devices: A flag to specify whether existing device annotations on
            tensors should be used for the input spec.

    Returns:
        engine.TorchInputSpec: The corresponding engine.TorchInputSpec.
    """
    if isinstance(object, torch.Tensor) or isinstance(object, FakeTensor):
        if dynamic:
            shape_spec = [None for i in range(len(object.shape))]
        else:
            shape_spec = [
                None if isinstance(dim, torch.SymInt) else dim
                for dim in object.shape
            ]
        return engine.TorchInputSpec(
            shape_spec,
            torch_to_max_type(object.dtype),
            str(object.device) if use_devices else "",
        )
    if isinstance(object, (list, tuple)):
        if len(object):
            dtype = max_type_of(object[0])
        else:
            dtype = DType.si64  # type: ignore
        return engine.TorchInputSpec([len(object)], dtype)
    if isinstance(object, (float, int, bool)):
        return engine.TorchInputSpec([], max_type_of(object))
    return engine.TorchInputSpec([], DType._unknown)


# ===----------------------------------------------------------------------=== #
# torch.compile support
# ===----------------------------------------------------------------------=== #


def construct_input_specs(sample_inputs: list[Any]):
    # TODO: We should be using symbolic shapes instead of static shapes of the sample inputs
    return [
        to_modular_torch_load_spec(input, dynamic=False)
        if isinstance(input, torch.Tensor)
        else engine.TorchInputSpec([], DType.int64)
        for input in sample_inputs
    ]


def get_input_specs_str(input_specs: list[engine.TorchInputSpec]):
    spec_strs = [
        "x".join(
            [str(dim) if dim is not None else "?" for dim in spec.shape]  # type: ignore
            + [spec.dtype._mlir]
        )
        for spec in input_specs
    ]
    return " ".join(f"--compile-specs={spec_str}" for spec_str in spec_strs)


def get_scalar_outputs_positions(graph) -> list[bool]:
    """
    Returns a list of a bool values indicating whether the corresponding graph
    output is scalar or not.
    """
    # Find output values of the TS graph
    graph_outputs = None

    # Often the graph returns a single tuple value - in that case we should
    # consider the value in that tuple as graph outputs.
    tuple_construct = list(graph.outputs())[0].node()
    if str(tuple_construct.kind()) != "prim::TupleConstruct":
        graph_outputs = graph.outputs()
    else:
        graph_outputs = tuple_construct.inputs()

    is_output_scalar = [str(t.type()) != "Tensor" for t in graph_outputs]
    return is_output_scalar


def _create_artifact_dir() -> Optional[Path]:
    """Create and return a temporary directory to dump test files into.

    Returns:
        None if test files should not be saved, or a directory path otherwise.
    """
    keep_tmpfile = os.getenv("MODULAR_PYTORCH_KEEP_TESTFILES", "False")
    if keep_tmpfile == "True":
        return Path(tempfile.mkdtemp())
    if keep_tmpfile == "False":
        return None

    Path(keep_tmpfile).mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(dir=Path(keep_tmpfile)))


def _create_symint_map(
    example_inputs: list[Union[torch.SymInt, FakeTensor]],
) -> dict[str, int]:
    """Create a map from SymInt instances to concrete integer dimensions.

    A unique integer value (within the signature) is used for `SymInt` values
    that don't have a hint.
    """

    # First we iterate through all the dimensions to populate a map with SymInt
    # names. We also keep track of all integer dimensions we've seen.
    existing_dim_values: set[int] = set()
    symint_map: dict[str, Optional[int]] = {}

    def record_dim(d: Union[torch.SymInt, int]):
        if isinstance(d, int):
            # We remember simple integers so we can avoid reusing them later.
            existing_dim_values.add(d)
        elif d.node.has_hint():
            existing = symint_map.get(str(d))
            new = d.node.hint
            if existing is None:
                # If no concrete value exists for this symint, we record it.
                symint_map[str(d)] = new
                existing_dim_values.add(new)
            else:
                # Otherwise, we just check that the new hint is not conflicting.
                assert existing == new
        else:
            # If no hint is available, we will assign a value later.
            symint_map.setdefault(str(d), None)

    for t in example_inputs:
        if isinstance(t, torch.SymInt):
            record_dim(t)
        elif isinstance(t, FakeTensor):
            for d in t.shape:
                record_dim(d)
        else:
            raise Exception(
                f"unknown example input type: {type(t)} expected {FakeTensor}"
            )

    # We create a generator that always yields a minimal unique integer
    # dimension value (and will consume the known dimension values). This will
    # keep the generated dimensions small, but guarantee that different
    # hint-less dimensions are mapped to different concrete values, and never be
    # equal to any other dimension.
    def unique_dim_value_generator() -> Iterator[int]:
        # 0 and 1 are special values, so we start the generation with 2.
        candidate = 2
        while True:
            # This is not the most efficient solution, but it's very simple.
            if candidate not in existing_dim_values:
                yield candidate
            candidate += 1

    # Update all hint-less SymInt entries in the map.
    unique_dim_value = unique_dim_value_generator()
    for dim_name, dim_value in symint_map.items():
        if dim_value is None:
            dim_value = next(unique_dim_value)
            print(f"SymInt '{dim_name}' has no size hint, using {dim_value}")
            symint_map[dim_name] = dim_value

    # `symint_map` only has integer values now, but make the type checker happy.
    return cast(dict[str, int], symint_map)


def _concretize_example_inputs(
    example_inputs: list[Union[torch.SymInt, FakeTensor]],
) -> list[Union[int, torch.Tensor]]:
    """Map the given example input signature to concrete integers and tensors.

    A unique integer value (within the signature) is used for `SymInt` values
    that don't have a hint.
    """

    # We create a map from all SymInts in the signature to concrete values, and
    # apply it. Dimensions that are already concrete integers are left as is.
    symint_map = _create_symint_map(example_inputs)

    def map_dim(d: Union[torch.SymInt, int]) -> int:
        if isinstance(d, torch.SymInt):
            v = symint_map[str(d)]
            assert isinstance(v, int)
            return v
        return d

    def map_input(t):
        if isinstance(t, torch.SymInt):
            return map_dim(t)
        if isinstance(t, FakeTensor):
            return torch.zeros(
                size=tuple(map_dim(d) for d in t.shape),
                dtype=t.dtype,
                device=t.device,
            )
        return t

    return [map_input(t) for t in example_inputs]


def _save_fx_graph_module(model: torch.fx.GraphModule, dirpath: Path):
    """Pickle the given FX graph to a new file in the given directory."""
    graph_filename = dirpath / "graph.fx"
    with open(graph_filename, "wb") as f:
        pickle.dump(model, f)
    print(f"Saved FX graph in: {graph_filename}")


def _save_input_specs(input_specs: list[Any], dirpath: Path):
    """Pickle the given input specs to a new file in the given directory."""
    specs_str = get_input_specs_str(input_specs)
    with open(dirpath / "input_specs.txt", "w") as f:
        f.write(specs_str)
    print(f"Input specs: {specs_str}")


def _save_example_inputs(
    example_inputs: list[Union[torch.SymInt, FakeTensor]], dirpath: Path
):
    """Save example input tensors derived from the given symbolic inputs.

    A new file will be created in the given directory with the pickled Tensors.
    """

    # We can't directly serialize SymInts and FakeTensors, so concretize them.
    inputs_to_pickle = _concretize_example_inputs(example_inputs)
    file_path = dirpath / "inputs.pkl"
    with open(file_path, "wb") as f:
        torch.save(inputs_to_pickle, f)
    print(f"Saved example inputs to: {file_path}")


@dynamo_timed_wrapper(phase_name="compile_mlir_module")
def compile_mlir_module(
    inference_session: engine.InferenceSession,
    gm: torch.fx.GraphModule,
    example_inputs: list[Union[torch.SymInt, FakeTensor]],
    input_specs: list[Any],
    weights_registry: Optional[dict[str, DLPackArray]] = None,
    export_meta: ExportMeta = None,  # type: ignore
    *,
    options: dict,
) -> tuple[fx.ir.Module, Any, list[bool]]:  # type: ignore
    """Compile the FX graph module and return the imported MLIR module and
        model handle.

    Args:
        inference_session (engine.InferenceSession): Modular engine.InferenceSession.
        gm: (torch.fx.GraphModule): The torch FX graph module to import.
        example_inputs (List[Union[torch.SymInt, FakeTensor]]): A list of sample inputs (symbolic and fake types).
        weights_registry (Optional[Dict[str, DLPackArray]]): A mapping of parameters to external resources.
        options (Dict): Compile and runtime options dictionary.
            Supported options:
                - "force_cpu_dense_resource": Force dense resources to reside in
                        CPU memory even when the type using the resource is on
                        another device. Only for debugging.

    Returns:
        fx.ir.Module: The imported FX graph module translated to a MLIR module.
        model: The model handle returned by compiling the MLIR module.
        is_output_scalar: List of output indices which are scalars.
    """
    mlir_module, is_output_scalar = fx.export_and_import(
        gm, export_meta=export_meta, options=options
    )

    def stream_mlir(op):
        """Yield MLIR lines one by one to avoid large memory usage."""
        for line in op.get_asm().split("\n"):
            yield line + "\n"

    if tmpdir := _create_artifact_dir():
        if os.getenv("MODULAR_PYTORCH_FX_IMPORTER_DUMP_MLIR", "") == "True":
            mlir_filename = tmpdir / "graph.fx.mlir"
            with open(mlir_filename, "w") as f:
                for line in stream_mlir(mlir_module.operation):
                    f.write(line)
            print(f"Saved mlir graph in: {mlir_filename}")

        with maybe_disable_fake_tensor_mode():
            _save_fx_graph_module(gm, tmpdir)
            _save_input_specs(input_specs, tmpdir)
            _save_example_inputs(example_inputs, tmpdir)

    # torch.jit.load doesn't work in FakeTensor mode, so we temporarily disable
    # it here. There might be cleaner ways to do this.
    # __dlpack_device__ fails if called in FakeTensor mode.
    with maybe_disable_fake_tensor_mode():
        model = inference_session.load(
            mlir_module,
            input_specs=input_specs,
            weights_registry=weights_registry,
        )

    return mlir_module, model, is_output_scalar


class GPUInteractionTracker(torch.fx.Interpreter):
    """
    Given a set of nodes that return a CPU tensor, traverse the downstream uses and find all the nodes that return a CUDA tensor.
    """

    class EarlyStopException(Exception):
        """Exception to stop GPU interaction tracking once all nodes are found."""

        pass

    def __init__(
        self,
        gm: torch.fx.GraphModule,
        nodes: Iterable[torch.fx.Node],
        fake_mode: FakeTensorMode,
    ):
        super().__init__(gm)
        self.fake_mode = fake_mode
        self.cpu_nodes = set(nodes)
        self.gpu_interactions: set[torch.fx.Node] = set()
        self.affected_values: dict[torch.fx.Node, set[torch.fx.Node]] = {
            target: set() for target in nodes
        }

    def run(self, *args):
        fake_args = [
            self.fake_mode.from_tensor(a) if isinstance(a, torch.Tensor) else a
            for a in args
        ]
        with self.fake_mode:
            try:
                return super().run(*fake_args)
            except GPUInteractionTracker.EarlyStopException:
                pass

    def run_node(self, n: torch.fx.Node) -> Any:
        result = super().run_node(n)

        for cpu_node in self.cpu_nodes:
            if n == cpu_node or any(
                inp in self.affected_values[cpu_node]
                for inp in n.all_input_nodes
            ):
                self.affected_values[cpu_node].add(n)

                has_cuda_output = (
                    hasattr(n, "meta")
                    and "val" in n.meta
                    and n.meta["val"].device.type == "cuda"
                )
                if has_cuda_output:
                    self.gpu_interactions.add(cpu_node)

                    # Stop if we've found interactions for all CPU nodes
                    if self.gpu_interactions == self.cpu_nodes:
                        raise GPUInteractionTracker.EarlyStopException()

        return result


@dynamo_timed_wrapper(phase_name="copy_graph_constants_to_gpu")
def copy_graph_constants_to_gpu(
    gm: torch.fx.GraphModule,
    example_inputs: list[Union[torch.SymInt, FakeTensor]],
    fake_mode: FakeTensorMode,
) -> dict[torch.fx.Node, torch.Tensor]:
    """
    Scalar values can appear as 0-dimensional CPU tensors even if the model is
    placed on a CUDA device. This function moves all such nodes to CUDA. The
    logic is adapted from torch/_dynamo/compiled_autograd.py `copy_graph_constants_to_gpu`.
    """

    to_move: dict[torch.fx.Node, torch.Tensor] = {}
    graph = gm.graph
    constant_attributes = graph.find_nodes(op="get_attr")

    for node in constant_attributes:
        assert hasattr(gm, node.target), (
            f"Attempting to retrieve attribute '{node.target}' from"
            " module, but no such attribute exists"
        )
        tensor = getattr(gm, node.target)
        assert not isinstance(tensor, FakeTensor)
        is_cpu = tensor.device.type == "cpu"
        is_scalar = len(tensor.size()) == 0
        if is_cpu and is_scalar:
            to_move[node] = tensor

    if len(to_move) == 0:
        return {}

    gpu_interaction_tracker = GPUInteractionTracker(
        gm, to_move.keys(), fake_mode
    )
    gpu_interaction_tracker.run(*example_inputs)

    to_move = {
        node: tensor
        for node, tensor in to_move.items()
        if node in gpu_interaction_tracker.gpu_interactions
    }

    with maybe_disable_fake_tensor_mode():
        for node, tensor in to_move.items():
            to_move[node] = tensor.cuda()
            setattr(gm, node.target, to_move[node])

    if len(to_move) > 0:
        FakeTensorProp(gm, fake_mode).propagate(*example_inputs)

    return to_move


def _annotate_input_indices(
    gm: torch.fx.GraphModule,
    flat_params: list[torch.Tensor],
    fw_metadata: torch._functorch.aot_autograd.ViewAndMutationMeta,
) -> list[int]:
    """
    Replaces the parameters of a PyTorch GraphModule with constants wherever possible.
    Returns a list of indices representing the input parameters that were not converted to constants.
    This is a modified version of replace_params_with_constants found in torch._inductor.freezing.
    """

    # Note: static_input_indices contains both parameters and mutated inputs.
    # We only want to convert parameters to constants, not mutated inputs.
    # - Placeholder nodes contain: parameters, inputs, and mutated inputs
    # - flat_params contains: parameters and mutated inputs
    # - We filter out mutated inputs to only convert parameters to constants
    placeholders = gm.graph.find_nodes(op="placeholder")
    for i, (param, node, info) in enumerate(
        zip(
            flat_params,
            [placeholders[j] for j in fw_metadata.static_input_indices],
            [
                fw_metadata.input_info[j]
                for j in fw_metadata.static_input_indices
            ],
        )
    ):
        if info.mutation_type in [
            MutationType.MUTATED_IN_GRAPH,
            MutationType.MUTATED_OUT_GRAPH,
        ]:
            continue
        param_metadata = extract_tensor_metadata(param)
        param_metadata.requires_grad = False

        # We enforce the params to be contiguous so we do the same for the fake tensor of the params here so that the metadata matches
        fake_tensor_metadata = extract_tensor_metadata(
            node.meta["val"].contiguous()
        )
        node.meta["static_input_index"] = i

    # Calculate indices to preserve
    mutated_inputs = {
        i
        for i, m in enumerate(fw_metadata.input_info)
        if m.mutation_type
        in (MutationType.MUTATED_IN_GRAPH, MutationType.MUTATED_OUT_GRAPH)
    }
    aliased_input_args = {
        out_info.base_idx
        for out_info in fw_metadata.output_info
        if out_info.base_idx is not None
    }
    non_static_inputs = set(range(len(placeholders))) - set(
        fw_metadata.static_input_indices
    )

    return sorted(list(mutated_inputs | aliased_input_args | non_static_inputs))


def _misc_fx_passes(
    gm: torch.fx.GraphModule,
    fw_metadata: Any,
    params_flat: list[torch.Tensor],
) -> tuple[torch.fx.GraphModule, list[int]]:
    """Taken from torch._inductor.freezing.freeze with the removal of
    constant_fold and binary_fold. Constant fold creates copies of parameters
    which cannot be deleted resulting in doubling of memory footprint for every
    compiled model.

    """
    view_to_reshape(gm)

    preserved_arg_indices = _annotate_input_indices(
        gm, params_flat, fw_metadata
    )

    cse_graph = fx_graph_cse(gm.graph)
    remove_noop_ops(gm.graph)
    gm.graph = cse_graph
    gm.recompile()

    return gm, preserved_arg_indices


def compile_fx(
    inference_session: engine.InferenceSession,
    gm: torch.fx.GraphModule,
    example_inputs: list[Union[torch.SymInt, FakeTensor]],
    params_flat: list[torch.Tensor],
    weights_registry: Optional[dict[str, DLPackArray]] = None,
    **kwargs,
) -> ModularCompiledFxGraph:
    """Compile the FX graph module and return a callable and serializable
      `ModularCompiledFxGraph`.

    Args:
        gm: (torch.fx.GraphModule): The torch FX graph module.
        example_inputs (List[Union[torch.SymInt, FakeTensor]]): A list of sample inputs (symbolic and fake types).
        params_flat (List[torch.Tensor]): A list of parameters as real tensors.
        weights_registry (Optional[Dict[str, DLPackArray]]): A mapping of parameters to external resources.
        **kwargs: keyword arguments primarily used for debugging internals and objects generated from torch.compile

    Returns:
        compiled_fx_graph (ModularCompiledFxGraph): ModularCompiledFxGraph: An object which maintains necessary state and methods to run, save and load a compiled model.
    """
    tracing_context = torch._guards.TracingContext.get()
    fw_metadata = tracing_context.fw_metadata

    gm, preserved = _misc_fx_passes(gm, fw_metadata, params_flat)
    gm.eval()
    aot_example_inputs = [example_inputs[ind] for ind in preserved]

    input_specs = construct_input_specs(aot_example_inputs)

    export_meta = ExportMeta(fw_metadata, preserved, params_flat)

    mlir_module, model_handle, is_output_scalar = compile_mlir_module(
        inference_session,
        gm,
        aot_example_inputs,
        input_specs,
        weights_registry,
        export_meta,
        options=kwargs,
    )

    # For testing and debugging
    if "fx_graphs" in kwargs:
        kwargs["fx_graphs"].append(gm.graph)
    if "mlir_modules" in kwargs:
        kwargs["mlir_modules"].append(mlir_module)

    compiled_fx_graph = ModularCompiledFxGraph(
        gm,
        example_inputs,
        input_specs,
        is_output_scalar,
        model_handle,
        preserved,
        kwargs,
        inference_session.stats_report,
    )
    return compiled_fx_graph


def get_cached_or_compile_fx_graph(
    inference_session: engine.InferenceSession,
    gm: torch.fx.GraphModule,
    example_inputs: list[Union[torch.SymInt, FakeTensor]],
    params_flat: list[torch.Tensor],
    weights_registry: Optional[dict[str, DLPackArray]],
    **kwargs,
) -> tuple[ModularCompiledFxGraph, int]:
    """Check cache if graph module has already been compiled. If not then
        compile the fx graph and store the compiled artifacts in the cache folder

    Args:
        inference_session (engine.InferenceSession): Modular engine.InferenceSession.
        gm: (torch.fx.GraphModule): The torch FX graph module.
        example_inputs (List[Union[torch.SymInt, FakeTensor]]): A list of
            sample inputs (symbolic and fake types).
        params_flat (List[torch.Tensor]): A list of parameters as real tensors.
        weights_registry (Optional[Dict[str, DLPackArray]]): A mapping of
            parameters to external resources.
        **kwargs: keyword arguments primarily used for debugging internals and
            objects generated from torch.compile


    Returns:
        compiled_fx_graph (ModularCompiledFxGraph): ModularCompiledFxGraph: An
            object which maintains necessary state and methods to run, save and
            load a compiled model.
        num_graphs (int): Number of graphs compiled.
    """

    fx_kwargs: dict[str, Any] = {}
    inputs_to_check = get_input_idxs_to_check(
        example_inputs, static_input_idxs=[]
    )
    num_graphs = 0
    try:
        compiled_fx_graph = ModularFxGraphCache.load(
            inference_session,
            gm,
            example_inputs,
            weights_registry,
            fx_kwargs,
            inputs_to_check,
        )

        if compiled_fx_graph is None:
            num_graphs = 1
            key = compiled_fx_graph_hash(
                gm, example_inputs, fx_kwargs, inputs_to_check
            )[0]
            compiled_fx_graph = compile_fx(
                inference_session,
                gm,
                example_inputs,
                params_flat,
                weights_registry,
                **kwargs,
            )
            ModularFxGraphCache.save(
                key,
                example_inputs,
                fx_kwargs,
                inputs_to_check,
                compiled_fx_graph,
            )
    except BypassFxGraphCache:
        num_graphs = 1
        compiled_fx_graph = compile_fx(
            inference_session,
            gm,
            example_inputs,
            params_flat,
            weights_registry,
            **kwargs,
        )

    return compiled_fx_graph, num_graphs


def _check_devices(
    devices: list[Device], example_inputs: list[Union[torch.SymInt, FakeTensor]]
):
    """A heuristic to guard users against trying to run a GPU model on the CPU
    and vice versa. The inference_session's device has no relation to the torch
    model or torch tensors. A mismatch in devices here is highly unlikely to be
    the user's intent so we raise an exception.


    Args:
        devices (List[Device]): List of max devices
        example_inputs (List[Union[torch.SymInt, FakeTensor]]): model inputs
    """
    # Revisit when we start using multi-device models
    engine_devices_are_cpu = [d.label == "cpu" for d in devices]

    input_devices_are_cpu = [
        t.is_cpu for t in example_inputs if isinstance(t, FakeTensor)
    ]

    if input_devices_are_cpu == []:
        return

    # Case 1: CPU engine with GPU inputs
    if all(engine_devices_are_cpu) and not any(input_devices_are_cpu):
        raise Exception(
            """The Modular InferenceSession is only using CPU devices, but one
            or more input torch tensors are not on the CPU"""
        )

    # Case 2: GPU engine with CPU inputs
    if not any(engine_devices_are_cpu) and all(input_devices_are_cpu):
        raise Exception(
            """The Modular InferenceSession is using GPU devices, but all
            input torch tensors are on the CPU"""
        )


@dynamo_timed_wrapper(phase_name="create weights registry")
def create_weights_registry(
    params_flat: list[torch.Tensor],
    constant_nodes: dict[torch.fx.Node, torch.Tensor] = {},
) -> Optional[dict[str, torch.Tensor]]:
    with maybe_disable_fake_tensor_mode():
        weights_registry = {}
        for i, param in enumerate(params_flat):
            params_flat[i] = param.contiguous()
            p = params_flat[i]
            dtype_str = str(p.dtype).split(".")[-1]
            shape_str = "x".join(map(str, p.shape))
            param_name = f"param_{i}_{dtype_str}_{shape_str}"
            weights_registry[param_name] = p.detach()

            # We use this attribute downstream to assign a name to the DenseResource
            setattr(p, WEIGHTS_REGISTRY_ATTR, param_name)

        for node, tensor in constant_nodes.items():
            dtype_str = str(tensor.dtype).split(".")[-1]
            shape_str = "x".join(map(str, tensor.shape))
            constant_name = f"{node.target}_{dtype_str}_{shape_str}"
            setattr(tensor, WEIGHTS_REGISTRY_ATTR, constant_name)
            weights_registry[constant_name] = tensor
        return weights_registry


class AotAutogradWrapper(AotAutograd):
    def __init__(self, **kwargs) -> None:
        self.backend_compiler = kwargs["fw_compiler"]
        super().__init__(**kwargs)

    def __call__(self, gm: torch.fx.GraphModule, example_inputs, **kwargs):
        self.backend_compiler.real_inputs = [
            weakref.ref(input) for input in example_inputs
        ]
        return super().__call__(gm, example_inputs, **kwargs)


def aot_autograd_wrapper(**kwargs) -> AotAutogradWrapper:
    return AotAutogradWrapper(**kwargs)


def get_modular_backend(
    inference_session: engine.InferenceSession, *args, **kwargs
):
    class ModularBackendCompiler:
        def __init__(self, *args, **kwargs):
            self.real_inputs: list[torch.Tensor] = []

        def _get_params_flat(self, static_input_indices: list[int]):
            params_flat = []
            for i in static_input_indices:
                input_ref = self.real_inputs[i]
                if isinstance(input_ref, weakref.ReferenceType):
                    actual_input = input_ref()
                    if actual_input is None:
                        raise RuntimeError(
                            f"Weakly referenced input at index {i} has been garbage collected"
                        )
                    params_flat.append(actual_input)
                else:
                    params_flat.append(input_ref)
            return params_flat

        def __call__(
            self,
            gm: torch.fx.GraphModule,
            example_inputs: list[Union[torch.SymInt, FakeTensor]],
        ):
            _check_devices(inference_session.devices, example_inputs)
            tracing_context = torch._guards.TracingContext.get()

            constant_nodes = {}
            if any([d.label == "gpu" for d in inference_session.devices]):
                constant_nodes = copy_graph_constants_to_gpu(
                    gm, example_inputs, tracing_context.fake_mode
                )

            fw_metadata = tracing_context.fw_metadata
            params_flat = self._get_params_flat(
                fw_metadata.static_input_indices
            )

            if tracing_context.global_context.global_state["grad_enabled"][1]:
                raise Exception(
                    """The Modular backend compiled callable must be wrapped in a
                    torch.no_grad() context"""
                )

            if kwargs.get("enable_weights_registry", True):
                weights_registry = create_weights_registry(
                    params_flat, constant_nodes
                )
            else:
                weights_registry = None

            if os.getenv("MODULAR_PYTORCH_ENABLE_CACHES", False) == "True":
                compiled_fx_graph, num_graphs = get_cached_or_compile_fx_graph(
                    inference_session,
                    gm,
                    example_inputs,
                    params_flat,
                    weights_registry,
                    **kwargs,
                )
            else:
                num_graphs = 1
                compiled_fx_graph = compile_fx(
                    inference_session,
                    gm,
                    example_inputs,
                    params_flat,
                    weights_registry,
                    **kwargs,
                )

            # stats_report gets serialized with the compiled graph. We populate the
            # dictionary passed in with the saved data for checking fallback
            # regressions
            if "stats_report" in kwargs:
                kwargs["stats_report"].update(compiled_fx_graph.stats_report)
                kwargs["stats_report"]["num_graphs"] += num_graphs
            return make_boxed_func(compiled_fx_graph)

    """Create a backend object that can be used in torch.compile."""
    backend_compiler = ModularBackendCompiler(*args, **kwargs)

    return torch._dynamo.disable(
        aot_autograd_wrapper(
            fw_compiler=backend_compiler,
            keep_inference_input_mutations=True,
            decompositions=get_decomposition_table(),
        )
    )


def get_modular_debug_backend(backend, *args, **kwargs):
    """Create a debug backend, based on an actual backend, that can be used in torch.compile."""

    @make_boxed_compiler
    def modular_backend_impl(
        gm: torch.fx.GraphModule,
        example_inputs: list[Union[torch.SymInt, FakeTensor]],
    ):
        tracing_context = torch._guards.TracingContext.get()
        params_flat = tracing_context.params_flat
        fw_metadata = tracing_context.fw_metadata

        gm, preserved = _misc_fx_passes(gm, fw_metadata, params_flat)
        gm.eval()

        def get_execute_and_verify_node(target):
            compiled_node = torch.compile(target, backend=backend)

            def execute_and_verify_node(*args, **kwargs):
                print("executing: ", target)
                exp_args = clone(args)
                exp_kwargs = clone(kwargs)

                exp_output = compiled_node(*exp_args, **exp_kwargs)

                ref_output = target(*args, **kwargs)

                if not compare(ref_output, exp_output, device="cpu"):
                    print("ref: ", ref_output)
                    print("exp: ", exp_output)
                    raise ValueError("Failed on node target ", target)

                return ref_output

            return execute_and_verify_node

        node_mapping = dict()

        for node in gm.graph.nodes:
            if (
                node.op == "placeholder"
                or node.op == "output"
                or node.op == "get_attr"
            ):
                continue
            node_mapping[node] = get_execute_and_verify_node(node.target)

        for node_key, node_value in node_mapping.items():
            with gm.graph.inserting_before(node_key):
                new_node = gm.graph.call_function(
                    node_value, args=node_key.args
                )
                node.replace_all_uses_with(new_node, propagate_meta=True)

        gm.recompile()

        # For testing and debugging
        if "fx_graphs" in kwargs:
            kwargs["fx_graphs"].append(gm.graph)

        def wrapper(*args):
            # The wrapper gets full set of inputs, including those that were
            # constantified by 'freeze'.  Here we filter them out and pass only
            # the actual inputs to the compiled function.
            args_new = [args[i] for i in preserved]
            assert gm
            return gm(*args_new)

        return wrapper

    return aot_autograd(
        fw_compiler=modular_backend_impl,
        keep_inference_input_mutations=True,
    )


class FunctionSchemaParser:
    def __init__(self):
        self.parser = re.compile(
            r"(?P<name>[^\(]+)\((?P<args>.*)\) -> (?P<returns>.*)"
        )

    def parse_custom_op_schema(
        self, schema: str
    ) -> tuple[str, str, Optional[str], str]:
        name, args, returns = self.parser.findall(schema)[0]
        namespace, overload_name = name.split("::")
        name_and_overload = overload_name.split(".")
        signature = f"({args}) -> ({returns})"
        return (
            namespace,
            name_and_overload[0],
            name_and_overload[1] if len(name_and_overload) > 1 else None,
            signature,
        )

    def get_overload_name(self, name: str, overload: Optional[str]) -> str:
        return name if overload is None else f"{name}.{overload}"


def _encode_function_name(name: str):
    name = name.replace("_", "_UND_")
    name = name.replace(".", "_DOT_")
    return name


def _get_torchscript_function_name_override(
    key: Union[tuple[str, str], tuple[str, str, str]], function_type: str
):
    return _encode_function_name(".".join(list(key) + [f"{function_type}"]))


class TorchMetadata:
    def __init__(self) -> None:
        self.shape_functions = dict()  # type: ignore
        self.dtype_functions = dict()  # type: ignore
        self.value_semantic_functions = dict()  # type: ignore

    def _get_op_key(self, op_name: str):
        return tuple(op_name.replace("::", ".").split("."))

    def register_shape_function(self, op_name):
        def decorator(fn):
            self.shape_functions[self._get_op_key(op_name)] = fn
            return fn

        return decorator

    def register_dtype_function(self, op_name):
        def decorator(fn):
            self.dtype_functions[self._get_op_key(op_name)] = fn
            return fn

        return decorator

    def set_has_value_semantics(self, op_name, value=True):
        self.value_semantic_functions[self._get_op_key(op_name)] = value

    def _get_jit_functions(self) -> torch.jit.ScriptModule:
        class TorchMetadataModule(torch.nn.Module):
            def __init__(self):
                super().__init__()

        module = TorchMetadataModule()
        jit_module = torch.jit.script(module)

        # Add the actual functions.
        # This allows the original shape inference functions to be written without
        # `self` argument, such that they work standalone as-is in python.
        # We can then coerce them to become module members in torchscript.
        for key, function in self.shape_functions.items():
            add_jit_function(
                jit_module._c,
                torch.jit.script(function),
                _get_torchscript_function_name_override(key, "shape"),
            )

        for key, function in self.dtype_functions.items():
            add_jit_function(
                jit_module._c,
                torch.jit.script(function),
                _get_torchscript_function_name_override(key, "dtype"),
            )

        for key, function in self.value_semantic_functions.items():
            # Dummy function.
            def value_semantics():
                pass

            add_jit_function(
                jit_module._c,
                torch.jit.script(value_semantics),
                _get_torchscript_function_name_override(key, "value_semantics"),
            )

        return jit_module

    def save(self, filename):
        torch.jit.save(self._get_jit_functions(), filename)


def _get_op_overload(namespace: str, name: str, overload: Optional[str] = None):
    op = getattr(getattr(torch.ops, namespace), name)
    return op.default if overload is None else getattr(op, overload)


# Note [Custom op registration]
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Extensibility of PyTorch's set of operations is possible through `CustomOpDef`
# since PyTorch 2.4.0. This new API offers advantages over static registration
# through PyTorch's C++ custom op APIs. One of them is being able to define
# dispatch boilerplate in Python.
# A distinct disadvantage is that `CustomOpDef` requires a Python interpreter to
# interact with the custom operations, so it is not ideal to deploy TorchScript
# or `torch.export` models using those custom operations.
#
# Concretely, we use `CustomOpDef` to register Mojo custom operations. When used
# in conjunction with `torch.compile`, the resulting FX graph will simply
# contain a reference to the registered custom ops used in the model, and the
# rest is handled in torch-mlir lowering just as with regular operations.
#
# In eager mode, the dispatch boilerplate registered with the `CustomOpDef` will
# be called. Here, our stack can handle this by wrapping the custom operation
# itself with `torch.compile` in the dispatch code, and we can again handle
# lowering as usual.
#
# Where extensibility becomes tricky is type inference; `torch.compile` expects
# that the registered kernels will work with `FakeTensor` inputs and outputs
# such that shape and dtype information can be inferred at (FX) graph building
# time.
#
# Our native Mojo kernels do not support FakeTensors, but `CustomOpDef` allows
# a separate dispatch function to be defined with `register_fake`. This dispatch
# will manually build and execute an FX graph, with the fallback kernel
# operation as a single graph node, through the MAX engine.
#
# To offer an ideal UX for the user, we can use Mojo-Python interop to define
# a PyTorch-native kernel implementation (`pytorch_fallback`) inside the
# struct-based extensibility kernel in Mojo. This kernel can be invoked by
# marshaling `FakeTensor`s as opaque types
# (`torch.opaque` -> `mo.opaque` -> `MojoValue<PythonObject>`)
# through the MAX engine into the kernel implementation.


def empty_callable(*args, **kwargs):
    pass


def register_custom_op(
    inference_session: engine.InferenceSession, custom_op_schema, meta_ops
) -> list[CustomOpDef]:
    parser = FunctionSchemaParser()
    op_defs: list[CustomOpDef] = []

    # Parse the function schema.
    namespace, name, overload, signature = parser.parse_custom_op_schema(
        custom_op_schema
    )

    if name.endswith("__pytorch_fallback__"):
        return op_defs

    fallback_op_name = parser.get_overload_name(
        f"{name}__pytorch_fallback__", overload
    )

    # Register the custom operation with an empty dispatch such that we can
    # create `eager_compiled`, which will both refer to the custom op,
    # and also be used as eager dispatch for the custom op.
    op_def = CustomOpDef(
        namespace,
        parser.get_overload_name(name, overload),
        signature,
        empty_callable,
    )

    # Register an opaque implementation of the custom operation, which will
    # be invoked by default when the custom operation is being used.
    eager_dispatch = torch.compile(
        _get_op_overload(namespace, name, overload),
        backend=get_modular_backend(inference_session),
    )

    def eager_dispatch_shim(*args, **kwargs):
        if "mojo_parameters" not in kwargs:
            kwargs["mojo_parameters"] = {}
        return eager_dispatch(*args, **kwargs)

    # Set the actual dispatch to replace `empty_callable`.
    device_types = None
    op_def.register_kernel(device_types)(eager_dispatch_shim)
    op_defs.append(op_def)

    # Register the fallback function as regular op.
    if fallback_op_name in meta_ops:

        def fake_dispatch(*args, **kwargs):
            fake_fn = _get_op_overload(
                namespace, f"{name}__pytorch_fallback__", overload
            )
            # Build a graph computing the function
            # `y = [namespace]::[name]__pytorch_fallback__(*args, **kwargs)`
            # with FakeTensor inputs and outputs.
            graph = torch.fx.Graph()
            fx_args = list()
            for i, _ in enumerate(args):
                fx_arg = graph.placeholder(f"arg{i}")
                fx_arg.meta["val"] = fx.Opaque()
                fx_args.append(fx_arg)
            y = graph.call_function(fake_fn, args=tuple(fx_args), kwargs=kwargs)
            y.meta["val"] = fx.Opaque()
            graph.output(y)

            # Use our own FX export/import function to translate the FX graph to
            # a MLIR module based on the torch-mlir dialect.
            #
            # Example graph:
            # module {
            #   func.func @main(%arg0: !torch.opaque<"PythonObject">, %arg1: !torch.opaque<"PythonObject">) -> !torch.opaque<"PythonObject"> {
            #     %0 = torch.operator "modular_ops.cumsum__pytorch_fallback__"(%arg0, %arg1) : (!torch.opaque<"PythonObject">, !torch.opaque<"PythonObject">) -> !torch.opaque<"PythonObject">
            #     return %0 : !torch.opaque<"PythonObject">
            #   }
            # }
            #
            mlir_module, _ = fx.export_and_import(
                fx.GraphModule(torch.nn.Module(), graph)
            )

            # Load and execute the graph using the MAX engine.
            # `[namespace]::[name]__pytorch_fallback__` will lower to the
            # fallback kernel defined in the custom op struct.
            fake_model = inference_session.load(
                mlir_module,
                input_specs=[
                    engine.TorchInputSpec([], DType._unknown) for _ in args
                ],
            )
            result = fake_model.execute_legacy(
                **dict(
                    zip(
                        [m.name for m in fake_model.input_metadata],
                        args[: len(args)],
                    )
                )
            )
            return result["result0"]

        fake_op_def = CustomOpDef(
            namespace,
            parser.get_overload_name(name + "__pytorch_fallback__", overload),
            meta_ops[fallback_op_name],
            fake_dispatch,
        )
        fake_op_def.register_fake(fake_dispatch)
        op_defs.append(fake_op_def)

        # Shim the fake dispatch such that the argument and result types are the
        # same as for the actual kernel. The `torch` argument is prepended.
        def fake_dispatch_shim(*args, **kwargs):
            if "mojo_parameters" not in kwargs:
                kwargs["mojo_parameters"] = {}
            return fake_dispatch(*([torch] + list(args)), **kwargs)

        op_def.register_fake(fake_dispatch_shim)

    # TODO: This is an untested stub, ONNX support for Mojo custom ops is not
    # currently functional.

    # Torch to ONNX export registration.
    def onnx_custom_op(g, *args, **kwargs):
        return g.op(f"{namespace}::{parser.get_overload_name(name, overload)}")

    torch.onnx.register_custom_op_symbolic(
        f"{namespace}::{parser.get_overload_name(name, overload)}",
        onnx_custom_op,
        11,
    )

    return op_defs


def register_custom_ops(inference_session: engine.InferenceSession):
    """Get all custom operations registered in the inference session
    and register them for PyTorch eager as well as ONNX."""

    # Retrieve function schemas from Mojo custom operations registered on the
    # inference session.
    custom_op_schemas = inference_session._get_torch_custom_op_schemas()

    parser = FunctionSchemaParser()

    op_defs = []

    # Collect the meta operations (shape and dtype inference).
    meta_ops = dict()
    for custom_op_schema in custom_op_schemas:
        # Parse the function schema.
        _, name, overload, signature = parser.parse_custom_op_schema(
            custom_op_schema
        )
        if name.endswith("__pytorch_fallback__"):
            meta_ops[parser.get_overload_name(name, overload)] = signature

    for custom_op_schema in custom_op_schemas:
        op_defs += register_custom_op(
            inference_session, custom_op_schema, meta_ops
        )

    return op_defs
