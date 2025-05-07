# ===----------------------------------------------------------------------=== #
#
# This file is Modular Inc proprietary.
#
# ===----------------------------------------------------------------------=== #

from collections.abc import Mapping, Sequence
from typing import Any, TypeVar

import numpy

import torch  # type: ignore


def _is_root_fallback(op_str: str) -> bool:
    """A heuristic to determine if an op is causing cascading fallbacks.

    Note that both the current implementation's "parsing" logic and the
    heuristic itself are crude, but it is good at finding ops that we don't have
    the lowering for and cause a cascade of fallbacks.
    """

    op_str = op_str.rsplit(")", maxsplit=1)[0]  # Drop attributes.

    SKIP_LIST = [
        "tensor_static_info_cast",
        "to_tensor",
        "to_vtensor",
        "forward",
        "literal",
        "constant",
        "return",
    ]

    if "tensor" not in op_str or any(skip in op_str for skip in SKIP_LIST):
        return False

    # NOTE: If any of the types are signatures or anything other than basic or
    # known torch types, this will probably fail.
    op_name, signature = op_str.split("(", maxsplit=1)
    args, results = signature.split(") -> (")

    def missing_dtype_or_shape(types: str) -> bool:
        # NOTE: This takes a list of types as a single string.
        return any(
            "tensor" in t and ("<[" not in t or "unk" in t)
            for t in types.split(", ")
        )

    # If the arguments all have dtype/shape, but any result is missing it, we
    # mark it as a root fallback.
    return not missing_dtype_or_shape(args) and missing_dtype_or_shape(results)


def print_fallback_log(log: str):
    """Print the fallback telemetry log, including root fallbacks (if any)."""
    root_fallbacks: list[str] = []
    print()
    for line in (l.strip() for l in log.splitlines()):
        if not line:
            continue
        if line == "--------------------------------------":
            break
        print(line)

        # If the line starts with a numeric value, this is a fallback op entry.
        if line[0].isnumeric():
            num_instance, op_str = line.split(maxsplit=1)
            if _is_root_fallback(op_str):
                root_fallbacks.append(op_str)

    if root_fallbacks:
        print("ROOT FALLBACKS")
        for op_str in sorted(root_fallbacks):
            print(op_str)


def is_iterable_of_tensors(iterable, include_empty=False):
    """Returns True if iterable is an iterable of tensors and False otherwise.

    If the iterable is empty, the return value is :attr:`include_empty`
    """
    # Tensor itself is iterable so we check this first
    if isinstance(iterable, torch.Tensor):
        return False

    try:
        if len(iterable) == 0:
            return include_empty

        for t in iter(iterable):
            if not isinstance(t, torch.Tensor):
                return False
    except TypeError:
        return False

    return True


_T = TypeVar("_T", Sequence[Any], dict[str, Any])


def clone(args: _T) -> _T:
    """Clone the given collection of arguments.

    Args:
        args: The collection of arguments to clone, either a list or a
        dictionary of keyword arguments.

    Returns:
        The cloned collection of arguments.
    """

    def clone_arg(v: Any) -> Any:
        if isinstance(v, torch.Tensor):
            return v.detach().clone().contiguous()
        if is_iterable_of_tensors(v):
            return [t.detach().clone().contiguous() for t in v]
        return v

    if isinstance(args, (list, tuple)):
        return type(args)(clone_arg(v) for v in args)
    elif isinstance(args, Mapping):
        return {k: clone_arg(v) for k, v in args.items()}  # type: ignore
    else:
        raise ValueError(f"Unsupported argument type: {type(args)}")


