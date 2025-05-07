# ===----------------------------------------------------------------------=== #
#
# This file is Modular Inc proprietary.
#
# ===----------------------------------------------------------------------=== #

# ===----------------------------------------------------------------------=== #
#
# File originates from:
#   Repo:   git@github.com:llvm/torch-mlir.git
#   Commit: 0b7349102db619105fb282c2340a64c44e4adbe6
#   Path:   python/torch_mlir/extras/fx_importer.py
#
# ===----------------------------------------------------------------------=== #


# Copyright 2023 Advanced Micro Devices, Inc
#
# Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# Also available under a BSD-style license. See LICENSE.

try:
    from types import NoneType
except ImportError:
    # python less than 3.10 doesn't have NoneType
    NoneType = type(None)

import ctypes
import logging
import operator
import re
import weakref
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from types import BuiltinFunctionType, BuiltinMethodType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Optional,
    Union,
)

import numpy as np
import torch
import torch.export
import torch.fx as torch_fx
from torch import FunctionSchema
from torch import dtype as TorchDtype
from torch._functorch.aot_autograd import MutationType, ViewAndMutationMeta
from torch._ops import HigherOrderOperator
from torch._ops import OpOverload as TorchOpOverload
from torch._subclasses import FakeTensor as TorchFakeTensor
from torch.fx.passes.infra.pass_base import PassResult
from torch.fx.passes.infra.pass_manager import PassManager
from torch.fx.passes.shape_prop import TensorMetadata

_RUN_BUILTIN_REPLACE_PASS = True
try:
    from torch._guards import active_fake_mode
except ImportError:
    _RUN_BUILTIN_REPLACE_PASS = False


from torch.fx import Graph, GraphModule, Node

try:
    from torch.export.graph_signature import InputSpec as TypingInputSpec
except ModuleNotFoundError:
    # PyTorch prior to 2.3 is missing certain things we use in typing
    # signatures. Just make them be Any.
    if not TYPE_CHECKING:
        TypingInputSpec = Any
    else:
        raise

try:
    import ml_dtypes
except ModuleNotFoundError:
    # The third-party ml_dtypes package provides some optional
    # low precision data-types. If used in this file, it is
    # conditional.
    ml_dtypes = None

from torch.fx.node import Argument as NodeArgument

from ..dialects import func as func_dialect
from ..ir import (
    Attribute,
    BF16Type,
    Block,
    BoolAttr,
    ComplexType,
    Context,
    DenseElementsAttr,
    DenseResourceElementsAttr,
    F16Type,
    F32Type,
    F64Type,
    FloatAttr,
    FunctionType,
    IndexType,
    InsertionPoint,
    IntegerAttr,
    IntegerType,
    Location,
    Module,
    Operation,
    RankedTensorType,
    StringAttr,
    SymbolTable,
    Value,
)
from ..ir import Type as IrType

__all__ = [
    "FxImporter",
]

REQUIRED_DIALCTS = [
    "builtin",
    "func",
    "torch",
]

TORCH_DTYPE_TO_MLIR_TYPE_ASM = {
    torch.float16: "f16",
    torch.bfloat16: "bf16",
    torch.float32: "f32",
    torch.float64: "f64",
    torch.uint8: "ui8",
    torch.int8: "si8",
    torch.int16: "si16",
    torch.int32: "si32",
    torch.int64: "si64",
    torch.bool: "i1",
    torch.qint8: "!torch.qint8",
    torch.quint8: "!torch.quint8",
    torch.complex32: "complex<f16>",
    torch.complex64: "complex<f32>",
    torch.complex128: "complex<f64>",
}

TORCH_DTYPE_TO_MLIR_TYPE: dict[torch.dtype, Callable[[], IrType]] = {
    torch.float16: lambda: F16Type.get(),
    torch.bfloat16: lambda: BF16Type.get(),
    torch.float32: lambda: F32Type.get(),
    torch.float64: lambda: F64Type.get(),
    torch.uint8: lambda: IntegerType.get_unsigned(8),
    torch.int8: lambda: IntegerType.get_signed(8),
    torch.int16: lambda: IntegerType.get_signed(16),
    torch.int32: lambda: IntegerType.get_signed(32),
    torch.int64: lambda: IntegerType.get_signed(64),
    torch.bool: lambda: IntegerType.get_signless(1),
    torch.qint8: lambda: IntegerType.get_signed(8),
    torch.quint8: lambda: IntegerType.get_unsigned(8),
    torch.complex32: lambda: ComplexType.get(F16Type.get()),
    torch.complex64: lambda: ComplexType.get(F32Type.get()),
    torch.complex128: lambda: ComplexType.get(F64Type.get()),
}

TORCH_DTYPE_TO_NPY_TYPE = {
    # torch.qint8: None, # no equivalent np datatype
    # torch.quint8: None,
    torch.uint8: np.uint8,
    torch.int8: np.int8,
    torch.int16: np.int16,
    torch.int32: np.int32,
    torch.int64: np.int64,
    torch.float16: np.float16,
    torch.float32: np.float32,
    torch.float64: np.float64,
    torch.bool: np.bool_,
    # torch.complex32: None, # no equivalent precision for numpy
    torch.complex64: np.complex64,
    torch.complex128: np.complex128,
}
if ml_dtypes is not None:
    TORCH_DTYPE_TO_NPY_TYPE[torch.bfloat16] = ml_dtypes.bfloat16

TORCH_DTYPE_TO_INT = {
    torch.uint8: 0,
    torch.int8: 1,
    torch.int16: 2,
    torch.int32: 3,
    torch.int64: 4,
    torch.float16: 5,
    torch.float32: 6,
    torch.float64: 7,
    # torch.complex_half 8
    torch.complex32: 9,
    torch.complex64: 10,
    torch.bool: 11,
    # torch.qint8: 12, # quantized dtypes are not supported in all backends, currently we do not support them
    # torch.quint8: 13,
    # torch.qint32 14
    torch.bfloat16: 15,
}

TORCH_MEMORY_FORMAT_TO_INT = {
    torch.contiguous_format: 0,
    torch.preserve_format: 1,
    torch.channels_last: 2,
    torch.channels_last_3d: 3,
}

TORCH_LAYOUT_TO_INT = {
    torch.strided: 0,
    torch.sparse_coo: 1,
    torch.sparse_csr: 2,
    torch.sparse_csc: 3,
    torch.sparse_bsr: 4,
    torch.sparse_bsc: 5,
}

PY_BUILTIN_TO_TORCH_OP = {
    "truediv": torch.ops.aten.div,
    "mul": torch.ops.aten.mul,
    "add": torch.ops.aten.add,
    "sub": torch.ops.aten.sub,
    "lt": torch.ops.aten.lt,
    "le": torch.ops.aten.le,
    "ge": torch.ops.aten.ge,
    "ne": torch.ops.aten.ne,
    "gt": torch.ops.aten.gt,
    "floor": torch.ops.aten.floor,
    "ceil": torch.ops.aten.ceil,
    "floordiv": torch.ops.aten.floordiv,
    "neg": torch.ops.aten.neg,
    "pow": torch.ops.aten.pow,
}

from max._torch_mlir.torch_api_compat import maybe_disable_fake_tensor_mode

# The following are maps from symbolic ops to their non symbolic equivalents.
# TODO(PT-473): Correctly disambiguate if the symbolic op needs to be replaced
# by a default, int, float, etc. overload.
SYMBOLIC_OP_TO_TORCH_OP = {
    torch.ops.aten.sym_size.default: torch.ops.aten.size.default,
    torch.ops.aten.sym_size.int: torch.ops.aten.size.int,
    torch.ops.aten.sym_stride.default: torch.ops.aten.stride.default,
    torch.ops.aten.sym_stride.int: torch.ops.aten.stride.int,
    torch.ops.aten.sym_numel.default: torch.ops.aten.numel.default,
    torch._sym_sqrt: torch.ops.aten.sqrt.int,
    torch._sym_cos: torch.ops.aten.cos.int,
    torch._sym_cosh: torch.ops.aten.cosh.int,
    torch._sym_sin: torch.ops.aten.sin.int,
    torch._sym_sinh: torch.ops.aten.sinh.int,
    torch._sym_tan: torch.ops.aten.tan.int,
    torch._sym_tanh: torch.ops.aten.tanh.int,
    torch._sym_asin: torch.ops.aten.asin.int,
    torch._sym_acos: torch.ops.aten.acos.int,
    torch._sym_atan: torch.ops.aten.atan.int,
}

SYMBOLIC_TORCH_OPS = {key for key in SYMBOLIC_OP_TO_TORCH_OP}

WEIGHTS_REGISTRY_ATTR = "__weights_registry_name"


class Opaque:
    """
    Class to represent opaque inputs/outputs.

    The class is only meant to be used as a placeholder in FX graphs to deduce
    the torch-mlir `torch.opaque` type when importing.
    Example: `fx_arg.meta["val"] = fx.Opaque()`
    """


@dataclass(frozen=True)
class SparsityMeta:
    """
    Class for keeping track of sparsity meta data.

    NOTE: this will be fully replaced by
          torch.fx.passes.shape_prop.SparseTensorMetadata
    """

    layout: torch.layout
    batch_dim: int
    sparse_dim: int
    dense_dim: int
    blocksize: Optional[tuple[int, int]]
    pos_dtype: torch.dtype
    crd_dtype: torch.dtype


