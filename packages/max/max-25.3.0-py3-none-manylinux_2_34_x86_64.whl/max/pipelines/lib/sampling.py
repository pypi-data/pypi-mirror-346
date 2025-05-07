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

"""Token sampling algorithms."""

from max.dtype import DType
from max.graph import DeviceRef, Dim, Graph, Shape, TensorType, TensorValue, ops
from max.nn.sampling import RejectionSampler

from .max_config import SamplingConfig


def _sampling_input_types(
    sampling_config: SamplingConfig, return_logits: bool, device: DeviceRef
) -> dict[str, TensorType]:
    inputs = {}

    # Logits are always provided
    if sampling_config.enable_variable_logits:
        logits_in_type = TensorType(
            sampling_config.in_dtype,
            ["total_output_len", "vocab_size"],
            device=device,
        )
        inputs["logits"] = logits_in_type
    else:
        logits_in_type = TensorType(
            sampling_config.in_dtype,
            ["batch", "vocab_size"],
            device=device,
        )
        inputs["logits"] = logits_in_type

    # We are currently, always passing tokens through
    prev_tokens_type = TensorType(
        DType.int64, ["batch", "num_prev_steps"], device=device
    )
    inputs["prev_tokens"] = prev_tokens_type

    # If we need to return logits, introduce tensor to append to.
    if return_logits:
        logits_type = TensorType(
            DType.float32, ["batch", "num_prev_steps"], device=device
        )
        inputs["existing_logits"] = logits_type

    # If we have variable token logits enabled
    if sampling_config.enable_variable_logits:
        logit_offset_type = TensorType(
            DType.uint32, ["logit_offsets_len"], device=device
        )
        inputs["logit_offsets"] = logit_offset_type

    # If we have structured_outputs enabled
    if sampling_config.enable_structured_output:
        bitmask_type = TensorType(
            DType.bool, ["batch", "vocab_size"], device=device
        )
        inputs["bitmask"] = bitmask_type

    return inputs


def token_sampler(
    sampling_config: SamplingConfig,
    device: DeviceRef,
    return_logits: bool = False,
) -> Graph:
    _input_dict = _sampling_input_types(
        sampling_config, return_logits=return_logits, device=device
    )
    with Graph("top_k_sampler", input_types=_input_dict.values()) as graph:
        # Deconstruct inputs
        # TODO: Explore better ways of indexing into these input values
        # tightly coupling the input order with element indices feels
        # quite brittle.
        logits = graph.inputs[list(_input_dict).index("logits")].tensor

        logits = ops.cast(logits, sampling_config.out_dtype)
        prev_tokens = graph.inputs[
            list(_input_dict).index("prev_tokens")
        ].tensor

        if "existing_logits" in _input_dict:
            existing_logits = graph.inputs[
                list(_input_dict).index("existing_logits")
            ].tensor

        if "logit_offsets" in _input_dict:
            logit_offsets = graph.inputs[
                list(_input_dict).index("logit_offsets")
            ].tensor
            logits = ops.gather(logits, logit_offsets[1:] - 1, axis=0)
            logits = ops.rebind(logits, shape=("batch", "vocab_size"))

        if "bitmask" in _input_dict:
            bitmask = graph.inputs[list(_input_dict).index("bitmask")].tensor
            logits = ops.select(
                bitmask,
                logits,
                ops.constant(-10000, dtype=DType.float32, device=device),
            )

        # Apply top_k sampling
        shape = Shape(logits.shape)
        shape[-1] = Dim(1)
        tokens = ops.custom(
            "topk_fused_sampling",
            [
                ops.constant(
                    sampling_config.top_k, dtype=DType.int64, device=device
                ),
                ops.constant(
                    sampling_config.temperature,
                    dtype=DType.float32,
                    device=device,
                ),
                logits,
            ],
            [TensorType(DType.int64, shape, device=device)],
        )[0]
        assert isinstance(tokens, TensorValue)

        # Concat tokens to previous tokens.
        all_tokens = ops.concat([prev_tokens, tokens], -1)

        # Gather logits if needed to return.
        if "existing_logits" in _input_dict:
            token_range = ops.reshape(
                ops.range(
                    ops.constant(0, dtype=DType.int64, device=device),
                    tokens.shape[0],
                    ops.constant(1, dtype=DType.int64, device=device),
                    out_dim=Dim(tokens.shape[0]),
                    device=device,
                ),
                shape=tokens.shape,
            )

            token_indices = ops.concat(
                [
                    token_range,
                    tokens,
                ],
                axis=1,
            )
            new_logits = ops.reshape(
                ops.gather_nd(logits, token_indices), shape=tokens.shape
            )

            all_logits = ops.concat([existing_logits, new_logits], -1)
            tokens = ops.squeeze(tokens, -1)
            graph.output(tokens, all_tokens, all_logits)
        else:
            tokens = ops.squeeze(tokens, -1)
            graph.output(tokens, all_tokens)

        return graph


def rejection_sampler(top_k: int, device: DeviceRef) -> Graph:
    # We have two distributions:
    #   p(x) - The target model distribution
    #   q(x) - The draft model distribution
    #
    # For any given token idx x_i, we have two probabilities p(x_i) and q(x_i)
    # We accept the token with a probability of p(x_i) > q(x_i)
    #
    # If rejected, we should just sample a new token from the target distribution.
    #
    # We then resample from this distribution.

    graph_inputs = [
        # Sampled Draft Tokens
        TensorType(DType.int64, ["batch_size", "num_steps"], device=device),
        # Logits for Sampled Tokens
        TensorType(DType.float32, ["batch_size", "num_steps"], device=device),
        # Target Logits
        TensorType(
            DType.float32,
            ["total_output_len", "vocab_size"],
            device=device,
        ),
        # Target Logit Offsets
        TensorType(DType.int64, ["logit_offsets_len"], device=device),
    ]
    with Graph("rejection_sampler", input_types=graph_inputs) as graph:
        (
            draft_tokens,
            draft_logits_for_sampled_tokens,
            target_logits,
            target_logit_offsets,
        ) = graph.inputs

        sampler = RejectionSampler(device=device, top_k=top_k)
        first_rejected_token, sampled_target_tokens = sampler(
            draft_tokens.tensor,
            draft_logits_for_sampled_tokens.tensor,
            target_logits.tensor,
            target_logit_offsets.tensor,
        )
        graph.output(first_rejected_token, sampled_target_tokens)

        return graph
