# This file was copied from the vLLM team, vLLM project,
# adapted from vllm/model_executor/layers/logits_processor.py
# The source file has no copyright description.
# SPDX-License-Identifier: Apache-2.0

# Some codes have been modified for compatibility with logits allgather.
# Copyright (c) Huawei Technologies Co., Ltd. 2024-2025. All rights reserved.

from typing import Optional

import torch
from vllm.model_executor.layers.logits_processor import (
    _apply_logits_processors,
    _prune_hidden_states,
)
from vllm.model_executor.layers.vocab_parallel_embedding import (
    VocabParallelEmbedding,
)
from vllm.model_executor.sampling_metadata import SamplingMetadata


def forward_with_allgather(
    self,
    lm_head: VocabParallelEmbedding,
    hidden_states: torch.Tensor,
    sampling_metadata: Optional[SamplingMetadata] = None,
    embedding_bias: Optional[torch.Tensor] = None,
) -> Optional[torch.Tensor]:
    self.use_all_gather = True
    if self.logits_as_input:
        logits = hidden_states
    else:
        if sampling_metadata is not None:
            hidden_states = _prune_hidden_states(
                hidden_states, sampling_metadata
            )

        # Get the logits for the next tokens.
        logits = self._get_logits(hidden_states, lm_head, embedding_bias)
    if logits is not None and (
        sampling_metadata and sampling_metadata.seq_groups is not None
    ):
        if self.soft_cap is not None:
            logits = logits / self.soft_cap
            logits = torch.tanh(logits)
            logits = logits * self.soft_cap

        if self.scale != 1.0:
            logits *= self.scale

        # Apply logits processors (if any).
        if sampling_metadata is not None:
            logits = _apply_logits_processors(logits, sampling_metadata)

    return logits