@dataclass
class ExportMeta:
    """
    Class for storing meta data needed for lowering to MLIR.
    """

    fw_metadata: ViewAndMutationMeta
    input_indices: list[int]
    params_flat: list[torch.Tensor]


def sparsity_encoding(shape: torch.Size, sparsity: SparsityMeta) -> str:
    """Returns sparse tensor encoding for the given sparse layout as string."""
    assert sparsity is not None

    # Sparse tensors have the form
    #   [ <batch_dimensions> , <sparse_dimensions>, <dense_dimensions> ]
    # which map directly to MLIR types.
    batch_dim, sparse_dim, dense_dim = (
        sparsity.batch_dim,
        sparsity.sparse_dim,
        sparsity.dense_dim,
    )
    dim = batch_dim + sparse_dim + dense_dim
    assert dim == len(shape)
    blocksize = sparsity.blocksize

    dims = ",".join(f"d{d}" for d in range(dim))

    if sparsity.layout is torch.sparse_coo:
        assert sparse_dim >= 2 and blocksize is None
        trail_dim = batch_dim + sparse_dim - 1
        coords = ",".join(
            f"d{d}:singleton(nonunique,soa)"
            for d in range(batch_dim + 1, trail_dim)
        )
        sep = "," if sparse_dim > 2 else ""
        lvls = f"d{batch_dim}:compressed(nonunique),{coords}{sep}d{trail_dim}:singleton(soa)"
    elif sparsity.layout is torch.sparse_csr:
        assert sparse_dim == 2 and blocksize is None
        lvls = f"d{batch_dim}:dense,d{batch_dim + 1}:compressed"
    elif sparsity.layout is torch.sparse_csc:
        assert sparse_dim == 2 and blocksize is None
        lvls = f"d{batch_dim + 1}:dense,d{batch_dim}:compressed"
    else:
        assert sparse_dim == 2 and blocksize is not None
        if sparsity.layout is torch.sparse_bsr:
            i, j = batch_dim, batch_dim + 1
        else:
            assert sparsity.layout is torch.sparse_bsc
            j, i = batch_dim, batch_dim + 1
        m, n = blocksize
        lvls = (
            f"d{i} floordiv {m}:dense,d{j} floordiv {n}:compressed,"
            f"d{i} mod {m}:dense,d{j} mod {n}:dense"
        )

    if batch_dim > 0:
        batch = ",".join(f"d{d}:batch" for d in range(batch_dim))
        lvls = f"{batch},{lvls}"

    if dense_dim > 0:
        dense = ",".join(
            f"d{d}:dense" for d in range(batch_dim + sparse_dim, dim)
        )
        lvls = f"{lvls},{dense}"

    posw = torch.iinfo(sparsity.pos_dtype).bits
    crdw = torch.iinfo(sparsity.crd_dtype).bits
    return f"#sparse_tensor.encoding<{{map=({dims})->({lvls}),posWidth={posw},crdWidth={crdw}}}>"


def is_symbolic(obj: Any) -> bool:
    """Check whether an object in our graph is symbolic"""
    return isinstance(obj, (torch.SymInt, torch.SymFloat, torch.SymBool))


def is_builtin_function_or_method(obj: Any) -> bool:
    return isinstance(obj, (BuiltinMethodType, BuiltinFunctionType))


def _populate_meta(
    node: torch.fx.Node, fake_mode: torch._subclasses.FakeTensorMode
):
    fake_args = [
        arg.meta["val"] if isinstance(arg, torch.fx.Node) else arg
        for arg in node.args
    ]

    fake_res = node.target(*fake_args)
    if isinstance(fake_res, torch.Tensor):
        fake_res = fake_mode.from_tensor(fake_res)

    node.meta["val"] = fake_res


# replace operator.mod(a,b) by a - b * (a // b)
def replace_int_modulo(
    graph_module: torch.fx.GraphModule,
) -> torch.fx.GraphModule:
    graph = graph_module.graph
    nodes_to_erase = []
    fake_mode = active_fake_mode()

    for node in graph.nodes:
        if not (
            node.op == "call_function"
            and is_builtin_function_or_method(node.target)
            and node.target.__name__ == "mod"
        ):
            continue

        for a in node.args:
            if hasattr(a, "meta"):
                assert a.meta["val"].node.pytype is int
            else:
                assert type(a) is int

        nodes_to_erase.append(node)

        with graph.inserting_after(node):
            floordiv = graph.call_function(
                torch.ops.aten.floordiv.int, args=node.args
            )
            _populate_meta(floordiv, fake_mode)

        with graph.inserting_after(floordiv):
            mul = graph.call_function(
                torch.ops.aten.mul.int, args=(node.args[1], floordiv)
            )
            _populate_meta(mul, fake_mode)

        with graph.inserting_after(mul):
            sub = graph.call_function(
                torch.ops.aten.sub.int, args=(node.args[0], mul)
            )
            _populate_meta(sub, fake_mode)

        node.replace_all_uses_with(sub)

    modified = len(nodes_to_erase) > 0

    for n in nodes_to_erase:
        graph.erase_node(n)

    return PassResult(graph_module, modified=modified)


def replace_builtin_trunc(
    graph_module: torch.fx.GraphModule,
) -> torch.fx.GraphModule:
    graph = graph_module.graph
    nodes_to_erase = []
    fake_mode = active_fake_mode()

    for node in graph.nodes:
        if not (
            node.op == "call_function"
            and is_builtin_function_or_method(node.target)
            and node.target.__name__ == "trunc"
        ):
            continue

        assert node.args[0].meta["val"].node.pytype is float
        nodes_to_erase.append(node)
        convert_trunc_output_to_int = node.meta["val"].node.pytype is not float
        scalar_implicit_op = (
            torch.ops.aten.FloatImplicit.default
            if not convert_trunc_output_to_int
            else torch.ops.aten.IntImplicit.default
        )

        with graph.inserting_after(node):
            arg_as_tensor = graph.call_function(
                torch.ops.aten.tensor.float, args=node.args
            )
            _populate_meta(arg_as_tensor, fake_mode)

        with graph.inserting_after(arg_as_tensor):
            aten_trunc = graph.call_function(
                torch.ops.aten.trunc.default, args=(arg_as_tensor,)
            )
            _populate_meta(aten_trunc, fake_mode)

        typed_trunc_tensor = aten_trunc
        if convert_trunc_output_to_int:
            with graph.inserting_after(aten_trunc):
                typed_trunc_tensor = graph.call_function(
                    torch._prims.convert_element_type,
                    args=(arg_as_tensor, torch.int32),
                )
                _populate_meta(typed_trunc_tensor, fake_mode)

        with graph.inserting_after(typed_trunc_tensor):
            trunc_to_scalar = graph.call_function(
                scalar_implicit_op, args=(typed_trunc_tensor,)
            )
            # calling _populate_meta here will cause graph breaks

        node.replace_all_uses_with(trunc_to_scalar, propagate_meta=True)

    modified = len(nodes_to_erase) > 0

    for n in nodes_to_erase:
        graph.erase_node(n)

    return PassResult(graph_module, modified=modified)


# TODO: switch back to `slots=True` when py3.9 support is dropped
@dataclass(frozen=True)
class InputInfo:
    """Provides additional metadata when resolving inputs."""

    program: torch.export.ExportedProgram
    input_spec: TypingInputSpec
    node: Node
    ir_type: IrType
    mutable_producer_node_name: Optional[str] = None
    store_producer_node: Optional[str] = None


class FxImporterHooks:
    """Hooks to control the behavior of the FxImporter."""

    def prepare_module(self, module_op: Operation):
        """Performs any needed preparation work on the module."""
        ...

    def resolve_literal(
        self, gni: "GraphNodeImporter", literal: Any
    ) -> Optional[Value]:
        """User overridable hook to resolve a literal value."""
        return None

    def resolve_input(
        self, gni: "GraphNodeImporter", value: Any, info: InputInfo
    ) -> Optional[Value]:
        """Resolves a Parameter or Buffer input to an IR value.

        If the 'mutable_producer_node_name' option is set, then the result must
        be a `!torch.tensor`.
        Otherwise, it must be an immutable `!torch.vtensor`. If this constraint cannot
        be met, the implementation must either error or return None to delegate to
        the default.
        """
        return None

    def store_produced_value(
        self,
        gni: "GraphNodeImporter",
        py_value: Any,
        produced_ir_value: Any,
        info: InputInfo,
    ):
        """Given a load/store semantic mutatation, issues the store.

        This style is used for buffer and parameter updates, which are assumed to be
        non-SSA updates that are otherwise in the value-tensor domain.
        """
        raise NotImplementedError(
            f"Store of a mutation to {info} is not supported (from"
            f" {produced_ir_value})"
        )


