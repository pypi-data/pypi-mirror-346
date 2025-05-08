# This file includes codes from vLLM project which is licensed under Apache License, Version 2.0.
# Some of the codes have been modified for compatibility with Ascend NPU.
# Copyright (c) Huawei Technologies Co., Ltd. 2024-2025. All rights reserved.

import functools
import importlib
from typing import List, Optional

import numpy as np
import torch
import torch_npu
from vllm.model_executor.sampling_metadata import (SamplingMetadata,
                                                   SequenceGroupToSample)

from mindie_turbo.utils.logger import logger


def load_cpu_logits_handler():
    mindie_turbo = importlib.import_module("mindie_turbo")
    from mindie_turbo import _cpu_logits_handler

    return _cpu_logits_handler._PostProcessingManager.get_instance(1, 0)


def _apply_top_k_top_p(
    logits: torch.Tensor,
    p: torch.Tensor,
    k: torch.Tensor,
) -> torch.Tensor:
    logits_dtype_str = {
        torch.float32: "float32",
        torch.float16: "float16",
        torch.bfloat16: "bfloat16",
    }.get(logits.dtype, "float16")
    logits_sort, logits_idx = logits.sort(dim=-1, descending=True)
    if p.dtype == torch.bfloat16:
        p = p.to(torch.float16)
    handler = load_cpu_logits_handler()
    logits_res = handler.apply_top_k_top_p(
        k.cpu().numpy(),
        p.cpu().numpy(),
        logits_sort.data_ptr(),
        logits_idx.data_ptr(),
        logits.shape[0],
        logits.shape[1],
        logits_dtype_str,
    )
    logits_res = torch.from_numpy(logits_res).to(logits.device).to(logits.dtype)
    logits_tmp = torch.full_like(logits_res, float("-inf"))
    return logits_tmp.scatter_(1, logits_idx, logits_res)


def _multinomial(
    probs: torch.Tensor,
    num_samples: int,
    seq_groups: Optional[List[SequenceGroupToSample]] = None,
) -> torch.Tensor:
    if num_samples > 1:
        probs = probs.repeat_interleave(num_samples, dim=0)
        q = torch.empty_like(probs)
        if seq_groups is None:
            q.exponential_()
        else:
            sample_idx = 0
            for seq_group in seq_groups:
                seq_ids = seq_group.seq_ids
                stride = len(seq_ids) * num_samples
                if seq_group.generator is None:
                    raise ValueError(
                        "Generator must be provided for each sequence group"
                    )
                q[sample_idx: sample_idx + stride].exponential_(
                    generator=seq_group.generator
                )
                sample_idx += stride
        return probs.div_(q).argmax(dim=1).view(-1, num_samples)
    else:
        probs_dtype_str = {
            torch.float32: "float32",
            torch.float16: "float16",
            torch.bfloat16: "bfloat16",
        }.get(probs.dtype, "float16")
        seeds = np.random.randint(-(2**31), 2**31, size=(probs.shape[0], 1))
        torch_npu.npu.synchronize()
        handler = load_cpu_logits_handler()
        next_tokens = handler.exponential(
            seeds,
            probs.data_ptr(),
            probs.shape[0],
            probs.shape[1],
            probs_dtype_str,
        )
        return torch.from_numpy(next_tokens).to(probs.device)


def cache_sampling_tensors_decorator(init_fn):
    """Decorator that caches sampling tensors based on request IDs hash.

    Args:
        init_fn: The original initialization function for sampling tensors.

    Returns:
        Wrapped function that implements caching behavior.
    """

    @functools.wraps(init_fn)
    def wrapper(self, logits, sampling_metadata: SamplingMetadata) -> None:
        if not (
            hasattr(sampling_metadata, "request_ids_hash")
            and hasattr(self, "last_request_ids_hash")
            and self.last_request_ids_hash
            == sampling_metadata.request_ids_hash
        ):
            self.last_request_ids_hash = getattr(
                sampling_metadata, "request_ids_hash", None
            )
            init_fn(self, logits, sampling_metadata)
        else:
            logger.debug("Cache hit for sampling tensors.")

    return wrapper


def _apply_min_p_without_changing_minp(
    logits: torch.Tensor,
    min_p: torch.Tensor,
) -> torch.Tensor:
    probs = torch.softmax(logits, dim=-1)
    top_probs, _ = probs.max(dim=-1, keepdim=True)
    scaled_min_p = torch.unsqueeze(min_p, dim=1) * top_probs
    tokens_to_remove = probs < scaled_min_p
    logits = logits.masked_fill_(tokens_to_remove, -float("inf"))

    return logits
