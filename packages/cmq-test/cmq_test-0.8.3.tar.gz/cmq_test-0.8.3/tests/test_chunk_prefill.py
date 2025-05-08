# SPDX-License-Identifier: Apache-2.0
"""Compare the outputs of HF and vLLM when using greedy sampling.

It tests chunked prefill. Chunked prefill can be enabled by
enable_chunked_prefill=True. If prefill size exceeds max_num_batched_tokens,
prefill requests are chunked.

Run `pytest tests/models/test_chunked_prefill.py`.
"""
import os

import pytest


from tests.model_utils import check_logprobs_close, check_outputs_equal

MODELS = [
    # "facebook/opt-125m",
    "/home/cmq/cache/modelscope/models/Qwen/Qwen2___5-0___5B-Instruct"
    # "meta-llama/Llama-3.2-1B-Instruct",
]


@pytest.mark.parametrize("model", MODELS)
@pytest.mark.parametrize("dtype", ["half"])
@pytest.mark.parametrize("max_tokens", [32])
@pytest.mark.parametrize("chunked_prefill_token_size", [1, 
                                                        4, 16
                                                        ])
@pytest.mark.parametrize("enforce_eager", [True])
# NOTE: Increasing this in this suite will fail CI because we currently cannot
# reset distributed env properly. Use a value > 1 just when you test.
@pytest.mark.parametrize("tensor_parallel_size", [1])
def test_models(
    hf_runner,
    vllm_runner,
    example_prompts,
    model: str,
    dtype: str,
    max_tokens: int,
    chunked_prefill_token_size: int,
    enforce_eager: bool,
    tensor_parallel_size: int,
) -> None:
    """
    Checks exact match decode between huggingface model and vllm runner with
    chunked prefill.
    """

    max_num_seqs = chunked_prefill_token_size
    max_num_batched_tokens = chunked_prefill_token_size

    with hf_runner(model, dtype=dtype) as hf_model:
        hf_outputs = hf_model.generate_greedy(example_prompts, max_tokens)

    with vllm_runner(
            model,
            dtype=dtype,
            max_num_batched_tokens=max_num_batched_tokens,
            enable_chunked_prefill=True,
            tensor_parallel_size=tensor_parallel_size,
            enforce_eager=enforce_eager,
            max_num_seqs=max_num_seqs,
    ) as vllm_model:
        vllm_outputs = vllm_model.generate_greedy(example_prompts, max_tokens)

    print(hf_outputs)
    print(100*"*")
    print(vllm_outputs)
    check_outputs_equal(
        outputs_0_lst=hf_outputs,
        outputs_1_lst=vllm_outputs,
        name_0="hf",
        name_1="vllm",
    )


# @pytest.mark.parametrize("max_tokens", [16])
# @pytest.mark.parametrize("enforce_eager", [False])
# @pytest.mark.parametrize("chunk_size", [30, 32])
# # NOTE: Increasing this in this suite will fail CI because we currently cannot
# # reset distributed env properly. Use a value > 1 just when you test.
# @pytest.mark.parametrize("tensor_parallel_size", [1])
# @pytest.mark.parametrize("dtype", ["half"])
# def test_with_prefix_caching(
#     vllm_runner,
#     max_tokens: int,
#     enforce_eager: bool,
#     chunk_size: int,
#     tensor_parallel_size: int,
#     dtype: str,
# ) -> None:
#     """
#     Checks exact match decode with and without prefix caching
#     with chunked prefill enabled.
#     """
#     model = "meta-llama/Llama-3.2-1B-Instruct"
#     # The common prompt has 142 tokens with Llama-2 tokenizer.
#     common_prompt = "You are a helpful AI assistant " * 20
#     unique_prompts = [
#         "Question",  # Warmup
#         "Question",  # Fully cached
#         "Another question",  # Partial cached
#     ]
#     full_prompts = [f"{common_prompt}\n{p}" for p in unique_prompts]

#     max_num_batched_tokens = max_num_seqs = chunk_size
#     outputs = {}  # type: ignore
#     for enable in (True, False):
#         with vllm_runner(
#                 model,
#                 dtype=dtype,
#                 max_num_batched_tokens=max_num_batched_tokens,
#                 enable_chunked_prefill=True,
#                 enable_prefix_caching=enable,
#                 tensor_parallel_size=tensor_parallel_size,
#                 enforce_eager=enforce_eager,
#                 max_num_seqs=max_num_seqs,
#         ) as vllm_model:
#             outputs[enable] = []
#             for prompt in full_prompts:
#                 outputs[enable] += vllm_model.generate_greedy([prompt],
#                                                               max_tokens)

#     check_outputs_equal(
#         outputs_0_lst=outputs[False],
#         outputs_1_lst=outputs[True],
#         name_0="w/o prefix caching",
#         name_1="with prefix caching",
#     )