class FxImporter:
    """Main entry-point for importing an fx.GraphModule.

    The FxImporter is a low-level class intended for framework integrators.
    It provides several options for customization:

    * config_check: Optionally allows some per-import configuration safety
      checks to be skipped.
    * literal_resolver_callback: Callback that will be invoked when a literal,
      live torch.Tensor is encountered in the FX graph, allowing the default
      action (which is to inline the data as a DenseResourceElementsAttr) to
      be completely overriden.
    * py_attr_tracker: Weak reference tracker for live PyTorch objects used
      to unique them with respect to attributes. If not specified, there will
      be one reference tracker per import, but this can be injected to share
      the same uniqueing across imports (i.e. if building multiple functions
      into the same context or module).
    """

    __slots__ = [
        "_c",
        "_cc",
        "_m",
        "_m_ip",
        "_py_attr_tracker",
        "_hooks",
        "symbol_table",
        "export_meta",
    ]

    def __init__(
        self,
        *,
        module: Optional[Module] = None,
        context: Optional[Context] = None,
        config_check: bool = True,
        py_attr_tracker: Optional["RefTracker"] = None,
        hooks: Optional[FxImporterHooks] = None,
        export_meta: ExportMeta = None,
    ):
        if module is not None:
            assert context is None, (
                "If configuring with a Module, context must be None"
            )
            self._m = module
            self._c = self.module.context
        else:
            self._c = context if context else Context()
            self._m = Module.create(Location.unknown(self._c))
        if config_check:
            # Production code can disable this for a bit of a boost.
            self._config_check()
        self._py_attr_tracker = py_attr_tracker or RefTracker()
        self._cc = ContextCache(self._c, py_attr_tracker=self._py_attr_tracker)
        self._m_ip = InsertionPoint(self._m.body)
        self._hooks = hooks or FxImporterHooks()
        self.symbol_table = SymbolTable(self._m.operation)
        self._hooks.prepare_module(self._m.operation)
        self.export_meta = export_meta

    def _config_check(self):
        for dname in REQUIRED_DIALCTS:
            try:
                self._c.dialects[dname]
                logging.debug("Context has registered dialect '%s'", dname)
            except IndexError:
                raise RuntimeError(
                    f"The MLIR context {self._c} is missing required dialect"
                    f" '{dname}'"
                )

    @property
    def module(self) -> Module:
        return self._m

    @property
    def module_op(self) -> Operation:
        return self._m.operation

    def import_stateless_graph(
        self,
        gm: GraphModule,
        *,
        func_name: str = "main",
        func_visibility: Optional[str] = None,
        options: dict = {},
    ) -> tuple[Operation, list[bool]]:
        """Low-level import of a functionalized, assumed stateless Graph as a func.

        TODO: This mechanism is deprecated by the `import_program` entry-point and
        it should be removed when no longer required for backwards compatibility.
        """
        passes = []
        if _RUN_BUILTIN_REPLACE_PASS:
            passes.append(replace_builtin_trunc)
            passes.append(replace_int_modulo)

        pass_manager = PassManager(
            passes=passes,
            run_checks_after_each_pass=True,
            suppress_check_failures=False,
        )
        pass_manager(gm)
        g = gm.graph

        ftype, loc, is_output_scalar = self._graph_to_function_meta(g)
        # TODO: The FuncOp constructor requires a context-manager context.
        # Fix upstream and then unnest.
        # See: https://github.com/nod-ai/SHARK-Turbine/issues/138
        with loc:
            func = func_dialect.FuncOp(
                func_name,
                ftype,
                ip=self._m_ip,
                visibility=func_visibility,
            )
            entry_block = Block.create_at_start(func.body, ftype.inputs)
        node_importer = GraphNodeImporter(
            self,
            self._c,
            self._cc,
            entry_block,
            options,
        )
        node_importer.import_nodes(g.nodes)
        self.symbol_table.insert(func)
        return func, is_output_scalar

    def _graph_to_function_meta(
        self, g: Graph
    ) -> tuple[FunctionType, Location, list[bool]]:
        """Extracts function metadata from the Graph.

        Principally, this includes the FunctionType, but in the future,
        it should also return other annotations (input strides, etc) that
        affect compilation and should be included as arg attrs.
        """
        input_types = []
        result_types = []
        is_output_scalar = []
        loc = None
        keep_input_mutations = False
        if (self.export_meta is not None) and (
            keep_input_mutations
            := self.export_meta.fw_metadata.keep_input_mutations
        ):
            input_infos = [
                self.export_meta.fw_metadata.input_info[i]
                for i in self.export_meta.input_indices
            ]
            input_nodes = [
                n
                for i, n in enumerate(g.find_nodes(op="placeholder"))
                if "static_input_index" not in n.meta
            ]
            assert len(input_nodes) == len(input_infos)
            input_infos_iter = iter(input_infos)

        for node in g.nodes:
            # Assume that the first node we can get a location for is about as
            # good as it gets as an overall function location.
            if loc is None:
                loc = self._cc.get_node_location(node)
            if (
                node.op == "placeholder"
                and "static_input_index" not in node.meta
            ):
                mutable = False
                if keep_input_mutations:
                    input_info = next(input_infos_iter)
                    mutable = input_info.mutation_type in (
                        MutationType.MUTATED_IN_GRAPH,
                        MutationType.MUTATED_OUT_GRAPH,
                    )

                input_types.append(
                    self._cc.node_val_to_type(node, mutable=mutable)
                )
            elif node.op == "output":
                # An output node's args[0] is the return value. If it is not
                # "boxed" as a tuple, wrap it so we can emit as multi-results.
                for result_node in (
                    node.args[0]
                    if isinstance(node.args[0], tuple)
                    else (node.args[0],)
                ):
                    if result_node is None:
                        result_types.append(
                            IrType.parse("!torch.none", context=self._c)
                        )
                        # TODO: do we support graphs with no output?
                        is_output_scalar.append(True)
                    elif isinstance(result_node, torch.Tensor):
                        is_output_scalar.append(False)
                        result_types.append(
                            self._cc.get_tensor_type(
                                result_node.size(),
                                result_node.dtype,
                                result_node.get_device(),
                            )
                        )
                    elif type(result_node) in SCALAR_TYPE_TO_TORCH_MLIR_TYPE:
                        is_output_scalar.append(True)
                        result_types.append(
                            IrType.parse(
                                SCALAR_TYPE_TO_TORCH_MLIR_TYPE[
                                    type(result_node)
                                ],
                                self._c,
                            )
                        )
                    else:
                        val = result_node.meta.get("val")
                        if isinstance(val, TorchFakeTensor):
                            is_output_scalar.append(False)
                        else:
                            is_output_scalar.append(True)
                        result_types.append(
                            self._cc.node_val_to_type(result_node)
                        )
        return (
            FunctionType.get(input_types, result_types, context=self._c),
            loc if loc else Location.unknown(self._c),
            is_output_scalar,
        )


