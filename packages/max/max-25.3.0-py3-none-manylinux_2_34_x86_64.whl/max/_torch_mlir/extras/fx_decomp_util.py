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
#   Path:   python/torch_mlir/extras/fx_decomp_util.py
#
# ===----------------------------------------------------------------------=== #
import torch
from torch._decomp import get_decompositions

# default decompositions pulled from SHARK / torch._decomp
DEFAULT_DECOMPOSITIONS = [
    torch.ops.aten.split_with_sizes,
    torch.ops.aten.gelu,
]


def get_decomposition_table():
    return get_decompositions(DEFAULT_DECOMPOSITIONS)
