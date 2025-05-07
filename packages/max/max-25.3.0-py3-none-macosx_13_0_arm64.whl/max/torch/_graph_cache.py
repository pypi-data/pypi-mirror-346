# ===----------------------------------------------------------------------=== #
#
# This file is Modular Inc proprietary.
#
# ===----------------------------------------------------------------------=== #

import logging
import os
import pickle
from collections.abc import Sequence
from copy import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Union

from max import engine
from max._torch_mlir.torch_api_compat import (
    _IS_TORCH_2_6_OR_LATER,
    dynamo_timed_wrapper,
    maybe_disable_fake_tensor_mode,
)

import torch  # type: ignore
from torch._inductor import config  # type: ignore
from torch._inductor.codecache import (  # type: ignore
    BypassFxGraphCache,
    FxGraphCache,
    compiled_fx_graph_hash,
    sha256_hash,
    write_atomic,
)

if _IS_TORCH_2_6_OR_LATER:
    from torch._inductor.output_code import CompiledFxGraph  # type: ignore
else:
    from torch._inductor.codecache import CompiledFxGraph

from torch._inductor.graph import GraphLowering  # type: ignore
from torch._subclasses.fake_tensor import FakeTensor  # type: ignore
from torch.fx.experimental.symbolic_shapes import hint_int  # type: ignore

from ._core import ModularCompiledFxGraphImpl

log = logging.getLogger(__name__)


@dataclass
class ModularCompiledFxGraph(CompiledFxGraph):
    def __init__(
        self,
        gm: torch.fx.GraphModule,
        example_inputs: list[Union[torch.SymInt, FakeTensor]],
        input_specs: list[Any],
        is_output_scalar: list[bool],
        model_handle: Any,
        fwd_input_indices: list[int],
        options: Optional[dict] = None,
        stats_report: Optional[dict] = None,
    ):
        graph = GraphLowering(gm, example_inputs)
        self.model_handle = model_handle
        self.fwd_input_indices = fwd_input_indices
        self.input_specs = input_specs
        self.is_output_scalar = is_output_scalar
        self.options = {} if options is None else options
        self.stats_report = {} if stats_report is None else stats_report
        self.impl: Optional[ModularCompiledFxGraphImpl] = (
            ModularCompiledFxGraphImpl(self.model_handle)
        )

        super_kwargs: dict[str, Any] = dict()
        super_kwargs["current_callable"] = None
        super_kwargs["graph"] = graph
        super_kwargs["output_strides"] = None
        super_kwargs["disabled_cudagraphs_reason"] = None
        super_kwargs["metrics_deltas"] = None
        super_kwargs["counter_deltas"] = None
        if _IS_TORCH_2_6_OR_LATER:
            super_kwargs["gm"] = gm
            super_kwargs["cudagraphs"] = None
            super_kwargs["example_inputs"] = example_inputs
            super_kwargs["static_input_idxs"] = None
            super_kwargs["inputs_to_check"] = None
            super_kwargs["boxed_forward_device_index"] = None
            super_kwargs["fx_kwargs"] = None

        super().__init__(**super_kwargs)

    def __call__(self, *args) -> Any:
        if self.fwd_input_indices is not None:
            args = tuple([args[i] for i in self.fwd_input_indices])

        if impl := self.impl:
            results = impl(*args)
        else:
            raise (ValueError("ModularCompiledFxGraphImpl is not initialized."))
        return tuple(
            r.item()
            if isinstance(r, torch.Tensor) and self.is_output_scalar[i]
            else r
            for i, r in enumerate(results)
        )