class ContextCache:
    """Caches per-context lookups of various things that we ask for repeatedly."""

    __slots__ = [
        "_c",
        "_dtype_to_type",
        "_tensor_metadata_cache",
        "_py_attr_tracker",
        # Types.
        "torch_bool_type",
        "torch_float_type",
        "torch_int_type",
        "torch_none_type",
        "torch_str_type",
        "torch_device_type",
        "torch_opaque_type",
    ]

    def __init__(
        self,
        context: Context,
        *,
        py_attr_tracker: Optional["RefTracker"] = None,
    ):
        self._c = context
        self._dtype_to_type: dict[TorchDtype, IrType] = {}
        self._tensor_metadata_cache: dict[
            tuple[
                torch.Size,
                torch.dtype,
                Optional[SparsityMeta],
                bool,
                Optional[int],
            ],
            IrType,
        ] = {}
        self._py_attr_tracker = py_attr_tracker or RefTracker()

        # Common types.
        with context:
            self.torch_bool_type = IrType.parse("!torch.bool")
            self.torch_float_type = IrType.parse("!torch.float")
            self.torch_int_type = IrType.parse("!torch.int")
            self.torch_none_type = IrType.parse("!torch.none")
            self.torch_str_type = IrType.parse("!torch.str")
            self.torch_device_type = IrType.parse("!torch.Device")
            self.torch_opaque_type = IrType.parse(
                '!torch.opaque<"PythonObject">'
            )

    def integer_attr(self, value: int, bits: int) -> Attribute:
        c = self._c
        return IntegerAttr.get(IntegerType.get_signless(bits, c), value)

    def get_tensor_type(
        self,
        shape: torch.Size,
        dtype: torch.dtype,
        device_id: Optional[int],
        *,
        sparsity: Optional[SparsityMeta] = None,
        mutable: bool = True,
    ) -> IrType:
        # TODO: enable sparsity
        assert sparsity is None, "we don't support sparsity yet"
        # if sparsity is not None:
        #     encoding = sparsity_encoding(shape, sparsity)
        #     assert encoding is not None
        #     return IrType.parse(
        #         f"!{stem}<[{shape_asm}],{str(mlir_dtype)},{encoding}>",
        #         context=self._c,
        #     )

        type_str = "tensor" if mutable else "vtensor"
        params: list[str] = [
            f"[{','.join('?' if is_symbolic(d) else str(d) for d in shape)}]",
            str(self.dtype_to_type(dtype)),
        ]
        # TODO(PT-644): Multi-device support, currently only supports `gpu:0`.
        if device_id is not None:
            params.append('"cpu"' if device_id == -1 else '"gpu:0"')

        return IrType.parse(
            f"!torch.{type_str}<{','.join(params)}>", context=self._c
        )

    def get_opaque_type(self):
        """Return IrType for !torch.opaque."""
        return self.torch_opaque_type

    def node_val_to_type(
        self, node: torch_fx.Node, *, mutable: bool = True
    ) -> IrType:
        try:
            val = node.meta.get("val")
            tensor_meta = node.meta.get("tensor_meta", None)
            sparsity = node.meta.get("sparsity", None)
        except KeyError as e:
            raise RuntimeError(
                "FIXME: Illegal access to torch.fx.Node.meta:"
                f" {e} ({node.meta.keys()} : {node.meta})"
            )
        return self.value_info_to_type(
            val, tensor_meta=tensor_meta, sparsity=sparsity, mutable=mutable
        )

    def value_info_to_type(
        self,
        val,
        *,
        tensor_meta: Optional[TensorMetadata] = None,
        sparsity=None,
        mutable: bool = True,
    ):
        if tensor_meta is not None:
            assert isinstance(tensor_meta, TensorMetadata)
            # Quantized tensor meta data is not preserved in our lowering,
            # so throw error instead of silently doing wrong thing.
            if tensor_meta.is_quantized:
                raise NotImplementedError(
                    "Quantized tensor meta data is not supported."
                )
            else:
                return self.tensor_metadata_to_type(
                    tensor_meta,
                    device_id=val.get_device(),
                    sparsity=sparsity,
                    mutable=mutable,
                )
        elif val is not None:
            # some nodes with symbolic inputs pass a 'val' attribute rather than
            # tensor_meta
            if isinstance(val, TorchFakeTensor):
                return self.get_tensor_type(
                    val.size(),
                    val.dtype,
                    val.get_device(),
                    sparsity=sparsity,
                    mutable=mutable,
                )
            if isinstance(val, Opaque):
                return self.get_opaque_type()

        # Handle list values.
        if isinstance(val, list):
            if len(val) == 0:
                raise NotImplementedError(
                    "Could not determine the type of the list elements."
                )

            inner_type = type(val[0])

            if not all([type(v) == inner_type for v in val]):
                return IrType.parse(
                    PY_TYPE_TO_TORCH_LIST_TYPE.get("any"), self._c
                )
            elif all([isinstance(v, TorchFakeTensor) for v in val]):
                return IrType.parse(
                    PY_TYPE_TO_TORCH_LIST_TYPE.get("tensor"), self._c
                )
            else:
                return IrType.parse(
                    PY_TYPE_TO_TORCH_LIST_TYPE.get(type(val[0])), self._c
                )

        # Note that None is a valid scalar here, so it is important that this
        # is always checked as the last fallback.
        t = SCALAR_TYPE_TO_TORCH_MLIR_TYPE.get(type(val))
        if t is not None:
            return IrType.parse(t, self._c)

        raise NotImplementedError(
            f"Could not deduce type from value info: tensor_meta={tensor_meta},"
            f" val={val} {type(val)}, sparsity={sparsity}"
        )

    def tensor_metadata_to_type(
        self,
        tm: TensorMetadata,
        *,
        device_id: Optional[int],
        sparsity: Optional[SparsityMeta] = None,
        mutable: bool = True,
    ) -> IrType:
        tm_shape = tuple(
            item.node if is_symbolic(item) else item for item in list(tm.shape)
        )

        key = (tm_shape, tm.dtype, sparsity, mutable, device_id)
        t = self._tensor_metadata_cache.get(key)
        if t is None:
            t = self.get_tensor_type(
                tm.shape,
                tm.dtype,
                device_id,
                sparsity=sparsity,
                mutable=mutable,
            )
            self._tensor_metadata_cache[key] = t
        return t

    def dtype_to_type(self, dtype: TorchDtype) -> IrType:
        t = self._dtype_to_type.get(dtype)
        if t is None:
            try:
                asm = TORCH_DTYPE_TO_MLIR_TYPE_ASM[dtype]
            except IndexError:
                raise ValueError(
                    f"Unknown conversion from {dtype} to IREE type"
                )
            t = IrType.parse(asm, self._c)
            self._dtype_to_type[dtype] = t
        return t

    def get_node_location(self, node: torch_fx.Node) -> Optional[Location]:
        stack_trace = node.meta.get("stack_trace")
        if stack_trace is None:
            return None
        # Ugh.
        # TODO: Avoid needing to regex match this.
        # https://github.com/pytorch/pytorch/issues/91000
        stack_trace = node.stack_trace
        if stack_trace:
            m = re.search(r"""File "([^"]+)", line ([0-9]+),""", stack_trace)
            if m:
                filename, line = m.group(1), int(m.group(2))
                return Location.file(filename, line, col=0, context=self._c)
        return Location.unknown(context=self._c)


