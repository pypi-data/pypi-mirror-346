# Copyright (c) Huawei Technologies Co., Ltd. 2024-2025. All rights reserved.
# MindIE is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import math
import copy
from typing import Tuple

import torch

from vllm.attention import AttentionMetadata


class MmZipManager:
    def __init__(self, block_size: int, zip_layer_idx: int = 2, zip_ratio: float = 0.5, **kwargs) -> None:
        if block_size <= 0:
            raise ValueError(f"Expected block_size greater than 0, but got {block_size}.")
        if zip_layer_idx <= 0:
            raise ValueError(f"Expected zip_layer_idx greater than 0, but got {zip_layer_idx}.")
        if zip_ratio < 0 or zip_ratio >= 1:
            raise ValueError(f"Expected zip_ratio is between [0, 1), but got {zip_ratio}.")
        
        self.block_size = block_size
        self.zip_layer_idx = zip_layer_idx
        self.zip_ratio = zip_ratio
        self.all_seq_lens = {}

    def drop(
            self,
            layer_idx: int,
            attn_metadata: AttentionMetadata,
            positions: torch.Tensor,
            hidden_states: torch.Tensor,
            residual: torch.Tensor,
            **kwargs
    ) -> Tuple[AttentionMetadata, torch.Tensor, torch.Tensor, torch.Tensor]:
        is_prefill = True if attn_metadata.num_prefills > 0 else False
        attn_metadata.return_attn_score = False

        if is_prefill:
            if layer_idx == self.zip_layer_idx - 1:
                attn_metadata.return_attn_score = True
            elif layer_idx == self.zip_layer_idx:
                return self.update_prefill_param(
                    attn_metadata, positions, hidden_states, residual)
        if not is_prefill and layer_idx == self.zip_layer_idx:
            attn_metadata = self.update_decode_param(attn_metadata)
        return attn_metadata, positions, hidden_states, residual

    def update_prefill_param(
            self,
            attn_metadata: AttentionMetadata,
            positions: torch.Tensor,
            hidden_states: torch.Tensor,
            residual: torch.Tensor
    ) -> Tuple[AttentionMetadata, torch.Tensor, torch.Tensor, torch.Tensor]:
        zip_mask = []
        slots = []
        seq_lens = copy.deepcopy(attn_metadata.seq_lens)
        start_idx = 0
        for loop_idx, cur_seq_len in enumerate(seq_lens):
            end_idx = start_idx + cur_seq_len
            # 1. get single zip mask and drop offset
            mask, drop_offset = self.calculate_zip_metadata(
                attn_metadata.attn_score[:, -1, start_idx:end_idx],
                attn_metadata.vision_mask[start_idx:end_idx]
            )
            zip_mask.append(mask)

            # 2. update single item param
            slots.append(attn_metadata.slot_mapping[start_idx:end_idx - drop_offset])
            attn_metadata.seq_lens[loop_idx] -= drop_offset
            attn_metadata.selected_token_indices[loop_idx:] -= drop_offset
            self.all_seq_lens[attn_metadata.all_seq_ids[loop_idx]] = attn_metadata.seq_lens[loop_idx]
            start_idx = end_idx
        
        # 3. update the other param
        max_prefill_seq_len = max(attn_metadata.seq_lens)
        slots = torch.cat(slots, dim=0)
        attn_metadata.slot_mapping = slots
        attn_metadata.prefill_metadata.max_prefill_seq_len = max_prefill_seq_len
        attn_metadata.prefill_metadata.seq_lens = attn_metadata.seq_lens
        attn_metadata.prefill_metadata.slot_mapping = slots

        # 4. update positions, hidden_states, residual
        zip_mask = torch.cat(zip_mask, dim=0)
        hidden_states = hidden_states[zip_mask, :].contiguous()
        residual = residual[zip_mask, :].contiguous()
        if positions.ndim == 2:
            positions = positions[:, zip_mask]
        elif positions.ndim == 1:
            positions = positions[zip_mask]
        return attn_metadata, positions, hidden_states, residual

    def calculate_zip_metadata(
            self,
            attn_score: torch.Tensor,
            vision_mask: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        cur_score = torch.nn.functional.softmax(attn_score, dim=-1, dtype=torch.float32).mean(0)
        non_image_mask = ~vision_mask
        image_atten_score = cur_score[vision_mask]
        image_token_num = image_atten_score.shape[0]
        save_token_num = int(image_token_num * self.zip_ratio)
        drop_offset = (image_token_num - save_token_num)
        top_score_token_idx = image_atten_score.topk(save_token_num).indices
        keep_mask = torch.zeros(image_atten_score.shape, dtype=torch.bool, device=attn_score.device)
        keep_mask[top_score_token_idx] = True
        non_image_mask[vision_mask] = keep_mask
        return non_image_mask, drop_offset

    def update_decode_param(self, attn_metadata: AttentionMetadata) -> AttentionMetadata:
        max_prefill_seq_len = 0
        for loop_idx, seq_id in enumerate(attn_metadata.all_seq_ids):
            single_seq_len = self.all_seq_lens[seq_id]
            attn_metadata.slot_mapping[loop_idx] = (
                attn_metadata.block_tables[loop_idx][single_seq_len // self.block_size] *
                self.block_size + single_seq_len % self.block_size
            )
            single_seq_len += 1
            attn_metadata.seq_lens[loop_idx] = single_seq_len
            max_prefill_seq_len = max(max_prefill_seq_len, single_seq_len)
            self.all_seq_lens[seq_id] = single_seq_len
        attn_metadata.block_tables = \
            attn_metadata.block_tables[:, :int(math.ceil(max_prefill_seq_len / self.block_size))]
        attn_metadata.decode_metadata.seq_lens = attn_metadata.seq_lens
        return attn_metadata
