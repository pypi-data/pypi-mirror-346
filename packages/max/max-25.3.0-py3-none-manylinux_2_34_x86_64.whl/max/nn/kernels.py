# ===----------------------------------------------------------------------=== #
# Copyright (c) 2025, Modular Inc. All rights reserved.
#
# Licensed under the Apache License v2.0 with LLVM Exceptions:
# https://llvm.org/LICENSE.txt
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===----------------------------------------------------------------------=== #
"""Helper functions for wrapping custom kv cache/attention related ops."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, cast

import numpy as np
from max.dtype import DType
from max.graph import (
    DeviceRef,
    Dim,
    TensorType,
    TensorValue,
    TensorValueLike,
    ops,
)
from max.graph.ops.quantized import repack_gguf_quantized_weights
from max.graph.quantization import QuantizationConfig, QuantizationEncoding

from .kv_cache import (
    ContinuousBatchingKVCacheCollection,
    KVCacheParams,
    KVCacheStrategy,
    PagedKVCacheCollection,
    PagedKVCacheCollectionFA3Fallback,
)


def fused_qkv_ragged_matmul(
    kv_params: KVCacheParams,
    input: TensorValue,
    input_row_offsets: TensorValue,
    wqkv: TensorValue,
    kv_collection: ContinuousBatchingKVCacheCollection | PagedKVCacheCollection,
    layer_idx: TensorValue,
    n_heads: int,
    bias: TensorValue | None = None,
) -> TensorValue:
    """Computes fused query, key, and value projections with ragged input.

    `input` and `input_row_offsets` are used together to implement the ragged
    tensor.
    `input_row_offsets` indicates where each batch starts and ends in `input`

    Raises:
        ValueError: on input shapes/dtypes that are invalid for the kernel.
    """
    if input.dtype != wqkv.dtype:
        msg = (
            "expected input and wqkv to have the same dtype, but got"
            f" {input.dtype} and {wqkv.dtype}, respectively."
        )
        raise ValueError(msg)

    input_rank_expected = 2
    if input.rank != input_rank_expected:
        msg = f"expected input to have rank {input_rank_expected}, was {input.rank}"
        raise ValueError(msg)

    if input_row_offsets.dtype != DType.uint32:
        msg = (
            "expected input_row_offsets to have dtype uint32, was"
            f" {input_row_offsets.dtype}"
        )
        raise ValueError(msg)

    if layer_idx.dtype != DType.uint32:
        msg = f"expected layer_idx to have dtype uint32, was {layer_idx.dtype}"
        raise ValueError(msg)

    if kv_params.cache_strategy not in {
        KVCacheStrategy.CONTINUOUS,
        KVCacheStrategy.PAGED,
        KVCacheStrategy.PAGED_FA3_FALLBACK,
    }:
        msg = f"unsupported cache strategy for fused_qkv_ragged_matmul: {kv_params.cache_strategy}"
        raise ValueError(msg)

    parameters: dict[str, int | str | DType] = {
        "num_heads": kv_params.n_kv_heads_per_device,
        "head_dim": kv_params.head_dim,
    }
    if kv_params.cache_strategy in {
        KVCacheStrategy.PAGED,
        KVCacheStrategy.PAGED_FA3_FALLBACK,
    }:
        assert kv_params.page_size is not None
        parameters["page_size"] = int(kv_params.page_size)

    cache_strategy_str = kv_params.cache_strategy.kernel_substring()

    if bias:
        op_name = f"mo.fused_qkv_matmul.ragged.{cache_strategy_str}.bias"

        return ops.inplace_custom(
            op_name,
            values=[
                input,
                input_row_offsets,
                wqkv,
                kv_collection,
                layer_idx,
                bias,
            ],
            out_types=[
                TensorType(
                    dtype=input.dtype,
                    shape=input.shape[:-1] + [n_heads * kv_params.head_dim],
                    device=input.device,
                )
            ],
            parameters=parameters,
        )[0].tensor

    op_name = f"mo.fused_qkv_matmul.ragged.{cache_strategy_str}"

    return ops.inplace_custom(
        op_name,
        values=[input, input_row_offsets, wqkv, kv_collection, layer_idx],
        out_types=[
            TensorType(
                dtype=input.dtype,
                shape=input.shape[:-1] + [n_heads * kv_params.head_dim],
                device=input.device,
            )
        ],
        parameters=parameters,
    )[0].tensor


def unfused_qkv_ragged_matmul_gguf_quantized(
    kv_params: KVCacheParams,
    input: TensorValue,
    input_row_offsets: TensorValue,
    n_heads: int,
    q_weight: TensorValue,
    k_weight: TensorValue,
    v_weight: TensorValue,
    quantization_encoding_q: QuantizationEncoding,
    quantization_encoding_k: QuantizationEncoding,
    quantization_encoding_v: QuantizationEncoding,
    kv_collection: ContinuousBatchingKVCacheCollection | PagedKVCacheCollection,
    layer_idx: TensorValue,
) -> TensorValue:
    """Computes fused query, key, and value projections with ragged input and
    quantized weight matrices. A `quantization_config` must be provided.

    `input` and `input_row_offsets` are used together to implement the ragged
    tensor.
    `input_row_offsets` indicates where each batch starts and ends in `input`

    Raises:
        ValueError: on input shapes/dtypes that are invalid for the kernel.
    """

    input_rank_expected = 2
    if input.rank != input_rank_expected:
        msg = f"expected input to have rank {input_rank_expected}, was {input.rank}"
        raise ValueError(msg)

    if input.dtype != DType.float32:
        msg = f"expected input to have dtype float32, was {input.dtype}"
        raise ValueError(msg)

    if input_row_offsets.dtype != DType.uint32:
        msg = (
            "expected input_row_offsets to have dtype uint32, was"
            f" {input_row_offsets.dtype}"
        )
        raise ValueError(msg)

    if layer_idx.dtype != DType.uint32:
        msg = f"expected layer_idx to have dtype uint32, was {layer_idx.dtype}"
        raise ValueError(msg)

    if kv_params.cache_strategy not in {
        KVCacheStrategy.CONTINUOUS,
    }:
        msg = f"unsupported cache strategy for fused_qkv_ragged_matmul: {kv_params.cache_strategy}"
        raise ValueError(msg)

    if (
        not quantization_encoding_q.is_gguf
        or not quantization_encoding_k.is_gguf
        or not quantization_encoding_v.is_gguf
    ):
        raise ValueError(
            f"expected quantization_encoding_q, quantization_encoding_k, and quantization_encoding_v to be gguf, was {quantization_encoding_q}, {quantization_encoding_k}, and {quantization_encoding_v}"
        )

    parameters: dict[str, int | str | DType] = {
        "num_heads": kv_params.n_kv_heads_per_device,
        "head_dim": kv_params.head_dim,
        "quantization_encoding_q": quantization_encoding_q.name,
        "quantization_encoding_k": quantization_encoding_k.name,
        "quantization_encoding_v": quantization_encoding_v.name,
    }

    cache_strategy_str = kv_params.cache_strategy.kernel_substring()
    return ops.inplace_custom(
        name=f"mo.unfused_qkv_matmul.ragged.{cache_strategy_str}.gguf_quantized",
        values=[
            input,
            input_row_offsets,
            repack_gguf_quantized_weights(q_weight, quantization_encoding_q),
            repack_gguf_quantized_weights(k_weight, quantization_encoding_k),
            repack_gguf_quantized_weights(v_weight, quantization_encoding_v),
            kv_collection,
            layer_idx,
        ],
        out_types=[
            TensorType(
                dtype=input.dtype,
                shape=input.shape[:-1] + [n_heads * kv_params.head_dim],
                device=input.device,
            )
        ],
        parameters=parameters,
    )[0].tensor


def fused_qkv_ragged_matmul_quantized(
    kv_params: KVCacheParams,
    input: TensorValue,
    input_row_offsets: TensorValue,
    wqkv: TensorValue,
    kv_collection: ContinuousBatchingKVCacheCollection | PagedKVCacheCollection,
    layer_idx: TensorValue,
    n_heads: int,
    quantization_config: QuantizationConfig,
    perm_idx: TensorValue | None = None,
    bias: TensorValue | None = None,
) -> TensorValue:
    """Computes fused query, key, and value projections with ragged input and
    quantized weight matrices. A `quantization_config` must be provided.

    `input` and `input_row_offsets` are used together to implement the ragged
    tensor.
    `input_row_offsets` indicates where each batch starts and ends in `input`

    Raises:
        ValueError: on input shapes/dtypes that are invalid for the kernel.
    """

    input_rank_expected = 2
    if input.rank != input_rank_expected:
        msg = f"expected input to have rank {input_rank_expected}, was {input.rank}"
        raise ValueError(msg)

    if input_row_offsets.dtype != DType.uint32:
        msg = (
            "expected input_row_offsets to have dtype uint32, was"
            f" {input_row_offsets.dtype}"
        )
        raise ValueError(msg)

    if layer_idx.dtype != DType.uint32:
        msg = f"expected layer_idx to have dtype uint32, was {layer_idx.dtype}"
        raise ValueError(msg)

    if kv_params.cache_strategy not in {
        KVCacheStrategy.CONTINUOUS,
        KVCacheStrategy.PAGED,
    }:
        msg = f"unsupported cache strategy for fused_qkv_ragged_matmul: {kv_params.cache_strategy}"
        raise ValueError(msg)

    # In the group-wise quantization scheme, every `group_size` quantized weights
    # share the same scale. If `has_zp` is `True`, there is also a group-wise zero
    # point that need to be substracted from the quantized weights.
    # Since the new extensibility API doesn't currently support `bool` type parameters,
    # we pass `has_zp` as an interger (`has_zp_int`).
    # For GPTQ, `has_zp_int` will always be 0.
    parameters: dict[str, int | str | DType] = {
        "num_heads": kv_params.n_kv_heads_per_device,
        "head_dim": kv_params.head_dim,
        "group_size": quantization_config.group_size,
        "has_zp_int": 0,
    }
    if perm_idx:
        input = ops.gather(input, TensorValue(perm_idx), axis=1)
        perm_idx = perm_idx.to(input.type.device or DeviceRef.CPU())
        wqkv = ops.custom(
            "GPTQ_gpu_repack_b4_g128_desc_act",
            list((wqkv, perm_idx)),
            out_types=[
                TensorType(
                    DType.uint8,
                    ((wqkv.shape[1], wqkv.shape[0])),
                    device=input.type.device or DeviceRef.CPU(),
                )
            ],
        )[0].tensor
    else:
        wqkv = ops.custom(
            "GPTQ_gpu_repack_b4_g128",
            list((wqkv,)),
            out_types=[
                TensorType(
                    DType.uint8,
                    ((wqkv.shape[1], wqkv.shape[0])),
                    device=input.type.device or DeviceRef.CPU(),
                )
            ],
        )[0].tensor

    if kv_params.cache_strategy == KVCacheStrategy.PAGED:
        assert kv_params.page_size is not None
        parameters["page_size"] = int(kv_params.page_size)

    cache_strategy_str = kv_params.cache_strategy.kernel_substring()

    args = [input, input_row_offsets, wqkv, kv_collection, layer_idx]
    if bias:
        args.append(bias)
        bias_name_str = "bias."
    else:
        bias_name_str = ""

    op_name = f"mo.fused_qkv_matmul.ragged.{cache_strategy_str}.{bias_name_str}quantized"

    return ops.inplace_custom(
        op_name,
        values=args,
        out_types=[
            TensorType(
                dtype=input.dtype,
                shape=input.shape[:-1] + [n_heads * kv_params.head_dim],
                device=input.device,
            )
        ],
        parameters=parameters,
    )[0].tensor


def fused_qkv_matmul(
    kv_params: KVCacheParams,
    input: TensorValue,
    wqkv: TensorValue,
    kv_collection: ContinuousBatchingKVCacheCollection,
    layer_idx: TensorValue,
    n_heads: int,
) -> TensorValue:
    """Computes fused query, key and value projections."""
    if input.dtype != wqkv.dtype:
        msg = (
            "expected input and wqkv to have the same dtype, but got"
            f" {input.dtype} and {wqkv.dtype}, respectively."
        )
        raise ValueError(msg)

    input_rank_expected = 3
    if input.rank != input_rank_expected:
        msg = f"expected input to have rank {input_rank_expected}, was {input.rank}"
        raise ValueError(msg)

    wqkv_rank_expected = 2
    if wqkv.rank != wqkv_rank_expected:
        msg = (
            f"expected wqkv to have rank {wqkv_rank_expected}, was {wqkv.rank}"
        )
        raise ValueError(msg)

    if layer_idx.dtype != DType.uint32:
        msg = f"expected layer_idx to have dtype uint32, was {layer_idx.dtype}"
        raise ValueError(msg)

    if kv_params.cache_strategy != KVCacheStrategy.CONTINUOUS:
        msg = f"unsupported cache strategy for fused_qkv_matmul: {kv_params.cache_strategy}"
        raise ValueError(msg)

    cache_strategy_str = kv_params.cache_strategy.kernel_substring()
    op_name = f"mo.fused_qkv_matmul.padded.{cache_strategy_str}"

    return ops.inplace_custom(
        op_name,
        values=[input, wqkv, kv_collection, layer_idx],
        out_types=[
            TensorType(
                dtype=input.dtype,
                shape=input.shape[:-1] + [n_heads * kv_params.head_dim],
                device=input.device,
            )
        ],
        parameters={
            "num_heads": kv_params.n_kv_heads_per_device,
            "head_dim": kv_params.head_dim,
        },
    )[0].tensor


def matmul_kv_cache_ragged(
    kv_params: KVCacheParams,
    hidden_states: TensorValue,
    input_row_offsets: TensorValue,
    weight: TensorValue,
    kv_collection: ContinuousBatchingKVCacheCollection,
    layer_idx: int | np.integer,
) -> None:
    """Computes key and value projections with ragged input.

    `hidden_states` and `input_row_offsets` are used together to
    implement the ragged tensor.
    `input_row_offsets` indicates where each batch starts and ends in `input`
    """
    if hidden_states.dtype != weight.dtype:
        msg = (
            "expected hidden_states and weight to have the same dtype, but got"
            f" {hidden_states.dtype} and {weight.dtype}, respectively."
        )
        raise ValueError(msg)

    hidden_states_rank_expected = 2
    if hidden_states.rank != hidden_states_rank_expected:
        msg = (
            "expected hidden_states to have rank "
            f"{hidden_states_rank_expected}, was {hidden_states.rank}"
        )
        raise ValueError(msg)

    if input_row_offsets.dtype != DType.uint32:
        msg = (
            "expected input_row_offsets to have dtype uint32, was"
            f" {input_row_offsets.dtype}"
        )
        raise ValueError(msg)

    if kv_params.cache_strategy != KVCacheStrategy.CONTINUOUS:
        msg = f"unsupported cache strategy for matmul_kv_cache_ragged: {kv_params.cache_strategy}"
        raise ValueError(msg)

    parameters: dict[str, int | str | DType] = {
        "num_heads": kv_params.n_kv_heads_per_device,
        "head_dim": kv_params.head_dim,
    }
    if kv_params.cache_strategy == KVCacheStrategy.PAGED:
        assert kv_params.page_size is not None
        parameters["page_size"] = kv_params.page_size

    cache_strategy_str = kv_params.cache_strategy.kernel_substring()
    op_name = f"mo.kv_matmul.ragged.{cache_strategy_str}"

    ops.inplace_custom(
        name=op_name,
        values=[
            hidden_states,
            input_row_offsets,
            weight,
            kv_collection,
            ops.constant(layer_idx, DType.uint32, device=DeviceRef.CPU()),
        ],
        parameters=parameters,
    )


def matmul_k_cache_ragged(
    kv_params: KVCacheParams,
    hidden_states: TensorValue,
    input_row_offsets: TensorValue,
    weight: TensorValue,
    kv_collection: PagedKVCacheCollection,
    layer_idx: int | np.integer,
) -> None:
    """Computes key projections with ragged input.

    `hidden_states` and `input_row_offsets` are used together to
    implement the ragged tensor.
    `input_row_offsets` indicates where each batch starts and ends in `input`
    """
    if hidden_states.dtype != weight.dtype:
        msg = (
            "expected hidden_states and weight to have the same dtype, but got"
            f" {hidden_states.dtype} and {weight.dtype}, respectively."
        )
        raise ValueError(msg)

    hidden_states_rank_expected = 2
    if hidden_states.rank != hidden_states_rank_expected:
        msg = (
            "expected hidden_states to have rank "
            f"{hidden_states_rank_expected}, was {hidden_states.rank}"
        )
        raise ValueError(msg)

    if input_row_offsets.dtype != DType.uint32:
        msg = (
            "expected input_row_offsets to have dtype uint32, was"
            f" {input_row_offsets.dtype}"
        )
        raise ValueError(msg)

    if kv_params.cache_strategy != KVCacheStrategy.PAGED:
        msg = f"unsupported cache strategy for matmul_kv_cache_ragged: {kv_params.cache_strategy}"
        raise ValueError(msg)

    parameters: dict[str, int | str | DType] = {
        "num_heads": kv_params.n_kv_heads_per_device,
        "head_dim": kv_params.head_dim,
    }
    if kv_params.cache_strategy == KVCacheStrategy.PAGED:
        assert kv_params.page_size is not None
        parameters["page_size"] = kv_params.page_size

    cache_strategy_str = kv_params.cache_strategy.kernel_substring()
    op_name = f"mo.k_matmul.ragged.{cache_strategy_str}"

    ops.inplace_custom(
        name=op_name,
        values=[
            hidden_states,
            input_row_offsets,
            weight,
            kv_collection,
            ops.constant(layer_idx, DType.uint32, device=DeviceRef.CPU()),
        ],
        parameters=parameters,
    )


def fused_qk_ragged_rope(
    kv_params: KVCacheParams,
    input: TensorValue,
    input_row_offsets: TensorValue,
    kv_collection: ContinuousBatchingKVCacheCollection | PagedKVCacheCollection,
    freqs_cis: TensorValue,
    layer_idx: TensorValue,
    interleaved: bool = True,
) -> TensorValue:
    """Computes fused query-key attention with rotary positional encodings and ragged inputs.

    Args:
        input: [batch_size * seq_len, n_heads, head_dim]
        input_row_offsets:
        freqs_cis: tensor of shape (max_seq_len * 2, head_dim)
        layer_idx:
        interleaved:

    `input` and `input_row_offsets` are used together to implement the ragged tensor.
    `input_row_offsets` indicates where each batch starts and ends in `input`
    """

    if input.dtype != freqs_cis.dtype:
        msg = (
            "expected input and freqs_cis to share a dtype, but got"
            f" {input.dtype} and {freqs_cis.dtype} respectively"
        )
        raise ValueError(msg)

    if input_row_offsets.dtype != DType.uint32:
        msg = (
            "expected input_row_offsets to have dtype uint32, was"
            f" {input_row_offsets.dtype}"
        )

    if layer_idx.dtype != DType.uint32:
        msg = f"expected layer_idx to have dtype uint32, was {layer_idx.dtype}"
        raise ValueError(msg)

    if kv_params.cache_strategy not in {
        KVCacheStrategy.CONTINUOUS,
        KVCacheStrategy.PAGED,
        KVCacheStrategy.PAGED_FA3_FALLBACK,
    }:
        msg = f"unsupported cache strategy for fused_qk_ragged_rope: {kv_params.cache_strategy}"
        raise ValueError(msg)

    parameters: dict[str, bool | int | str | DType] = {
        "num_heads": kv_params.n_kv_heads_per_device,
        "head_dim": kv_params.head_dim,
        "interleaved": interleaved,
    }
    if kv_params.cache_strategy in {
        KVCacheStrategy.PAGED,
        KVCacheStrategy.PAGED_FA3_FALLBACK,
    }:
        assert kv_params.page_size is not None
        parameters["page_size"] = kv_params.page_size

    cache_strategy_str = kv_params.cache_strategy.kernel_substring()
    op_name = f"mo.fused_qk_rope.ragged.{cache_strategy_str}"

    return ops.inplace_custom(
        op_name,
        values=[input, input_row_offsets, kv_collection, freqs_cis, layer_idx],
        out_types=[
            TensorType(
                dtype=input.dtype, shape=input.shape, device=input.device
            )
        ],
        parameters=parameters,
    )[0].tensor


def fused_qk_rope(
    kv_params: KVCacheParams,
    input: TensorValue,
    kv_collection: ContinuousBatchingKVCacheCollection,
    freqs_cis_2d: TensorValue,
    layer_idx: TensorValue,
    interleaved: bool = True,
) -> TensorValue:
    """Computes fused query-key attention with rotary positional encodings."""
    input_rank_expected = 4
    if input.rank != input_rank_expected:
        msg = (
            f"expected input of rank {input_rank_expected} but got {input.rank}"
        )
        raise ValueError(msg)

    freqs_cis_rank_expected = 2
    if freqs_cis_2d.rank != freqs_cis_rank_expected:
        msg = (
            f"expected freqs_cis_2d of rank {freqs_cis_rank_expected} but got "
            f"{freqs_cis_2d.rank}"
        )
        raise ValueError(msg)

    if layer_idx.dtype != DType.uint32:
        msg = f"expected uint32 layer_idx but got {layer_idx.dtype}"
        raise ValueError(msg)

    if kv_params.cache_strategy != KVCacheStrategy.CONTINUOUS:
        msg = f"unsupported cache strategy for fused_qk_rope: {kv_params.cache_strategy}"
        raise ValueError(msg)

    parameters: dict[str, bool | int | str | DType] = {
        "num_heads": kv_params.n_kv_heads_per_device,
        "head_dim": kv_params.head_dim,
        "interleaved": interleaved,
    }
    if kv_params.cache_strategy == KVCacheStrategy.PAGED:
        assert kv_params.page_size is not None
        parameters["page_size"] = kv_params.page_size

    cache_strategy_str = kv_params.cache_strategy.kernel_substring()
    op_name = f"mo.fused_qk_rope.padded.{cache_strategy_str}"

    return ops.inplace_custom(
        op_name,
        values=[input, kv_collection, freqs_cis_2d, layer_idx],
        out_types=[
            TensorType(
                dtype=input.dtype, shape=input.shape, device=input.device
            )
        ],
        parameters=parameters,
    )[0].tensor


def flash_attention(
    kv_params: KVCacheParams,
    input: TensorValue,
    kv_collection: ContinuousBatchingKVCacheCollection,
    layer_idx: TensorValue,
    attention_mask: TensorValue,
    valid_lengths: TensorValue,
    scale: float,
) -> TensorValue:
    """Computes flash attention provided the mo.opaque KV Cache."""
    input_rank_expected = 4
    if input.rank != input_rank_expected:
        msg = (
            f"expected input of rank {input_rank_expected} but got {input.rank}"
        )
        raise ValueError(msg)

    if layer_idx.dtype != DType.uint32:
        msg = f"expected uint32 layer_idx but got {layer_idx.dtype}"
        raise ValueError(msg)

    if attention_mask.dtype != input.dtype:
        msg = (
            f"expected attention mask dtype {attention_mask.dtype} to match "
            f"the input's dtype {input.dtype}"
        )
        raise ValueError(msg)

    if valid_lengths.dtype != DType.uint32:
        msg = f"expected uint32 valid_lengths but got {valid_lengths.dtype}"
        raise ValueError(msg)

    if kv_params.cache_strategy != KVCacheStrategy.CONTINUOUS:
        msg = f"unsupported cache strategy for flash_attention: {kv_params.cache_strategy}"
        raise ValueError(msg)

    cache_strategy_str = kv_params.cache_strategy.kernel_substring()
    op_name = f"mo.mha.padded.{cache_strategy_str}.tensor_mask.no_pos"

    return ops.inplace_custom(
        op_name,
        values=[
            input,
            kv_collection,
            layer_idx,
            attention_mask,
            valid_lengths,
            # NOTE: The scale argument to the flash attention kernel is
            # constrained to float32.
            ops.constant(scale, dtype=DType.float32, device=DeviceRef.CPU()),
        ],
        out_types=[
            TensorType(
                dtype=input.dtype, shape=input.shape, device=input.device
            )
        ],
        parameters={
            "num_heads": kv_params.n_kv_heads_per_device,
            "head_dim": kv_params.head_dim,
        },
    )[0].tensor


def flash_attention_with_causal_mask(
    kv_params: KVCacheParams,
    input: TensorValue,
    kv_collection: ContinuousBatchingKVCacheCollection,
    layer_idx: TensorValue,
    valid_lengths: TensorValue,
    scale: float,
) -> TensorValue:
    """Computes flash attention provided the mo.opaque KV Cache.
    Notably, materializes the causal mask within the kernel."""

    if input.shape[0] != valid_lengths.shape[0]:
        msg = (
            "expected batch size of input, to equal length of valid_lengths"
            f" got batch size of input ({input.shape[0]}), length of"
            f" valid_lengths ({valid_lengths.shape[0]})"
        )
        raise ValueError(msg)

    if input.dtype != kv_params.dtype:
        msg = (
            f"expected input to be dtype: {kv_params.dtype}, got {input.dtype}"
        )
        raise ValueError(msg)

    if layer_idx.dtype != DType.uint32:
        msg = f"expected uint32 layer_idx but got {layer_idx.dtype}"
        raise ValueError(msg)

    if valid_lengths.dtype != DType.uint32:
        msg = f"expected uint32 valid_lengths but got {valid_lengths.dtype}"
        raise ValueError(msg)

    if kv_params.cache_strategy != KVCacheStrategy.CONTINUOUS:
        msg = f"unsupported cache strategy for flash_attention_with_causal_mask: {kv_params.cache_strategy}"
        raise ValueError(msg)

    cache_strategy_str = kv_params.cache_strategy.kernel_substring()
    op_name = f"mo.mha.padded.{cache_strategy_str}.causal_mask.no_pos"

    return ops.inplace_custom(
        op_name,
        values=[
            input,
            kv_collection,
            layer_idx,
            valid_lengths,
            # NOTE: The scale argument to flash attention is constrained to float32.
            ops.constant(scale, dtype=DType.float32, device=DeviceRef.CPU()),
        ],
        out_types=[
            TensorType(
                dtype=input.dtype, shape=input.shape, device=input.device
            )
        ],
        parameters={
            "num_heads": kv_params.n_kv_heads_per_device,
            "head_dim": kv_params.head_dim,
        },
    )[0].tensor


@dataclass
class MHAMaskConfig:
    attention_mask_variant: AttentionMaskVariant
    positional_encoding_variant: PositionalEncodingVariant


class AttentionMaskVariant(str, Enum):
    NULL_MASK = "null_mask"
    CAUSAL_MASK = "causal_mask"
    TENSOR_MASK = "tensor_mask"
    CHUNKED_CAUSAL_MASK = "chunked_causal_mask"
    SLIDING_WINDOW_CAUSAL_MASK = "sliding_window_causal_mask"


class PositionalEncodingVariant(str, Enum):
    NO_POS = "no_pos"
    ALIBI_POS = "alibi_pos"


class MHAMaskVariant(str, Enum):
    CAUSAL_MASK = 0
    CAUSAL_ALIBI_MASK = 1
    NULL_MASK = 2
    CHUNKED_CAUSAL_MASK = 3
    SLIDING_WINDOW_CAUSAL_MASK = 4


_MHA_MASK_CONFIG_DICT = {
    MHAMaskVariant.CAUSAL_MASK: MHAMaskConfig(
        attention_mask_variant=AttentionMaskVariant.CAUSAL_MASK,
        positional_encoding_variant=PositionalEncodingVariant.NO_POS,
    ),
    MHAMaskVariant.CAUSAL_ALIBI_MASK: MHAMaskConfig(
        attention_mask_variant=AttentionMaskVariant.CAUSAL_MASK,
        positional_encoding_variant=PositionalEncodingVariant.ALIBI_POS,
    ),
    MHAMaskVariant.NULL_MASK: MHAMaskConfig(
        attention_mask_variant=AttentionMaskVariant.NULL_MASK,
        positional_encoding_variant=PositionalEncodingVariant.NO_POS,
    ),
    MHAMaskVariant.CHUNKED_CAUSAL_MASK: MHAMaskConfig(
        attention_mask_variant=AttentionMaskVariant.CHUNKED_CAUSAL_MASK,
        positional_encoding_variant=PositionalEncodingVariant.NO_POS,
    ),
    MHAMaskVariant.SLIDING_WINDOW_CAUSAL_MASK: MHAMaskConfig(
        attention_mask_variant=AttentionMaskVariant.SLIDING_WINDOW_CAUSAL_MASK,
        positional_encoding_variant=PositionalEncodingVariant.NO_POS,
    ),
}


def flash_attention_ragged_paged_fa3_fallback(
    kv_params: KVCacheParams,
    input: TensorValue,
    input_row_offsets: TensorValue,
    kv_collection: PagedKVCacheCollectionFA3Fallback,
    context_lengths: TensorValue,
    layer_idx: TensorValue,
) -> TensorValue:
    """Computes flash attention provided the `!mo.opaque` KV Cache. using the FA3 fallback kernel."""
    input_rank_expected = 3
    if input.rank != input_rank_expected:
        msg = (
            f"expected input of rank {input_rank_expected} but got {input.rank}"
        )
        raise ValueError(msg)

    if input.dtype != kv_params.dtype:
        msg = (
            f"expected input to be dtype: {kv_params.dtype}, got {input.dtype}"
        )
        raise ValueError(msg)

    if layer_idx.dtype != DType.uint32:
        msg = f"expected uint32 layer_idx but got {layer_idx.dtype}"
        raise ValueError(msg)

    if input_row_offsets.dtype != DType.uint32:
        msg = f"expected uint32 input_row_offsets but got {input_row_offsets.dtype}"
        raise ValueError(msg)

    # TODO(austin): remove this cast.
    input_row_offsets_cast = input_row_offsets.cast(DType.int32)
    assert kv_params.page_size is not None, (
        "Expected page size to be set for PAGED_FA3_FALLBACK"
    )
    parameters: dict[str, int | str | DType] = {
        "num_heads": kv_params.n_kv_heads_per_device,
        "head_dim": kv_params.head_dim,
        "page_size": kv_params.page_size,
    }
    context_lengths_cast = context_lengths.cast(DType.int32)

    op_name = "mo.mha.ragged.paged_fa3_fallback.causal_mask.no_pos"
    return ops.inplace_custom(
        op_name,
        values=[
            input,
            input_row_offsets_cast,
            context_lengths_cast,
            kv_collection,
            layer_idx,
        ],
        out_types=[
            TensorType(
                dtype=input.dtype, shape=input.shape, device=input.device
            )
        ],
        parameters=parameters,
        device=input.device,
    )[0].tensor


def flash_attention_ragged(
    kv_params: KVCacheParams,
    input: TensorValue,
    input_row_offsets: TensorValue,
    kv_collection: ContinuousBatchingKVCacheCollection
    | PagedKVCacheCollection
    | PagedKVCacheCollectionFA3Fallback,
    layer_idx: TensorValue,
    mask_variant: MHAMaskVariant,
    scale: float,
    context_lengths: Optional[TensorValue] = None,
    local_window_size: int = 8192,
) -> TensorValue:
    """Computes flash (self) attention provided the `!mo.opaque` KV Cache.

    Notably, this materializes the attention mask (dependent on MHAMaskVariant)
    within the kernel.
    `input` and `input_row_offsets` are used together to implement the ragged
    tensor.
    `input_row_offsets` indicates where each batch starts and ends in `input`

    Note that this is self attention and the KV sequence length is
    assumed to be equal to the Q sequence length.
    For KV sequence length != Q sequence length, use `cross_attention_ragged`.
    """
    if kv_params.cache_strategy == KVCacheStrategy.PAGED_FA3_FALLBACK:
        assert context_lengths is not None, (
            "context_lengths must be provided for PAGED_FA3_FALLBACK"
        )
        return flash_attention_ragged_paged_fa3_fallback(
            kv_params,
            input,
            input_row_offsets,
            cast(PagedKVCacheCollectionFA3Fallback, kv_collection),
            context_lengths,
            layer_idx,
        )
    input_rank_expected = 3
    if input.rank != input_rank_expected:
        msg = (
            f"expected input of rank {input_rank_expected} but got {input.rank}"
        )
        raise ValueError(msg)

    if input.dtype != kv_params.dtype:
        msg = (
            f"expected input to be dtype: {kv_params.dtype}, got {input.dtype}"
        )
        raise ValueError(msg)

    if layer_idx.dtype != DType.uint32:
        msg = f"expected uint32 layer_idx but got {layer_idx.dtype}"
        raise ValueError(msg)

    if input_row_offsets.dtype != DType.uint32:
        msg = f"expected uint32 input_row_offsets but got {input_row_offsets.dtype}"
        raise ValueError(msg)

    if kv_params.cache_strategy not in {
        KVCacheStrategy.CONTINUOUS,
        KVCacheStrategy.PAGED,
    }:
        msg = f"unsupported cache strategy for flash_attention_ragged: {kv_params.cache_strategy}"
        raise ValueError(msg)

    parameters: dict[str, int | str | DType] = {
        "num_heads": kv_params.n_kv_heads_per_device,
        "head_dim": kv_params.head_dim,
    }
    if kv_params.cache_strategy == KVCacheStrategy.PAGED:
        assert kv_params.page_size is not None
        parameters["page_size"] = kv_params.page_size

    if (
        mask_variant == MHAMaskVariant.CHUNKED_CAUSAL_MASK
        or mask_variant == MHAMaskVariant.SLIDING_WINDOW_CAUSAL_MASK
    ):
        parameters["local_window_size"] = local_window_size

    cache_strategy_str = kv_params.cache_strategy.kernel_substring()
    mha_mask_config = _MHA_MASK_CONFIG_DICT[mask_variant]
    op_name = f"mo.mha.ragged.{cache_strategy_str}.{str(mha_mask_config.attention_mask_variant.value)}.{str(mha_mask_config.positional_encoding_variant.value)}"

    return ops.inplace_custom(
        op_name,
        values=[
            input,
            input_row_offsets,
            kv_collection,
            layer_idx,
            # NOTE: The scale argument to flash attention is constrained to float32.
            ops.constant(scale, dtype=DType.float32, device=DeviceRef.CPU()),
        ],
        out_types=[
            TensorType(
                dtype=input.dtype, shape=input.shape, device=input.device
            )
        ],
        parameters=parameters,
    )[0].tensor


def flare_mla_decode_ragged(
    kv_params: KVCacheParams,
    input: TensorValue,
    input_row_offsets: TensorValue,
    kv_collection: PagedKVCacheCollection,
    layer_idx: TensorValue,
    mask_variant: MHAMaskVariant,
    scale: float,
    qk_rope_dim: int = 64,
) -> TensorValue:
    """Computes flash (self) attention provided the `!mo.opaque` KV Cache.

    Notably, this materializes the attention mask (dependent on MHAMaskVariant)
    within the kernel.
    `input` and `input_row_offsets` are used together to implement the ragged
    tensor.
    `input_row_offsets` indicates where each batch starts and ends in `input`

    Note that this is self attention and the KV sequence length is
    assumed to be equal to the Q sequence length.
    For KV sequence length != Q sequence length, use `cross_attention_ragged`.
    """
    input_rank_expected = 3
    if input.rank != input_rank_expected:
        msg = (
            f"expected input of rank {input_rank_expected} but got {input.rank}"
        )
        raise ValueError(msg)

    if input.dtype != kv_params.dtype:
        msg = (
            f"expected input to be dtype: {kv_params.dtype}, got {input.dtype}"
        )
        raise ValueError(msg)

    if layer_idx.dtype != DType.uint32:
        msg = f"expected uint32 layer_idx but got {layer_idx.dtype}"
        raise ValueError(msg)

    if input_row_offsets.dtype != DType.uint32:
        msg = f"expected uint32 input_row_offsets but got {input_row_offsets.dtype}"
        raise ValueError(msg)

    if kv_params.cache_strategy is not KVCacheStrategy.PAGED:
        msg = f"unsupported cache strategy for flash_attention_ragged: {kv_params.cache_strategy}"
        raise ValueError(msg)

    assert kv_params.page_size is not None
    parameters: dict[str, int | str | DType] = {
        "num_heads": kv_params.n_kv_heads_per_device,
        "head_dim": kv_params.head_dim,
        "page_size": kv_params.page_size,
    }

    mha_mask_config = _MHA_MASK_CONFIG_DICT[mask_variant]
    op_name = f"mo.mla.decode.ragged.paged.{str(mha_mask_config.attention_mask_variant.value)}.{str(mha_mask_config.positional_encoding_variant.value)}"

    return ops.inplace_custom(
        op_name,
        values=[
            input,
            input_row_offsets,
            kv_collection,
            layer_idx,
            # NOTE: The scale argument to flash attention is constrained to float32.
            ops.constant(scale, dtype=DType.float32, device=DeviceRef.CPU()),
        ],
        out_types=[
            TensorType(
                dtype=input.dtype,
                shape=[
                    input.shape[0],
                    input.shape[1],
                    input.shape[2] - qk_rope_dim,
                ],
                device=input.device,
            )
        ],
        parameters=parameters,
    )[0].tensor


def flare_mla_prefill_ragged(
    kv_params: KVCacheParams,
    input: TensorValue,
    k: TensorValue,
    v: TensorValue,
    input_row_offsets: TensorValue,
    buffer_row_offsets: TensorValue,
    cache_offsets: TensorValue,
    kv_collection: PagedKVCacheCollection,
    layer_idx: TensorValue,
    mask_variant: MHAMaskVariant,
    scale: float,
    qk_rope_dim: int = 64,
) -> TensorValue:
    """Performs MLA prefill."""
    input_rank_expected = 3
    if input.rank != input_rank_expected:
        msg = (
            f"expected input of rank {input_rank_expected} but got {input.rank}"
        )
        raise ValueError(msg)

    if input.dtype != kv_params.dtype:
        msg = (
            f"expected input to be dtype: {kv_params.dtype}, got {input.dtype}"
        )
        raise ValueError(msg)

    if layer_idx.dtype != DType.uint32:
        msg = f"expected uint32 layer_idx but got {layer_idx.dtype}"
        raise ValueError(msg)

    if input_row_offsets.dtype != DType.uint32:
        msg = f"expected uint32 input_row_offsets but got {input_row_offsets.dtype}"
        raise ValueError(msg)

    if kv_params.cache_strategy is not KVCacheStrategy.PAGED:
        msg = f"unsupported cache strategy for flare_mla_prefill_ragged: {kv_params.cache_strategy}"
        raise ValueError(msg)

    assert kv_params.page_size is not None
    parameters: dict[str, int | str | DType] = {
        "num_heads": kv_params.n_kv_heads_per_device,
        "head_dim": kv_params.head_dim,
        "page_size": kv_params.page_size,
    }

    mha_mask_config = _MHA_MASK_CONFIG_DICT[mask_variant]
    op_name = f"mo.mla.prefill.ragged.paged.{str(mha_mask_config.attention_mask_variant.value)}.{str(mha_mask_config.positional_encoding_variant.value)}"

    return ops.inplace_custom(
        op_name,
        values=[
            input,
            k,
            v,
            buffer_row_offsets,
            cache_offsets,
            input_row_offsets,
            kv_collection,
            layer_idx,
            ops.constant(scale, dtype=DType.float32, device=DeviceRef.CPU()),
        ],
        out_types=[
            TensorType(
                dtype=input.dtype,
                shape=[
                    input.shape[0],
                    input.shape[1],
                    input.shape[2] - qk_rope_dim,
                ],
                device=input.device,
            )
        ],
        parameters=parameters,
    )[0].tensor


def flare_mla_prefill_plan(
    kv_params: KVCacheParams,
    input_row_offsets: TensorValue,
    kv_collection: PagedKVCacheCollection,
    layer_idx: TensorValue,
    buffer_size: int,
    max_chunks: int = 16,
) -> tuple[TensorValue, TensorValue, TensorValue]:
    """This kernel plans how to process a batch of sequences with
    varying lengths using a fixed-size buffer.

    Each sequence in the batch has some existing cached tokens and new input
    tokens. The kernel divides the total tokens into chunks of buffer_size.

    For each chunk (iteration), it calculates:
        1. Buffer offsets for each sequence in each chunk
        2. Cache offsets for each sequence in each chunk
        3. Total buffer lengths for each processing iteration
    """

    if layer_idx.dtype != DType.uint32:
        msg = f"expected uint32 layer_idx but got {layer_idx.dtype}"
        raise ValueError(msg)

    if input_row_offsets.dtype != DType.uint32:
        msg = f"expected uint32 input_row_offsets but got {input_row_offsets.dtype}"
        raise ValueError(msg)

    if kv_params.cache_strategy is not KVCacheStrategy.PAGED:
        msg = f"unsupported cache strategy for flare_mla_prefill_plan: {kv_params.cache_strategy}"
        raise ValueError(msg)

    assert kv_params.page_size is not None
    parameters: dict[str, int | str | DType] = {
        "type": kv_params.dtype,
        "num_heads": kv_params.n_kv_heads_per_device,
        "head_dim": kv_params.head_dim,
        "page_size": kv_params.page_size,
    }

    buffer_size_tensor = ops.constant(
        buffer_size, DType.uint32, device=DeviceRef.CPU()
    )

    results = ops.inplace_custom(
        "mo.mla.prefill.ragged.plan",
        values=[
            input_row_offsets,
            kv_collection,
            layer_idx,
            buffer_size_tensor,
        ],
        out_types=[
            TensorType(
                dtype=DType.uint32,
                shape=[max_chunks, input_row_offsets.shape[0]],
                device=input_row_offsets.device,
            ),  # buffer_row_offsets
            TensorType(
                dtype=DType.uint32,
                shape=[max_chunks, input_row_offsets.shape[0] - 1],
                device=input_row_offsets.device,
            ),  # cache_offsets
            TensorType(
                dtype=DType.int32,
                shape=[max_chunks],
                device=input_row_offsets.device,
            ),  # buffer_lengths
        ],
        parameters=parameters,
    )

    return results[0].tensor, results[1].tensor, results[2].tensor


def flare_mla_decompress_k_cache(
    kv_params: KVCacheParams,
    buffer_row_offsets_1d: TensorValue,
    cache_offsets_1d: TensorValue,
    buffer_length: TensorValue,
    weight: TensorValue,
    kv_collection: PagedKVCacheCollection,
    layer_idx: TensorValue,
    buffer_size: int,
) -> TensorValue:
    """This kernel decompresses the key cache by up-projecting latent representations
    into the KV space using a weight matrix.

    The process involves:
        1. Copying buffer_length latent vectors from the key cache into a contiguous
           buffer (k_latent)
        2. Computing k = k_latent @ weight.T to obtain the decompressed keys

    Returns:
        A tensor of shape [buffer_size, weight.shape[0]] containing the decompressed
        keys. Note that only the first buffer_length tokens are valid.
    """

    if layer_idx.dtype != DType.uint32:
        msg = f"expected uint32 layer_idx but got {layer_idx.dtype}"
        raise ValueError(msg)

    if cache_offsets_1d.dtype != DType.uint32:
        msg = f"expected uint32 cache_offsets but got {cache_offsets_1d.dtype}"
        raise ValueError(msg)

    if kv_params.cache_strategy is not KVCacheStrategy.PAGED:
        msg = f"unsupported cache strategy for flare_mla_decompress_k_cache: {kv_params.cache_strategy}"
        raise ValueError(msg)

    assert kv_params.page_size is not None
    parameters: dict[str, int | str | DType] = {
        "num_heads": kv_params.n_kv_heads_per_device,
        "head_dim": kv_params.head_dim,
        "page_size": kv_params.page_size,
    }

    results = ops.inplace_custom(
        "mo.mla.decompress.k.cache.ragged.paged",
        values=[
            buffer_row_offsets_1d,
            cache_offsets_1d,
            buffer_length,
            weight,
            kv_collection,
            layer_idx,
        ],
        out_types=[
            TensorType(
                dtype=kv_params.dtype,
                shape=[buffer_size, weight.shape[1]],
                device=buffer_row_offsets_1d.device,
            ),  # k_latent_buffer, only stores intermediate values
            TensorType(
                dtype=kv_params.dtype,
                shape=[buffer_size, weight.shape[0]],
                device=buffer_row_offsets_1d.device,
            ),  # k_buffer
        ],
        parameters=parameters,
    )

    return results[1].tensor


def kv_cache_get_max_seq_len(
    kv_collection: PagedKVCacheCollection,
) -> TensorValue:
    """This kernel returns the maximum sequence length."""
    return ops.inplace_custom(
        "mo.kv_cache.get_max_seq_len.paged",
        values=[kv_collection],
        out_types=[
            TensorType(
                dtype=DType.uint32,
                shape=[1],
                device=DeviceRef.CPU(),
            )
        ],
    )[0].tensor[0]


def cross_attention_ragged(
    kv_params: KVCacheParams,
    input: TensorValue,
    input_row_offsets: TensorValue,
    kv_collection: ContinuousBatchingKVCacheCollection | PagedKVCacheCollection,
    layer_idx: TensorValue,
    mask_variant: MHAMaskVariant,
    kv_input_row_offsets: TensorValue,
    q_max_seq_len: TensorValue,
    scale: float,
) -> TensorValue:
    """Computes cross attention provided the `!mo.opaque` KV Cache.

    Notably, this materializes the attention mask (dependent on MHAMaskVariant)
    within the kernel.
    `input` and `input_row_offsets` are used together to implement the ragged
    tensor.
    `input_row_offsets` indicates where each batch starts and ends in `input`

    attention, `kv_input_row_offsets` represents the KV sequence length.
    """
    input_rank_expected = 3
    if input.rank != input_rank_expected:
        msg = (
            f"expected input of rank {input_rank_expected} but got {input.rank}"
        )
        raise ValueError(msg)

    if input.dtype != kv_params.dtype:
        msg = (
            f"expected input to be dtype: {kv_params.dtype}, got {input.dtype}"
        )
        raise ValueError(msg)

    if layer_idx.dtype != DType.uint32:
        msg = f"expected uint32 layer_idx but got {layer_idx.dtype}"
        raise ValueError(msg)

    if input_row_offsets.dtype != DType.uint32:
        msg = f"expected uint32 input_row_offsets but got {input_row_offsets.dtype}"
        raise ValueError(msg)

    if kv_params.cache_strategy not in {
        KVCacheStrategy.CONTINUOUS,
        KVCacheStrategy.PAGED,
    }:
        msg = f"unsupported cache strategy for cross_attention_ragged: {kv_params.cache_strategy}"
        raise ValueError(msg)

    if q_max_seq_len and (q_max_seq_len.dtype != DType.uint32):
        msg = (
            "expected q_max_seq_len to be uint32 but got {q_max_seq_len.dtype}"
        )
        raise ValueError(msg)

    parameters: dict[str, int | str | DType] = {
        "num_heads": kv_params.n_kv_heads_per_device,
        "head_dim": kv_params.head_dim,
    }
    if kv_params.cache_strategy == KVCacheStrategy.PAGED:
        assert kv_params.page_size is not None
        parameters["page_size"] = kv_params.page_size

    cache_strategy_str = kv_params.cache_strategy.kernel_substring()
    mha_mask_config = _MHA_MASK_CONFIG_DICT[mask_variant]
    op_name = f"mo.cross_attention.ragged.{cache_strategy_str}.{str(mha_mask_config.attention_mask_variant.value)}.{str(mha_mask_config.positional_encoding_variant.value)}"

    return ops.inplace_custom(
        op_name,
        values=[
            input,
            input_row_offsets,
            # Plumb in the query max sequence length for cross attention.
            # For self attention this is the same as the KV max seq len stored
            # on the kv_collection, but that isn't the case for cross attention.
            q_max_seq_len,
            kv_input_row_offsets,
            kv_collection,
            layer_idx,
            # NOTE: The scale argument to flash attention is constrained to float32.
            ops.constant(scale, dtype=DType.float32, device=DeviceRef.CPU()),
        ],
        out_types=[
            TensorType(
                dtype=input.dtype, shape=input.shape, device=input.device
            )
        ],
        parameters=parameters,
        device=input.device,
    )[0].tensor


def swish_glu(
    a: TensorValueLike, b0: TensorValueLike, b1: TensorValueLike
) -> TensorValue:
    """Computes swish(a@b0.t()) * (a@b1.t())"""
    a = TensorValue(a)
    b0 = TensorValue(b0)
    b1 = TensorValue(b1)
    a_rank_expected = 2
    if a.rank != a_rank_expected:
        msg = f"expected a to have rank {a_rank_expected}, was {a.rank}"
        raise ValueError(msg)

    b0_rank_expected = 2
    if b0.rank != b0_rank_expected:
        msg = f"expected b0 to have rank {b0_rank_expected}, was {b0.rank}"
        raise ValueError(msg)

    b1_rank_expected = 2
    if b1.rank != b1_rank_expected:
        msg = f"expected b1 to have rank {b1_rank_expected}, was {b1.rank}"
        raise ValueError(msg)

    m = a.shape[0]
    n = b0.shape[0]
    if b0.shape[1] != a.shape[1]:
        msg = f"a.shape[1] == {a.shape[1]} != {b0.shape[1]} == b0.shape[1]"
        raise ValueError(msg)

    if b0.shape != b1.shape:
        msg = f"b0.shape == {b0.shape} != {b1.shape} == b1.shape"
        raise ValueError(msg)

    if a.dtype != b0.dtype or a.dtype != b1.dtype:
        msg = (
            "Element types of all arguments must be equal, but received"
            f" {a.dtype}, {b0.dtype}, and {b1.dtype}."
        )
        raise ValueError(msg)

    return ops.custom(
        "swishGLU",
        values=[a, b0, b1],
        out_types=[
            TensorType(
                dtype=a.dtype,
                shape=[m, n],
                device=a.device,
            )
        ],
    )[0].tensor


def rms_norm_key_cache(
    kv_params: KVCacheParams,
    kv_collection: ContinuousBatchingKVCacheCollection | PagedKVCacheCollection,
    gamma: TensorValue,
    epsilon: float | np.floating,
    layer_idx: int | np.integer,
    total_seq_len: Dim,
    input_row_offsets: TensorValue,
    rms_norm_cols: Optional[int] = None,
) -> None:
    """Computes RMSNorm on the _new_ entries in the KVCache.

    This function applies RMSNorm to either all dimensions or a subset of
    dimensions in each head of the key cache. The size of the gamma tensor
    determines how many dimensions will be normalized. If gamma's size doesn't
    match head_dim, rms_norm_cols must be explicitly specified to confirm the
    intention to normalize only a subset of dimensions.

    Currently, the KVCacheT class itself isn't aware of the new cache entries
    until cache length increment, which happens after model forward.
    So use `input_row_offsets` to do this bookkeeping.
    """
    cache_strategy_str = kv_params.cache_strategy.kernel_substring()
    op_name = f"mo.rms_norm_kv_cache.ragged.{cache_strategy_str}"

    gamma_rank_expected = 1
    if gamma.rank != gamma_rank_expected:
        msg = (
            f"expected gamma of rank {gamma_rank_expected} but got {gamma.rank}"
        )
        raise ValueError(msg)

    if input_row_offsets.dtype != DType.uint32:
        msg = f"expected uint32 input_row_offsets but got {input_row_offsets.dtype}"
        raise ValueError(msg)

    if gamma.shape[0] != kv_params.head_dim:
        if rms_norm_cols is None:
            msg = (
                "Size of gamma doesn't match head_dim. Please pass rms_norm_cols "
                "explicitly if you intend to apply RMSNorm to only a subset of "
                "head dimensions"
            )
            raise ValueError(msg)
        elif rms_norm_cols != gamma.shape[0]:
            msg = f"expected gamma of size {rms_norm_cols} but got {gamma.shape[0]}"
            raise ValueError(msg)

    if gamma.dtype != kv_params.dtype:
        msg = f"expected gamma dtype {gamma.dtype} to match KV dtype {kv_params.dtype}"
        raise TypeError(msg)

    parameters: dict[str, int | str | DType] = {
        "num_heads": kv_params.n_kv_heads_per_device,
        "head_dim": kv_params.head_dim,
    }
    if kv_params.cache_strategy == KVCacheStrategy.PAGED:
        assert kv_params.page_size is not None
        parameters["page_size"] = kv_params.page_size

    ops.inplace_custom(
        op_name,
        values=[
            kv_collection,
            gamma,
            ops.constant(epsilon, gamma.dtype, device=DeviceRef.CPU()),
            ops.constant(layer_idx, DType.uint32, device=DeviceRef.CPU()),
            ops.cast(TensorValue(total_seq_len), DType.uint32),
            input_row_offsets,
        ],
        parameters=parameters,
    )


def moe_create_indices(
    topk_ids: TensorValue,
    num_local_experts: int,
) -> tuple[TensorValue, TensorValue, TensorValue, TensorValue, TensorValue]:
    """Creates indices for the MoE layer.

    Args:
        topk_ids: The expert assignments for each token from the router.
        num_local_experts: The number of experts on this device.

    Returns:
        A tuple of four tensors:
        - token_expert_order: The reordered token indices, grouped by assigned expert.
        - expert_start_indices: The starting index for each expert's token group in
            the reordered sequence.
        - restore_token_order: The indices to restore original token ordering after
            expert computation.
        - expert_ids: ids of active experts selected for tokens
        - expert_usage_stats: The maximum number of tokens assigned to any expert,
            and the number of active experts.
    """

    results = ops.custom(
        "mo.moe.create.indices",
        values=[
            topk_ids,
        ],
        out_types=[
            TensorType(
                dtype=DType.uint32,
                shape=[topk_ids.shape[0]],
                device=topk_ids.device,
            ),  # token_expert_order
            TensorType(
                dtype=DType.uint32,
                shape=[num_local_experts + 1],
                device=topk_ids.device,
            ),  # expert_start_indices
            TensorType(
                dtype=DType.uint32,
                shape=[topk_ids.shape[0]],
                device=topk_ids.device,
            ),  # restore_token_order
            TensorType(
                dtype=DType.uint32,
                shape=[num_local_experts],
                device=topk_ids.device,
            ),  # expert_ids
            TensorType(
                dtype=DType.uint32,
                shape=[2],
                device=topk_ids.device,
            ),  # expert_usage_stats
        ],
    )

    return (
        results[0].tensor,
        results[1].tensor,
        results[2].tensor,
        results[3].tensor,
        results[4].tensor,
    )


def grouped_matmul_ragged(
    hidden_states: TensorValue,
    weight: TensorValue,
    expert_start_indices: TensorValue,
    expert_ids: TensorValue,
    expert_usage_stats_host: TensorValue,
) -> TensorValue:
    """Grouped matmul used in MoE layer.

    `hidden_states` and `expert_start_indices` are used together to implement
    the ragged tensor. `expert_start_indices` indicates where each group starts
    and ends in `hidden_states`

    `expert_ids` is the id of the expert for each group in `hidden_states`

    `expert_usage_stats_host` is the maximum number of tokens assigned to any
    expert, and the number of active experts.

    """

    if weight.rank != 3:
        msg = f"expected weight of rank 3 but got {weight.rank}"
        raise ValueError(msg)

    if hidden_states.rank != 2:
        msg = f"expected hidden_states of rank 2 but got {hidden_states.rank}"
        raise ValueError(msg)

    if (
        weight.shape[2] != hidden_states.shape[1]
        or weight.shape[0] != expert_ids.shape[0]
    ):
        msg = f"expected weight is of shape [num_experts, *, {hidden_states.shape[1]}] but got {weight.shape}"
        raise ValueError(msg)

    output = ops.custom(
        "mo.grouped.matmul.ragged",
        values=[
            hidden_states,
            weight,
            expert_start_indices,
            expert_ids,
            expert_usage_stats_host[0],
            expert_usage_stats_host[1],
        ],
        out_types=[
            TensorType(
                dtype=hidden_states.dtype,
                shape=[hidden_states.shape[0], weight.shape[1]],
                device=hidden_states.device,
            ),
        ],
    )[0].tensor

    return output