class GraphNodeImporter:
    """Imports graph nodes into an MLIR function.

    The caller must have already created the function.
    """

    __slots__ = [
        "_b",
        "_c",
        "_cc",
        "_on_node_produced",
        "_v",
        "_multi_result_nodes",
        "fx_importer",
        "_options",
    ]

    def __init__(
        self,
        fx_importer: FxImporter,
        context: Context,
        context_cache: ContextCache,
        block: Block,
        options: dict,
    ):
        self.fx_importer = fx_importer
        self._c = context
        self._cc = context_cache
        self._b = block
        # Map of (Node, result_index) to MLIR Value or a callback that lazily
        # constructs and returns a value.
        self._v: dict[
            Union[Callable[[], Value], tuple[torch_fx.Node, int]], Value
        ] = {}
        # Map of node name to hook that should be called when it is produced.
        self._on_node_produced: dict[str, Callable[[Value], None]] = {}
        # Statically multi-result nodes which we have de-tupled are noted here.
        # They will have their getitem calls short-circuited.
        self._multi_result_nodes: set[torch_fx.Node] = set()
        self._options = options

    def bind_node_value(
        self,
        node: Node,
        value: Union[Value, Callable[[], Value]],
        result_index: int = 0,
    ):
        """Binds a node to a value (and asserts if already bound).

        This is used by outside callers. Many internal callers poke directly
        into the dict.
        """
        key = (node, result_index)
        assert key not in self._v, f"Node already has a value: {node}"
        self._v[key] = value

        producer_callback = self._on_node_produced.get(node.name)
        if producer_callback is not None:
            producer_callback(value)

    def has_node_value(self, node: Node, result_index: int = 0) -> bool:
        key = (node, result_index)
        return key in self._v

    def resolve_node_value(self, node: Node, result_index: int = 0) -> Value:
        """Resolves a node to a value."""
        key = (node, result_index)
        try:
            binding = self._v[key]
        except KeyError:
            raise KeyError(
                f"FX Node {node} has not been bound to an MLIR value"
            )
        if isinstance(binding, Value):
            return binding

        # It is a lazy callback.
        value = binding()
        self._v[key] = value
        return value

    def import_vtensor_to_tensor(
        self, loc: Location, node: Node, value: Value, mutable_type
    ) -> Value:
        """Imports a node that copies from value to non-value tensor.

        This will generate and associate the following with the node:
          %1 = torch.copy.to_tensor %0
        """
        with loc:
            copy_result = Operation.create(
                "torch.copy.to_tensor",
                results=[mutable_type],
                operands=[value],
            ).result
            self.bind_node_value(node, copy_result)
        return copy_result

    def import_constant(
        self, loc: Location, node: Node, constant: Any
    ) -> Value:
        with loc, InsertionPoint(self._b):
            value = self._import_literal(constant)
            self.bind_node_value(node, value)
        return value

    def lazy_import_parameter(
        self, loc, node: Node, parameter_value: Any, info: InputInfo
    ):
        def _on_access() -> Value:
            with loc, InsertionPoint(self._b):
                # TODO: Should go to a parameter binding hook.
                return self._import_input(parameter_value, info)

        self.bind_node_value(node, _on_access)

    def lazy_import_buffer(
        self,
        loc,
        node: Node,
        buffer_value: Any,
        info: InputInfo,
    ):
        def _on_access() -> Value:
            with loc, InsertionPoint(self._b):
                # TODO: Should go to a buffer binding hook.
                return self._import_input(buffer_value, info)

        self.bind_node_value(node, _on_access)

        if info.mutable_producer_node_name is not None:
            raise NotImplementedError("NYI: Mutable SSA buffer updates")

        if info.store_producer_node is not None:

            def on_produced(value: Value):
                with loc, InsertionPoint(self._b):
                    self.fx_importer._hooks.store_produced_value(
                        self, buffer_value, value, info
                    )

            self._on_node_produced[info.store_producer_node] = on_produced

    def return_node_values(self, loc, nodes: list[Node]):
        with loc, InsertionPoint(self._b):
            operands = [self.resolve_node_value(n) for n in nodes]
            func_dialect.ReturnOp(operands, loc=loc)

    def import_nodes(
        self, nodes: Iterable[Node], *, skip_placeholders_outputs: bool = False
    ):
        with InsertionPoint(self._b):
            loc = Location.unknown()
            num_placeholders = 0
            for node in nodes:
                op = node.op
                # Attempt to extract locations. Not everything has them,
                # so we do our best.
                new_loc = self._cc.get_node_location(node)
                if new_loc is not None:
                    loc = new_loc
                if (
                    op == "placeholder"
                    and not skip_placeholders_outputs
                    and "static_input_index" not in node.meta
                ):
                    # Associate the placeholder node with corresponding block
                    # argument.

                    value = self._b.arguments[num_placeholders]

                    # Check if the current type is the same as the default (mutable) type.
                    mutable_type = self._cc.value_info_to_type(
                        node.meta.get("val")
                    )
                    if value.type != mutable_type:
                        # If the placeholder is a value tensor, copy it to a non-value
                        # tensor to match the rest of the graph.
                        value = self.import_vtensor_to_tensor(
                            loc, node, value, mutable_type
                        )
                    else:
                        self.bind_node_value(node, value)

                    num_placeholders += 1
                elif op == "call_function":
                    target = node.target
                    if target == operator.getitem:
                        # Special case handling of getitem for when it is resolving
                        # against a function call that we know has returned multiple
                        # results. We short-circuit this case because we have modeled
                        # function calls to natively return multiple results vs tupling.
                        getitem_ref, getitem_index = node.args
                        if getitem_ref in self._multi_result_nodes:
                            try:
                                self.bind_node_value(
                                    node,
                                    self.resolve_node_value(
                                        getitem_ref, getitem_index
                                    ),
                                )
                            except IndexError:
                                raise RuntimeError(
                                    "getitem de-aliasing failed. This likely"
                                    " indicates a programmer error that"
                                    " usually would have happened at runtime."
                                    " Please notify developers if this case"
                                    f" happens (at {loc})."
                                )
                        else:
                            # Replace built-in `getitem` with ATen `getitem` for lists (t).
                            self._import_torch_op_overload(
                                loc, node, torch.ops.aten.__getitem__.t
                            )
                    elif target in SYMBOLIC_TORCH_OPS or (
                        is_symbolic(node.meta.get("val"))
                        and (
                            is_builtin_function_or_method(target)
                            or target == torch.sym_float
                        )
                    ):
                        self._import_symbolic_torch_op(loc, node, target)
                    elif isinstance(target, TorchOpOverload):
                        # Dispatch to an ATen op.
                        self._import_torch_op_overload(loc, node, target)
                    elif isinstance(target, HigherOrderOperator):
                        self._import_hop(loc, node, target)
                    elif isinstance(target, torch._ops.OpOverloadPacket):
                        self._import_torch_op_overload(
                            loc, node, target.default
                        )
                    else:
                        raise NotImplementedError(
                            "FIX ME: Unimplemented call_function:"
                            f" target={node.target}, {node.meta}"
                        )
                elif op == "output" and not skip_placeholders_outputs:
                    # args[0] is a singleton tuple that we flatten into multiple results.
                    # If it is not "boxed" as a tuple, wrap it.
                    operands = [
                        self._import_argument(loc, arg, self._options)
                        for arg in (
                            node.args[0]
                            if isinstance(node.args[0], tuple)
                            else (node.args[0],)
                        )
                    ]
                    func_dialect.ReturnOp(operands, loc=loc)

    def _promote_symbolic_scalar_int_float(self, loc, graph, param, name=None):
        temp_target = torch.ops.aten.Float.Scalar
        if not name:
            name = f"{str(param)}_as_float"
        temp_node = Node(
            graph=graph,
            name=name,
            op="call_function",
            target=temp_target,
            args=(param,),
            kwargs={},
            return_type=float,
        )
        temp_node.meta["val"] = torch.sym_float(param.meta["val"])
        self._import_torch_op_overload(loc, temp_node, temp_target)
        return temp_node

    def _import_symbolic_torch_op(
        self,
        loc: Location,
        node: torch_fx.Node,
        target: Union[
            torch._ops.OpOverloadPacket, BuiltinMethodType, BuiltinFunctionType
        ],
    ):
        # parse builtin operations like add, sub, mul, etc. because dynamo captures these
        # operations on symbolic arguments as regular python expressions rather than as torch ops
        if is_builtin_function_or_method(target) or target == torch.sym_float:
            arg_types = []
            for arg in node.args:
                if isinstance(arg, Node):
                    if hasattr(arg.meta["val"], "node"):
                        arg_types.append(arg.meta["val"].node.pytype)
                    else:
                        assert isinstance(arg.meta["val"], (float, int))
                        arg_types.append(type(arg.meta["val"]))
                else:
                    arg_types.append(type(arg))
            is_int = [item is int for item in arg_types]
            if all(is_int):
                op_overload = "int"
                if target.__name__ == "pow":
                    # aten.pow.int returns float, so we need aten.pow.int_to_int here.
                    # `int_to_int` should return int but actually also returns float
                    # (PyTorch bug) so we need to avoid using the fallback execution.
                    op_overload = "int_to_int"
            elif any(is_int):
                if target.__name__ in ("add", "lt", "ge", "ne", "gt"):
                    op_overload = "float_int"
                    # put float arg first, as expected in signature
                    if arg_types[1] == float:
                        node.args = (node.args[1], node.args[0])
                else:
                    # promote int argument to float - following torch-mlir convention
                    arg0, arg1 = node.args
                    if is_int[0]:
                        if isinstance(arg0, Node):
                            prom_arg = self._promote_symbolic_scalar_int_float(
                                loc, node.graph, arg0
                            )
                            new_args = (prom_arg, arg1)
                        else:
                            arg0 = float(arg0)
                            new_args = (arg0, arg1)
                    else:
                        if isinstance(arg1, Node):
                            prom_arg = self._promote_symbolic_scalar_int_float(
                                loc, node.graph, arg1
                            )
                            new_args = (arg0, prom_arg)
                        else:
                            arg1 = float(arg1)
                            new_args = (arg0, arg1)

                    node.args = new_args
                    op_overload = "float"
            else:
                op_overload = "float"

            if target.__name__ in PY_BUILTIN_TO_TORCH_OP:
                assert op_overload in ("float", "int", "int_to_int")
                return_type = float if op_overload == "float" else int
                concrete_target = getattr(
                    PY_BUILTIN_TO_TORCH_OP.get(target.__name__), op_overload
                )
                new_node = Node(
                    graph=node.graph,
                    name=node.name,
                    op="call_function",
                    target=concrete_target,
                    args=node.args,
                    kwargs={},
                    return_type=return_type,
                )
                node.replace_all_uses_with(new_node, propagate_meta=True)
                node = new_node

            elif target == torch.sym_float:
                assert len(node.args) == 1
                assert isinstance(node.args[0], Node)
                prom_arg = self._promote_symbolic_scalar_int_float(
                    loc, node.graph, node.args[0], name=node.name
                )
                node.replace_all_uses_with(prom_arg)

                return
            else:
                torch_op = PY_BUILTIN_TO_TORCH_OP.get(target.__name__)
                assert torch_op is not None, (
                    "Unsupported builtin function for symbolic types:"
                    f" {target} with args {node.args}"
                )
                concrete_target = getattr(torch_op, op_overload)
        else:
            concrete_target = SYMBOLIC_OP_TO_TORCH_OP.get(target)

        assert concrete_target is not None, (
            f"Unable to parse symbolic operation: {target} with args {node.args}"
        )
        self._import_torch_op_overload(loc, node, concrete_target)

    def _import_hop(
        self, loc: Location, node: torch_fx.Node, hop: HigherOrderOperator
    ):
        # Imports a higher-order operator.
        # See: https://dev-discuss.pytorch.org/t/higher-order-operators-2023-10/1565
        assert hop.namespace == "higher_order"
        hop_name = hop.name()
        handler_name = f"_import_hop_{hop_name}"
        handler = getattr(self, handler_name, None)
        if handler is None:
            raise NotImplementedError(
                f"Higher-order operation '{hop_name}' not "
                "implemented in the FxImporter "
                f"(tried '{handler_name}')"
            )
        handler(loc, node, hop)

    def _import_hop_auto_functionalized(
        self, loc: Location, node: torch_fx.Node, hop: HigherOrderOperator
    ):
        # Imports the torch._higher_order_ops.auto_functionalize.auto_functionalized HOP.
        # This op wraps a target OpOverload with args/kwargs dispatched to it.
        # Even thought the OpOverload will return None, this returns the
        # arguments mutated. Note that the general op overload importing can't
        # be used here as they use a special encoding for everything.
        # See: torch/_higher_order_ops/auto_functionalize.py
        (op_overload,) = node.args
        schema = op_overload._schema
        assert isinstance(schema, FunctionSchema)
        mlir_op_name = _get_mlir_op_name_for_schema(schema)

        # Functionalization transforms the results to (*actual, *aliased).
        # If the schema is actually zero return, then the first "val"
        # type will be None and we need to bind that as a result of the node.
        # However, that doesn't make it into the IR. This special casing is
        # annoying.
        node_result_types = [
            (
                None
                if v is None
                else self._cc.tensor_metadata_to_type(
                    v, device_id=v.get_device()
                )
            )
            for v in node.meta["val"]
        ]

        if len(schema.returns) == 0:
            assert node_result_types[0] is None
            ir_result_types = node_result_types[1:]
            bind_none = 1
        else:
            ir_result_types = node_result_types
            bind_none = 0

        # The auto_functionalized ops maps all arguments by name (as opposed
        # to mixed for generic OpOverload). Linearize them.
        operands = []
        for parameter in schema.arguments:
            operand = self._import_argument(
                loc, node.kwargs[parameter.name], parameter.type
            )
            operands.append(operand)

        operation = _emit_operation(
            mlir_op_name,
            result_types=ir_result_types,
            operands=operands,
            loc=loc,
        )

        # Special case: if declared_result_types was empty, then we bind a
        # None for future node access.
        self._multi_result_nodes.add(node)
        if bind_none:
            self.bind_node_value(node, None, 0)
        # Record value mappings for remainder.
        for i, value in enumerate(operation.results):
            self.bind_node_value(node, value, i + bind_none)

    def _import_torch_op_overload(
        self, loc: Location, node: torch_fx.Node, target: TorchOpOverload
    ):
        # TODO: Convert this cascade of ifs to a table-driven
        # replace lift_fresh_copy with clone op

        if target in [
            torch.ops.aten.mul.Tensor,
            torch.ops.aten.add.Tensor,
            torch.ops.aten.div.Tensor,
            torch.ops.aten.sub.Tensor,
        ]:
            assert len(node.args) == 2
            scalar_arg = False
            args = []
            for i, a in enumerate(node.args):
                if isinstance(a, (float, int, bool)) or isinstance(
                    a.meta["val"], (torch.SymFloat, torch.SymInt, torch.SymBool)
                ):
                    scalar_arg = True
                args.append(a)

            if scalar_arg:
                node.args = tuple(args)
                target = target.overloadpacket.Scalar

        if target == torch.ops.aten.lift_fresh_copy.default:
            node.target = target = torch.ops.aten.clone.default
            node.args = (node.args[0],)
            node.kwargs = {"memory_format": None}
        elif target == torch.ops.aten.lift_fresh_copy.out:
            # TODO: It seems not possible to hit this case from user code.
            # Retaining in case if it is triggered internally somehow, but
            # it can most likely be removed once assuming full
            # functionalization in all cases.
            node.target = target = torch.ops.aten.clone.out
            node.args = (node.args[0],)
            node.kwargs = {"memory_format": None, "out": node.args[1]}
        # TODO: generalize empty.memory_format in the future
        # Currently, the aten.baddbmm.default op for Unet includes multiplying an
        # empty.memory_format input with a constant, which creates NaN values
        # because empty.memory_format contains uninitialized data. Converting
        # aten.baddbmm.default -> aten.zeros.default fixes the correctness issue
        elif target == torch.ops.aten.empty.memory_format:
            if len(node.users) == 1:
                for key_node in node.users:
                    if key_node.target == torch.ops.aten.baddbmm.default:
                        node.target = target = torch.ops.aten.zeros.default
        elif target == torch.ops.aten._local_scalar_dense.default:
            input_type = node.args[0].meta["tensor_meta"].dtype
            if input_type.is_floating_point:
                node.target = target = torch.ops.aten.Float.Tensor
            else:
                node.target = target = torch.ops.aten.Int.Tensor
            node.args = (node.args[0],)
        elif target == torch.ops.aten._assert_async.msg:
            # TODO: A more suitable op to replace it?
            return
        elif target == torch.ops.aten._unsafe_index_put.default:
            node.target = target = torch.ops.aten._unsafe_index_put.hacked_twin
        elif target == torch.ops.aten._unsafe_index.Tensor:
            node.target = target = torch.ops.aten.index.Tensor
        elif (
            target == torch.ops.aten._scaled_dot_product_flash_attention.default
        ):
            # For some reason the node meta shows nonetype for some of the results which should be int
            # We create some dummy ints here to get the correct result types
            # TODO(shaurya): maybe we can match the `schema.returns` field against the node meta
            val = []
            for v in node.meta["val"]:
                if v is None:
                    v = torch.SymInt(0)

                val.append(v)
            node.meta["val"] = tuple(val)

        schema = target._schema
        assert isinstance(schema, FunctionSchema)
        mlir_op_name = _get_mlir_op_name_for_schema(schema)

        # Intervening to use Scalar ops due to incorrect ops from AOT-autograd with scalar arguments.
        if mlir_op_name in TENSOR_SCALAR_OP_CONVERTER and (
            isinstance(node.args[1], float) or isinstance(node.args[1], int)
        ):
            mlir_op_name = TENSOR_SCALAR_OP_CONVERTER[mlir_op_name]
            # we are dynamically changing which op is emitted here due to an issue in
            # torch dynamo where it emits the Tensor variant of ops even when processing
            # scalar arguments, therefore we retrieve the schema as well so that we
            # consume the correct typing information when subsequently importing the
            # function arguments and result types
            # i.e. the code below is basically doing `schema = torch.ops.aten.my_op.Scalar._schema`
            op_attrs = mlir_op_name.split(".")
            op_overload = getattr(torch, "ops")
            for i in range(1, len(op_attrs)):
                op_overload = getattr(op_overload, op_attrs[i])
            schema = op_overload._schema

        # Unroll operands from formal parameters, args and kwargs.
        operands = []
        attributes = {}
        for i, parameter in enumerate(schema.arguments):
            # Special handling for parameters argument on Mojo custom ops
            if parameter.name == "mojo_parameters":
                # Handle parameters dict by adding contents as attributes rather than operands
                params_dict = node.kwargs.get("mojo_parameters", {})
                for param_name, param_value in params_dict.items():
                    # Convert Python values to MLIR attributes
                    if isinstance(param_value, bool):
                        attributes[param_name] = BoolAttr.get(param_value)
                    elif isinstance(param_value, int):
                        attributes[param_name] = IntegerAttr.get(
                            IndexType.get(), param_value
                        )
                    elif isinstance(param_value, float):
                        attributes[param_name] = FloatAttr.get_f64(param_value)
                    elif isinstance(param_value, str):
                        attributes[param_name] = StringAttr.get(param_value)
                    else:
                        raise ValueError(
                            f"Unsupported parameter type {type(param_value)} for {param_name}"
                        )
            else:
                if i < len(node.args):
                    operands.append(
                        self._import_argument(loc, node.args[i], parameter.type)
                    )
                elif parameter.name in node.kwargs:
                    operands.append(
                        self._import_argument(
                            loc, node.kwargs[parameter.name], parameter.type
                        )
                    )
                else:
                    operands.append(
                        self._import_default_value(
                            loc, parameter.default_value, parameter.type
                        )
                    )

        # Convert result types.
        result_types = self._unpack_node_result_types(node, schema)
        if len(result_types) > 1:
            self._multi_result_nodes.add(node)

        result_types_ = []
        for result_type in result_types:
            if isinstance(result_type, tuple):
                tuple_result_type = IrType.parse("!torch.tuple<tensor>")
                result_types_.append(tuple_result_type)
            else:
                result_types_.append(result_type)

        operation = _emit_operation(
            mlir_op_name,
            result_types=result_types_,
            operands=operands,
            loc=loc,
            attributes=attributes,
        )

        self._bind_operation_result_values(loc, node, operation, result_types)

    def _bind_node_argument(self, loc: Location, arg: torch_fx.Node):
        # If implementing boxed support for multi-result nodes, then
        # this will need to do something more intelligent.
        if arg in self._multi_result_nodes:
            raise RuntimeError("Attempt to de-reference a multi-result node")

        if arg.op == "get_attr" and (arg.target, 0) not in self._v:
            gm = arg.graph.owning_module
            assert hasattr(gm, arg.target), (
                f"Attempting to retrieve attribute '{arg.target}' from"
                " module, but no such attribute exists"
            )
            obj = getattr(gm, arg.target)
        elif arg.op == "placeholder" and (arg, 0) not in self._v:
            obj = self.fx_importer.export_meta.params_flat[
                arg.meta["static_input_index"]
            ]
        else:
            raise ValueError(f"Unsupported argument type {arg.op}")

        with loc:
            self.bind_node_value(arg, self._import_literal(obj))

    def _bind_operation_result_values(
        self,
        loc: Location,
        node: torch_fx.Node,
        operation: Operation,
        result_types: list[IrType],
    ):
        for i, (value, result_type) in enumerate(
            zip(operation.results, result_types)
        ):
            self.bind_node_value(node, value, i)

    def _import_argument(
        self, loc: Location, arg: NodeArgument, expected_jit_type=None
    ) -> Value:
        """Import an FX `Argument`, which must result to an MLIR `Value`."""
        if isinstance(arg, torch_fx.Node):
            if not self.has_node_value(arg):
                self._bind_node_argument(loc, arg)

            argument_value = self.resolve_node_value(arg)
        elif isinstance(arg, torch_fx.immutable_collections.immutable_list):
            argument_value = self._import_list_argument(
                loc, arg, expected_jit_type
            )
        elif isinstance(expected_jit_type, torch.TensorType) and not isinstance(
            arg, torch.Tensor
        ):
            # promote scalars to tensor types as appropriate
            argument_value = self._import_scalar_as_tensor(loc, arg)
        elif LITERAL_CONVERTER_MAP.lookup(type(arg)) is not None:
            with loc:
                argument_value = self._import_literal(arg)
        else:
            raise TypeError(f"Unsupported argument type {arg.__class__}")
        with loc:
            if (
                not expected_jit_type
                or argument_value.type != self._cc.torch_bool_type
            ):
                return argument_value
            if isinstance(expected_jit_type, torch.FloatType):
                return Operation.create(
                    name="torch.aten.Float.bool",
                    results=[self._cc.torch_float_type],
                    operands=[argument_value],
                ).result
            if isinstance(expected_jit_type, (torch.IntType, torch.NumberType)):
                return Operation.create(
                    name="torch.aten.Int.bool",
                    results=[self._cc.torch_int_type],
                    operands=[argument_value],
                ).result
            return argument_value

    def _import_literal(self, py_value: Any) -> Value:
        orig_value = None
        if isinstance(py_value, torch.Tensor) and py_value.dtype == torch.bool:
            orig_value = py_value
            py_value = py_value.to(torch.uint8)
        # Apply the conversion callback.
        user_value = self.fx_importer._hooks.resolve_literal(self, py_value)
        if user_value is not None:
            assert isinstance(user_value, Value)
            return user_value

        # Default conversion path.
        converter = LITERAL_CONVERTER_MAP.lookup(type(py_value))
        if converter is None:
            raise TypeError(
                "Unsupported argument -> literal conversion for"
                f" {py_value.__class__}"
            )
        result = converter(py_value, self, self._cc, self._options)
        if orig_value is None:
            return result

        # Convert the tensor element type.
        dtype = orig_value.dtype
        dtype_converter = LITERAL_CONVERTER_MAP.lookup(torch.dtype)
        return Operation.create(
            name="torch.prims.convert_element_type",
            results=[
                self._cc.get_tensor_type(
                    orig_value.size(), dtype, orig_value.get_device()
                )
            ],
            operands=[
                result,
                dtype_converter(dtype, self, self._cc, self._options),
            ],
        ).result

    def _import_input(self, py_value: Any, info: InputInfo) -> Value:
        # Try the hook.
        user_value = self.fx_importer._hooks.resolve_input(self, py_value, info)
        if user_value is not None:
            assert isinstance(user_value, Value)
            return user_value

        # Fall-back to treating as a literal if not mutating.
        if info.mutable_producer_node_name is not None:
            raise ValueError(
                f"Cannot import {info.input_spec} as a literal because it is"
                " mutable"
            )
        return self._import_literal(py_value)

    def _import_scalar_as_tensor(
        self, loc: Location, arg: NodeArgument
    ) -> Value:
        tensor_arg = torch.tensor(arg)
        result_type = self._cc.get_tensor_type(
            tensor_arg.size(), tensor_arg.dtype, tensor_arg.get_device()
        )
        with loc:
            constant_arg = LITERAL_CONVERTER_MAP.lookup(type(arg))(
                arg, self, self._cc, self._options
            )

        return Operation.create(
            name="torch.prim.NumToTensor.Scalar",
            results=[result_type],
            operands=[constant_arg],
            loc=loc,
        ).result

    def _import_list_argument(
        self, loc: Location, arg: Sequence[NodeArgument], expected_jit_type
    ) -> Value:
        assert (
            isinstance(expected_jit_type, torch.ListType)
            or (
                isinstance(expected_jit_type, torch.OptionalType)
                and isinstance(
                    expected_jit_type.getElementType(), torch.ListType
                )
            )
            or (expected_jit_type is None)
        ), (
            f"Unexpected jit type as list argument: {arg} of type"
            f" {expected_jit_type}"
        )

        # parse list type
        if expected_jit_type is None:
            element_type = type(arg[0])
        else:
            element_jit_type = expected_jit_type.getElementType()

            # this branch is needed to handle Optional[List[]] types
            if isinstance(element_jit_type, torch.ListType):
                element_jit_type = element_jit_type.getElementType()

            # this handles getting the inner types for List[Optional[]] types
            is_optional_type = isinstance(element_jit_type, torch.OptionalType)
            if is_optional_type:
                element_jit_type = element_jit_type.getElementType()
            element_type = TORCH_TYPE_TO_PY_TYPE[type(element_jit_type)]

        # create list operands
        list_operands = []

        for operand in arg:
            operand_type = type(operand)
            if isinstance(operand, Node):
                if operand in self._multi_result_nodes:
                    raise RuntimeError(
                        "Attempt to de-reference a multi-result node"
                    )
                if not self.has_node_value(operand) and (
                    operand.op == "get_attr"
                    or (
                        operand.op == "placeholder"
                        and "static_input_index" in operand.meta
                    )
                ):
                    self._bind_node_argument(loc, operand)
                val = self.resolve_node_value(operand)
                val_type = str(val.type)
                assert (
                    isinstance(element_type, str) and element_type in val_type
                ) or SCALAR_TYPE_TO_TORCH_MLIR_TYPE.get(
                    element_type
                ) == val_type, (
                    "Heterogeneous lists are not supported: expected"
                    f" {element_type}, got {val_type}"
                )
            else:
                operand_jit_type = (
                    torch.NoneType
                    if operand_type is NoneType
                    else element_jit_type
                )
                val = self._import_default_value(loc, operand, operand_jit_type)

            list_operands.append(val)

        # construct list op
        if is_optional_type:
            list_type = PY_TYPE_TO_TORCH_OPTIONAL_LIST_TYPE[element_type]
        else:
            list_type = PY_TYPE_TO_TORCH_LIST_TYPE[element_type]

        result_type = IrType.parse(list_type, context=self._c)
        operation = Operation.create(
            "torch.prim.ListConstruct",
            results=[result_type],
            operands=list_operands,
            loc=loc,
        )

        return operation.result

    def _import_default_value(
        self, loc: Location, arg, expected_jit_type
    ) -> Value:
        """Imports a defaulted value for a known function schema."""
        if isinstance(arg, list):
            return self._import_list_argument(loc, arg, expected_jit_type)

        # The LITERAL_CONVERTER_MAP maps each arg to its respective constant
        # of the expected jit IR type (types like torch.dtype will form a chain of
        # maps to get to constant of expected_jit_type).
        converter = LITERAL_CONVERTER_MAP.lookup(type(arg))
        if converter is None:
            raise RuntimeError(
                f"Unhandled default value ({arg.__class__}): {arg})"
            )
        with loc:
            return converter(arg, self, self._cc, self._options)

    def _unpack_node_result_types(
        self, node: torch.fx.Node, schema: FunctionSchema
    ) -> list[IrType]:
        return_count = len(schema.returns)

        if return_count == 1:
            # Unary return directly maps a single meta["val"] and cannot be subscripted.
            # if "tensor_meta" is None, this will throw unsupported placeholder node error
            result_types = [self._cc.node_val_to_type(node)]
        elif return_count == 0:
            # Some torch ops do have 0 returns, and these are supported with ZeroResults
            # op trait. Python bindings for IR creation allow us to pass empty result_types
            # for such ops. Therefore, we pass an empty result types for these cases.
            result_types = []
        else:
            # Multi-return will unpack the meta["val"] and trigger our getitem subscripting
            # short-circuit above. Note that if we ever choose to also fully reify Python
            # level result tuples, we will need to create a tuple-boxed version of this and
            # redirect to it for generic object access.
            result_types = []
            for v in node.meta["val"]:
                result_types.append(self._cc.value_info_to_type(v))

        return result_types


