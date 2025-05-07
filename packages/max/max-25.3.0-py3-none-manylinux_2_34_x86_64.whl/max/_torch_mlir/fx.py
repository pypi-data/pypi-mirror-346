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
#   Path:   python/torch_mlir/fx.py
#
# ===----------------------------------------------------------------------=== #

# Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# Also available under a BSD-style license. See LICENSE.

from typing import Optional

from max._torch_mlir import ir
from max._torch_mlir.dialects import torch as torch_d
from max._torch_mlir.extras.fx_importer import (
    ExportMeta,
    FxImporter,
    FxImporterHooks,
    Opaque,  # noqa
)
from torch.fx import GraphModule


def export_and_import(
    graph_module: GraphModule,
    *args,
    fx_importer: Optional[FxImporter] = None,
    hooks: Optional[FxImporterHooks] = None,
    func_name: str = "main",
    export_meta: ExportMeta = None,
    options: dict = {},
    **kwargs,
):
    context = ir.Context()
    torch_d.register_dialects(context)

    if fx_importer is None:
        fx_importer = FxImporter(
            context=context, hooks=hooks, export_meta=export_meta
        )

    _, is_output_scalar = fx_importer.import_stateless_graph(
        graph_module, func_name=func_name, options=options
    )
    return fx_importer.module, is_output_scalar