def compare(
    ref_results: Any,
    exp_results: Any,
    rtol=1e-4,
    atol=1e-4,
    device=None,
):
    """Verify that experimental results match reference results.
    The function checks that the result structures and primitive values are the
    same and the corresponding tensors are close to each other within the
    specified tolerance.
    """

    def results_are_instances_of(*types):
        return isinstance(ref_results, types) and isinstance(exp_results, types)

    if ref_results is None and exp_results is None:
        return True
    if results_are_instances_of(str, int, bool):
        return ref_results == exp_results
    if results_are_instances_of(float):
        return torch.allclose(
            torch.tensor(ref_results),
            torch.tensor(exp_results),
            rtol=rtol,
            atol=atol,
            equal_nan=True,
        )
    if results_are_instances_of(torch.Tensor):
        return (
            ref_results.shape == exp_results.shape
            and ref_results.device == exp_results.device
            and torch.allclose(
                ref_results.to(
                    device=ref_results.device if device is None else device
                ),
                exp_results.to(
                    device=ref_results.device if device is None else device
                ),
                rtol=rtol,
                atol=atol,
                equal_nan=True,
            )
        )
    if results_are_instances_of(numpy.ndarray):
        return ref_results.shape == exp_results.shape and numpy.allclose(
            ref_results, exp_results, rtol=rtol, atol=atol, equal_nan=True
        )
    if results_are_instances_of(list, tuple) and (
        len(ref_results) == len(exp_results)
    ):
        return all(
            compare(ref_i, exp_i, rtol=rtol, atol=atol)
            for ref_i, exp_i in zip(ref_results, exp_results)
        )
    if results_are_instances_of(dict) and (
        set(ref_results.keys()) == set(exp_results.keys())
    ):
        return all(
            compare(ref_i, exp_results[key], rtol=rtol, atol=atol)
            for key, ref_i in ref_results.items()
        )
    return False


def get_max_rtol_atol(
    ref_results: Any, exp_results: Any
) -> tuple[float, float]:
    """Return the maximum observed relative and absolute tolerances."""

    def compute_rtol_atol(
        a: torch.Tensor, b: torch.Tensor
    ) -> tuple[float, float]:
        absolute_diff = torch.abs(a.float() - b.float())
        # Add small epsilon to avoid division by zero.
        relative_diff = absolute_diff / (torch.abs(b.float()) + 1e-12)
        return torch.max(relative_diff).item(), torch.max(absolute_diff).item()

    def results_are_instances_of(*types):
        return isinstance(ref_results, types) and isinstance(exp_results, types)

    if results_are_instances_of(float):
        rtol, atol = compute_rtol_atol(
            torch.tensor(ref_results), torch.tensor(exp_results)
        )
    elif results_are_instances_of(torch.Tensor):
        rtol, atol = compute_rtol_atol(ref_results, exp_results)
    elif results_are_instances_of(numpy.ndarray):
        rtol, atol = compute_rtol_atol(
            torch.from_numpy(ref_results), torch.from_numpy(exp_results)
        )
    elif results_are_instances_of(list, tuple) and (
        len(ref_results) == len(exp_results)
    ):
        rtol, atol = 0.0, 0.0
        for ref_i, exp_i in zip(ref_results, exp_results):
            new_rtol, new_atol = get_max_rtol_atol(ref_i, exp_i)
            rtol, atol = max(rtol, new_rtol), max(atol, new_atol)
    elif results_are_instances_of(dict) and (
        set(ref_results.keys()) == set(exp_results.keys())
    ):
        rtol, atol = 0.0, 0.0
        for key, ref_i in ref_results.items():
            new_rtol, new_atol = get_max_rtol_atol(ref_i, exp_results[key])
            rtol, atol = max(rtol, new_rtol), max(atol, new_atol)
    else:
        return 0.0, 0.0

    return max(0.0, rtol), max(0.0, atol)


def to_torch_value(value: Any) -> Any:
    """Traverses a python data structure containing `numpy.ndarray` leaf nodes
    and converts the `numpy.ndarray`s to `torch.tensor`s.

    The function supports nested lists, dictionaries, and tuples.
    """
    if isinstance(value, numpy.ndarray):
        return torch.from_numpy(value)
    if isinstance(value, list):
        return [to_torch_value(v) for v in value]
    if isinstance(value, dict):
        return {to_torch_value(k): to_torch_value(v) for k, v in value.items()}
    if isinstance(value, tuple):
        return tuple(to_torch_value(v) for v in value)
    return value