def _make_constant_op(
    op_name: str, value_attr: Attribute, result_type: Optional[IrType] = None
) -> Operation:
    return Operation.create(
        op_name,
        results=[result_type if result_type else value_attr.type],
        attributes={"value": value_attr},
    )


def _create_mlir_tensor_type(dtype: torch.dtype, size: torch.Size) -> IrType:
    try:
        element_type = TORCH_DTYPE_TO_MLIR_TYPE[dtype]()
        tensor_type = RankedTensorType.get(size, element_type)
        return tensor_type
    except KeyError:
        raise TypeError(f"Could not map Torch dtype {dtype} to an MLIR type")


def create_mlir_tensor_type(tensor: torch.Tensor) -> IrType:
    return _create_mlir_tensor_type(tensor.dtype, tensor.size())


def tensor_to_memoryview(tensor: torch.Tensor) -> memoryview:
    if not tensor.is_contiguous():
        raise ValueError("Tried converting non contiguous tensor to memoryview")
    ptr = tensor.data_ptr()
    size = tensor.numel() * tensor.element_size()
    buffer = (ctypes.c_byte * size).from_address(ptr)
    return memoryview(buffer)


def get_bytes(
    tensor: torch.Tensor, force_cpu: bool
) -> Union[np.ndarray, memoryview]:
    """Returns a memory view of the underlying data of the pointer.

    We assume the tensor must be contiguous.
    """
    with maybe_disable_fake_tensor_mode():
        if force_cpu:
            # Copy the tensor to CPU for debugging and view as raw bytes so
            # bfloat16 is not a problem.
            cpu_tensor = tensor.cpu()
            if cpu_tensor.dtype == torch.bfloat16:
                cpu_tensor = cpu_tensor.view(torch.uint16)
            np_tensor = cpu_tensor.numpy()
            if np_tensor.base is not None:
                # Ensure we have a contiguous copy, not just a view.
                # We need a raw buffer of data in order to create an ElementsAttr for the invocation of torch.tensor.literal.
                np_tensor = np_tensor.copy()
            return np_tensor
        else:
            # The literal tensors are ensured to be contiguous from our torch.compile backend.
            return tensor_to_memoryview(tensor)