class ModularFxGraphCache(FxGraphCache):
    """
    Supports caching and reusing compiled Fx graphs.

    The overall strategy is as follows:
    - This cache stores entries on disk. When saving an entry, we can't
      serialize the max engine model handle or the callable. We export the
      model as a mef artifact and pickle metadata necessary to reconstruct the
      callable.
    - For indexing the cache, we gather the fields relevant to identifying an
      FxGraph (the graph module, graph inputs, system settings etc.) into an
      FxGraphCacheDetails object, pickle it, and compute a hash for the key.
      See FxGraphCachePickler.
    - Among the metadata we store, we also include a guards expression that's
      appropriate for validating any symbols for Tensor arguments that have
      symbolic bounds. On cache lookup then, we evaluate those guards in the
      current context to validate that a cached entry can be served.
    - A given graph could have multiple compiled versions, corresponding to
      different sets of guards. Therefore, we store cache entries in the form:
          <temp dir>/<fx graph hash>/<serialized metatdata>
    - On lookup, we compute the key from the graph details, iterate over all
      leaf files in the corresponding subdirectory, deserialize the entry, and
      evaluate its guards expression. If the evaluation succeeds, we have a
      cache hit. If it fails, we compile the graph and store a new entry.
    - Finally, on a cache hit, we need to make sure any guards that would
      have been created during compilation are added to the current context.
    """

    @staticmethod
    def _lookup_graph(
        key: str, example_inputs: list[torch.Tensor]
    ) -> Optional[tuple[CompiledFxGraph, Path]]:
        """
        Lookup a compiled graph in the cache by key.
        Returns the deserialized CompiledFxGraph object and MEF path on hit, None on miss.
        """
        shape_env = FxGraphCache._get_shape_env()
        if shape_env is None:
            return None

        symints = FxGraphCache._filter_backed_symints(example_inputs)
        hints = [hint_int(s) for s in symints]

        subdir = FxGraphCache._get_tmp_dir_for_key(key)
        if not os.path.exists(subdir):
            return None

        mef_paths = list(Path(subdir).glob("*.mef"))
        if len(mef_paths) != 1:
            raise ValueError("Found more than one .mef file in artifact dir")
        mef_path = mef_paths[0]

        graph = None
        for path in sorted(os.listdir(subdir)):
            if path.endswith(".mef"):
                continue

            try:
                with open(os.path.join(subdir, path), "rb") as f:
                    graph = pickle.load(f)
            except Exception:
                log.warning(
                    "fx graph cache unable to load compiled graph",
                    exc_info=True,
                )
                continue

            if graph is None:
                continue

            if graph.guards_expr:
                hit = bool(
                    shape_env.evaluate_guards_expression(
                        graph.guards_expr, hints
                    )
                )
                log.debug(
                    (
                        "fx graph cache key %s evaluating guards [%s] with"
                        " values %s => hit=%s"
                    ),
                    key,
                    graph.guards_expr,
                    hints,
                    hit,
                )
                if not hit:
                    continue

                check = bool(
                    shape_env.evaluate_guards_expression(
                        graph.guards_expr, symints
                    )
                )
                log.debug(
                    (
                        "fx graph cache key %s evaluating guards [%s] with"
                        " values %s => hit=%s (post-load)"
                    ),
                    key,
                    graph.guards_expr,
                    symints,
                    check,
                )
                if not check:
                    continue

                log.debug(
                    "fx graph cache key %s post-load guards: %s",
                    key,
                    shape_env.guards,
                )

            return graph, mef_path

        return None

    @staticmethod
    @dynamo_timed_wrapper(phase_name="save_cached_model")
    def save(
        key: str,
        example_inputs: list[torch.Tensor],
        fx_kwargs: dict[str, Any],
        inputs_to_check: Sequence[int],
        compiled_graph: ModularCompiledFxGraph,
    ):
        """
        Store a serialized CompiledFxGraph on disk.
        """
        disk_compiled_graph = copy(compiled_graph)

        # We don't serialize the callable or the model_handle but export the mef separately
        disk_compiled_graph.current_callable = None
        model_handle = disk_compiled_graph.model_handle
        disk_compiled_graph.model_handle = None
        disk_compiled_graph.impl = None

        # Before serializing, compute the guard expression that will be used to
        # ensure that a CompiledFxGraph is valid when loaded from the cache. It's
        # sufficient to consider only the SymInt args to the fx graph since the
        # Tensor shapes are already captured in the hash for the cache key. Any
        # Tensor arg with a symbolic shape will have a SymInt arg for the graph.
        shape_env = FxGraphCache._get_shape_env()
        assert shape_env is not None
        symints = FxGraphCache._filter_backed_symints(example_inputs)
        guards = shape_env.get_pruned_guards(symints)
        disk_compiled_graph.guards_expr = shape_env.produce_guards_expression(
            placeholders=symints, guards=guards
        )

        try:
            content = pickle.dumps(disk_compiled_graph)
        except Exception:
            log.warning(
                "fx graph cache unable to serialize compiled graph",
                exc_info=True,
            )
            return

        try:
            subdir = FxGraphCache._get_tmp_dir_for_key(key)
            if not os.path.exists(subdir):
                os.makedirs(subdir, exist_ok=True)

            # Use a hash of the serialized CompiledFxGraph to get a unique file
            # name. The specific name doesn't matter since a lookup involves
            # iterating over all entries in the parent subdir.
            compiled_fx_hash = sha256_hash(content)
            fx_path = os.path.join(subdir, compiled_fx_hash)
            write_atomic(fx_path, content, make_dirs=True)

            mef_path = os.path.splitext(fx_path)[0] + ".mef"
            model_handle._export_mef(mef_path)
        except Exception:
            log.warning("fx graph unable to write to cache", exc_info=True)

    @staticmethod
    def _check_can_cache(gm: torch.fx.GraphModule):
        """
        Check some conditions that would preclude caching and raise BypassFxGraphCache
        to bypass in case caching is not possible.
        """
        # Freezing can embed constants that wouldn't be static across runs. We
        # pass them through the weights registry so they will not be embedded.
        if config.aot_inductor.use_runtime_constant_folding:
            log.debug("fx graph caching disabled when constant folding enabled")
            raise BypassFxGraphCache

        # The treatment of guards in the caching implementation requires that
        # we have a shape env.
        if FxGraphCache._get_shape_env() is None:
            log.debug("fx graph cache no shape env")
            raise BypassFxGraphCache

        # HigherOrderOperators should be handled on a case-by-case basis.
        # Currently, we just skip caching if we have any.
        # We also skip if there are any torchbind objects.
        for node in gm.graph.nodes:
            if isinstance(node.target, torch._ops.HigherOrderOperator):
                log.debug("fx graph caching skipped due to HOP node")
                raise BypassFxGraphCache
            if node.op == "getattr" and isinstance(
                getattr(gm, node.target), torch._C.ScriptObject
            ):
                log.debug(
                    "fx graph caching skipped due to script object target"
                )
                raise BypassFxGraphCache

    @staticmethod
    @dynamo_timed_wrapper(phase_name="load_cached_model")
    def load(
        inference_session: engine.InferenceSession,
        gm: torch.fx.GraphModule,
        example_inputs: list[torch.Tensor],
        weights_registry: dict[str, Any],
        fx_kwargs: dict[str, Any],
        inputs_to_check: Sequence[int],
    ) -> Optional[ModularCompiledFxGraph]:
        """
        Load a compiled graph from the cache. Returns None if not found in cache
        """
        compiled_graph = None
        try:
            ModularFxGraphCache._check_can_cache(gm)
            key = compiled_fx_graph_hash(
                gm, example_inputs, fx_kwargs, inputs_to_check
            )[0]

            result = ModularFxGraphCache._lookup_graph(key, example_inputs)
            if result is None:
                log.debug("fx graph cache miss for key %s", key)
            else:
                log.debug("fx graph cache hit for key %s", key)
                compiled_graph, mef_path = result
                with maybe_disable_fake_tensor_mode():
                    compiled_graph.model_handle = inference_session.load(
                        mef_path,
                        input_specs=compiled_graph.input_specs,
                        weights_registry=weights_registry,
                    )
                    compiled_graph.impl = ModularCompiledFxGraphImpl(
                        compiled_graph.model_handle
                    )

        except BypassFxGraphCache:
            pass

        return compiled_graph