def _make_tensor_literal_op(
    tensor: torch.Tensor,
    result_type: IrType,
    py_attr_tracker: "RefTracker",
    force_cpu=False,
) -> Operation:
    mapping = py_attr_tracker.track(tensor)
    if mapping.is_empty:
        # check support for bfloat16
        assert not (tensor.dtype == torch.bfloat16 and ml_dtypes is None), (
            "torch.bfloat16 requires the ml_dtypes package, please run:\n\npip"
            " install ml_dtypes\n"
        )
        # Resolve the attribute.
        npy_dtype = TORCH_DTYPE_TO_NPY_TYPE.get(tensor.dtype)
        assert npy_dtype is not None, (
            "Can not create literal tensor for unsupported datatype:"
            f" {tensor.dtype}"
        )

        # One element constants are more optimizable as splat DenseElementsAttr. DenseResourceElementsAttr does not
        # support splats, so don't use it for that case. In addition, at the time of writing, it has bugs with handling
        # 0d tensors.
        externalize = False
        if tensor.numel() == 1 and tensor.get_device() == -1:
            try:
                dtype = tensor.dtype
                element_type = TORCH_DTYPE_TO_MLIR_TYPE[dtype]()
            except KeyError:
                raise TypeError(
                    f"Could not map Torch dtype {dtype} to an MLIR type"
                )
            elements_attr = DenseElementsAttr.get(
                type=element_type,
                array=get_bytes(tensor, force_cpu),
                shape=tensor.shape,
            )
        else:
            tensor_type = create_mlir_tensor_type(tensor)
            shape_desc = "_".join([str(d) for d in tensor.shape])
            blob_name = f"torch_tensor_{shape_desc}_{str(tensor.dtype)}"
            if hasattr(tensor, WEIGHTS_REGISTRY_ATTR):
                blob_name = getattr(tensor, WEIGHTS_REGISTRY_ATTR)
                externalize = True
                bytes = get_bytes(tensor, force_cpu)
            else:
                # We will depend on the DenseResourceElementsAttr to store
                # the proper data. This requires data to be on CPU.
                bytes = get_bytes(tensor, True)

            elements_attr = DenseResourceElementsAttr.get_from_buffer(
                bytes,
                blob_name,
                tensor_type,
            )
        mapping.value = elements_attr
        mapping.externalize = externalize
    else:
        elements_attr = mapping.value
        externalize = mapping.externalize

    attributes = {
        "value": elements_attr,
        "externalize": BoolAttr.get(externalize),
    }
    if (device_id := tensor.get_device()) is not None:
        # TODO(PT-644): Multi-device support, currently only supports `gpu:0`.
        attributes["device"] = StringAttr.get(
            "cpu" if device_id == -1 else "gpu:0"
        )
    return Operation.create(
        name="torch.tensor.literal",
        results=[result_type],
        attributes=attributes,
    )


################################################################################
# TypeSubclassMapping
################################################################################


class TypeSubclassMap:
    """Mapping of super-types to values.

    Maintains a cache of actual types seen and uses that instead of a linear
    scan.
    """

    __slots__ = [
        "_cache",
        "_mapping",
    ]

    def __init__(self):
        # The linear list of converters.
        self._mapping: list[tuple[type, Any]] = []
        # When there is a hit on the linear mapping, memoize it here.
        self._cache: dict[type, Any] = {}

    def map(self, t: type, value: Any):
        self._mapping.append((t, value))
        self._cache[t] = value

    def lookup(self, t: type) -> Any:
        try:
            return self._cache[t]
        except KeyError:
            pass
        for t_super, value in self._mapping:
            if issubclass(t, t_super):
                self._cache[t] = value
                return value
        else:
            self._cache[t] = None
            return None


###############################################################################
# Utilities
###############################################################################


def _get_mlir_op_name_for_schema(schema: FunctionSchema) -> str:
    # Returns a fully-qualified MLIR operation name (i.e. 'torch.foobar')
    # for a function schema.
    namespace, sep, unqualified_name = schema.name.partition("::")
    assert sep, f"Malformed Torch op name {schema.name}"
    mlir_op_name = f"torch.{namespace}.{unqualified_name}"
    if schema.overload_name != "":
        mlir_op_name += f".{schema.overload_name}"
    return mlir_op_name


def _emit_operation(
    mlir_op_name: str,
    result_types: list[IrType],
    operands: list[Value],
    loc: Location,
    attributes: dict[str, Attribute] = {},
) -> Operation:
    # Support unregistered torch ops using torch.operator.
    # torch.operator is used to represent ops from registry
    # which haven't been generated by torch_ods_gen.py.
    context = loc.context
    if not context.is_registered_operation(mlir_op_name):
        # mlir_op_name here looks like 'torch.aten.relu'.
        # When we create a torch.operator, we need to remove the 'torch.'
        # prefix - the first dot in the name is used to split namespace from
        # the opname, and we want "aten::relu" here, and not "torch::aten.relu"
        op_name = mlir_op_name.removeprefix("torch.")
        operation = Operation.create(
            "torch.operator",
            attributes=attributes | {"name": StringAttr.get(op_name)},
            results=result_types,
            operands=operands,
            loc=loc,
        )
    else:
        operation = Operation.create(
            mlir_op_name,
            results=result_types,
            operands=operands,
            loc=loc,
        )
    return operation


###############################################################################
# Reference mapping
###############################################################################


# Opaque value to indicate something is empty. Used in cases where 'None'
# may have a different meaning.
class EmptyType: ...


Empty = EmptyType()


class RefMapping:
    __slots__ = [
        "_referrent",
        "value",
        "externalize",
    ]

    def __init__(self, referrent: Any):
        if referrent is not Empty:
            self._referrent = weakref.ref(referrent)
        self.value = Empty
        self.externalize = False

    @property
    def is_empty(self):
        return self.value is Empty

    @property
    def is_externalized(self):
        return self.externalize

    def __repr__(self):
        return (
            "<RefMapping"
            f" {id(self._referrent) if self._referrent is not Empty else 'empty'} ->"
            f" ({self.value if self.value is not Empty else 'empty'},"
            f" 'externalize:' {self.externalize})>"
        )


class RefTracker:
    """Tracks live references from Python values to symbolic associations."""

    def __init__(self):
        self._refs: dict[int, RefMapping] = {}

    def track(self, referrent: Any) -> RefMapping:
        ref_id = id(referrent)
        existing = self._refs.get(ref_id)
        if existing:
            return existing
        info = RefMapping(referrent)
        if referrent is not Empty:
            weakref.finalize(referrent, self._ref_finalizer, ref_id)
        self._refs[ref_id] = info
        return info

    def _ref_finalizer(self, ref_id: int):
        del self._refs[ref_id]


################################################################################
# Mappings
################################################################################

LITERAL_CONVERTER_MAP = TypeSubclassMap()
LITERAL_CONVERTER_MAP.map(
    NoneType,
    lambda arg, gni, cc, options: Operation.create(
        "torch.constant.none", results=[cc.torch_none_type]
    ).result,
)
LITERAL_CONVERTER_MAP.map(
    bool,
    lambda arg, gni, cc, options: _make_constant_op(
        "torch.constant.bool", cc.integer_attr(arg, 1), cc.torch_bool_type
    ).result,
)
LITERAL_CONVERTER_MAP.map(
    int,
    lambda arg, gni, cc, options: _make_constant_op(
        "torch.constant.int", cc.integer_attr(arg, 64), cc.torch_int_type
    ).result,
)
LITERAL_CONVERTER_MAP.map(
    float,
    lambda arg, gni, cc, options: _make_constant_op(
        "torch.constant.float", FloatAttr.get_f64(arg), cc.torch_float_type
    ).result,
)
LITERAL_CONVERTER_MAP.map(
    str,
    lambda arg, gni, cc, options: _make_constant_op(
        "torch.constant.str", StringAttr.get(arg), cc.torch_str_type
    ).result,
)
LITERAL_CONVERTER_MAP.map(
    torch.Tensor,
    lambda arg, gni, cc, options: _make_tensor_literal_op(
        arg,
        cc.get_tensor_type(arg.size(), arg.dtype, arg.get_device()),
        cc._py_attr_tracker,
        options.get("force_cpu_dense_resource", False),
    ).result,
)
LITERAL_CONVERTER_MAP.map(
    torch.device,
    lambda arg, gni, cc, options: _make_constant_op(
        "torch.constant.device", StringAttr.get(str(arg)), cc.torch_device_type
    ).result,
)
LITERAL_CONVERTER_MAP.map(
    torch.dtype,
    lambda arg, gni, cc, options: LITERAL_CONVERTER_MAP.lookup(int)(
        TORCH_DTYPE_TO_INT[arg], gni, cc, options
    ),
)
LITERAL_CONVERTER_MAP.map(
    torch.layout,
    lambda arg, gni, cc, options: LITERAL_CONVERTER_MAP.lookup(int)(
        TORCH_LAYOUT_TO_INT[arg], gni, cc, options
    ),
)
LITERAL_CONVERTER_MAP.map(
    torch.memory_format,
    lambda arg, gni, cc, options: LITERAL_CONVERTER_MAP.lookup(int)(
        TORCH_MEMORY_FORMAT_TO_INT[arg], gni, cc, options
    ),
)

TORCH_TYPE_TO_PY_TYPE = {
    torch.IntType: int,
    torch.FloatType: float,
    torch.StringType: str,
    torch.BoolType: bool,
    torch.TensorType: "tensor",
}

PY_TYPE_TO_TORCH_LIST_TYPE = {
    int: "!torch.list<int>",
    float: "!torch.list<float>",
    str: "!torch.list<str>",
    bool: "!torch.list<bool>",
    "tensor": "!torch.list<tensor>",
    "vtensor": "!torch.list<vtensor>",
    "any": "!torch.list<any>",
}

PY_TYPE_TO_TORCH_OPTIONAL_LIST_TYPE = {
    int: "!torch.list<optional<int>>",
    float: "!torch.list<optional<float>>",
    str: "!torch.list<optional<str>>",
    bool: "!torch.list<optional<bool>>",
    "tensor": "!torch.list<optional<tensor>>",
    "vtensor": "!torch.list<optional<vtensor>>",
    "any": "!torch.list<optional<any>>",
}

SCALAR_TYPE_TO_TORCH_MLIR_TYPE = {
    torch.SymInt: "!torch.int",
    torch.SymFloat: "!torch.float",
    torch.SymBool: "!torch.bool",
    int: "!torch.int",
    float: "!torch.float",
    str: "!torch.str",
    bool: "!torch.bool",
    NoneType: "!torch.none",
}


# AOT-autograd sometimes falsely emit tensor version op with scalar arguments.
# We may remove this dictionary, if we fix such behavior in the backend.
TENSOR_SCALAR_OP_CONVERTER = {
    "torch.aten.mul.Tensor": "torch.aten.mul.Scalar",
    "torch.aten.div.Tensor": "torch.aten.div.Scalar",
    "torch.aten.add.Tensor": "torch.aten.add.Scalar",
    "torch.aten.sub.Tensor": "torch.aten.sub.Scalar",
    "torch.aten.floor_divide": "torch.aten.floor_divide.Scalar",
}
