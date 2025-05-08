#
# Copyright (c) 2025 Huawei Technologies Co., Ltd. All Rights Reserved.
# Adapted from vllm/model_executor/models/qwen2_vl.py
# Copyright 2023 The vLLM team.
#
# This file is a part of the vllm-ascend project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math
from functools import partial
from typing import Callable, Optional, Type

import torch
import torch.nn as nn
import torch_npu
from einops import rearrange
from transformers.models.qwen2_vl.configuration_qwen2_vl import \
    Qwen2VLVisionConfig
from vllm.config import VllmConfig
from vllm.distributed import utils as dist_utils
from vllm.model_executor.layers.activation import QuickGELU
from vllm.model_executor.layers.linear import ReplicatedLinear
from vllm.model_executor.layers.quantization import QuantizationConfig
from vllm.model_executor.models.qwen2_vl import (
    Qwen2VisionAttention, Qwen2VisionBlock, Qwen2VisionTransformer,
    Qwen2VLForConditionalGeneration, apply_rotary_pos_emb_vision,
    Qwen2VisionPatchMerger, Qwen2VisionMLP)
from vllm.model_executor.models.utils import maybe_prefix
from mindie_turbo.multimodal.mmdist.comm import all_to_all_3d, all_to_all_4d, all_gather_2d
from mindie_turbo.multimodal.mmdist.utils import get_rank_world, extract_local, pad_to_divisible


class CustomQwen2VisionMLP(Qwen2VisionMLP):

    def __init__(
        self,
        in_features: int,
        hidden_features: int,
        act_layer: Type[nn.Module] = QuickGELU,
        quant_config: Optional[QuantizationConfig] = None,
        prefix: str = "",
    ):
        super().__init__(in_features, hidden_features, act_layer, quant_config, prefix)
        self.fc1 = ReplicatedLinear(in_features,
                                        hidden_features,
                                        quant_config=quant_config,
                                        prefix=f"{prefix}.fc1")
        self.act = act_layer()
        self.fc2 = ReplicatedLinear(hidden_features,
                                     in_features,
                                     quant_config=quant_config,
                                     prefix=f"{prefix}.fc2")


class CustomQwen2VisionAttention(Qwen2VisionAttention):

    def __init__(
        self,
        embed_dim: int,
        num_heads: int,
        projection_size: int,
        quant_config: Optional[QuantizationConfig] = None,
        prefix: str = "",
    ) -> None:
        super().__init__(
            embed_dim,
            num_heads,
            projection_size,
            quant_config,
            prefix,
        )
        self.cu_seqlens = None
        self.tp_size = 1
        self.tp_rank = 0
        _, world_size = get_rank_world()
        self.num_attention_heads_per_partition = dist_utils.divide(
            num_heads, world_size)
        self.qkv = ReplicatedLinear(input_size=embed_dim,
                                        output_size=3 * projection_size,
                                        quant_config=quant_config,
                                        prefix=f"{prefix}.qkv")
        self.proj = ReplicatedLinear(input_size=projection_size,
                                      output_size=embed_dim,
                                      quant_config=quant_config,
                                      prefix=f"{prefix}.proj")

    def split_qkv(self, qkv: torch.Tensor) -> tuple[torch.Tensor, ...]:
        seq_len, bs, _ = qkv.shape

        # [s, b, 3 * head * head_dim] -> 3 * [s, b, head * head_dim]
        q, k, v = qkv.chunk(3, dim=2)

        # 3 * [s, b, head * head_dim] -> 3 * [s, b, head, head_dim]
        new_shape = (seq_len, bs, -1, self.hidden_size_per_attention_head)
        q, k, v = (x.view(*new_shape) for x in (q, k, v))
        return q, k, v

    def forward(
        self,
        x: torch.Tensor,
        cu_seqlens: torch.Tensor,
        rotary_pos_emb: torch.Tensor,
    ) -> torch.Tensor:

        rank, world_size = get_rank_world()
        self.cu_seqlens = cu_seqlens

        # [s, b, c] --> [s, b, 3 * head * head_dim]
        x, _ = self.qkv(x)
        x = rearrange(x, 's b (t h d) -> (b t) s h d', 
            b=1, t=3, h=self.num_attention_heads_per_partition * world_size
        )

        x = all_to_all_4d(x, is_seq_to_head=True)

        x = rearrange(x, '(b t) s h d -> s b (t h d)', 
            b=1, t=3, h=self.num_attention_heads_per_partition
        )

        # [s, b, 3 * head * head_dim] -> 3 * [s, b, head, head_dim]
        q, k, v = self.split_qkv(x)
        batch_size = q.shape[1]

        q, k, v = [rearrange(x, "s b ... -> b s ...").contiguous() for x in (q, k, v)]
        if rotary_pos_emb is not None:
            q = apply_rotary_pos_emb_vision(q, rotary_pos_emb)
            k = apply_rotary_pos_emb_vision(k, rotary_pos_emb)
        q, k, v = [
            rearrange(x, "b s h d -> (b s) h d").contiguous()
            for x in (q, k, v)
        ]

        context_layer = torch.torch.empty_like(q)

        # operator requires pta version >= 2.5.1.dev20250226
        torch_npu._npu_flash_attention_unpad(
            query=q,
            key=k,
            value=v,
            seq_len=self.cu_seqlens,
            scale_value=self.hidden_size_per_attention_head**-0.5,
            num_heads=self.num_attention_heads_per_partition,
            num_kv_heads=self.num_attention_heads_per_partition,
            out=context_layer)

        context_layer = all_to_all_3d(context_layer, is_seq_to_head=False)
        context_layer = rearrange(context_layer,
                                  "(b s) h d -> s b (h d)",
                                  b=batch_size).contiguous()

        output, _ = self.proj(context_layer)
        return output


class CustomQwen2VisionBlock(Qwen2VisionBlock):

    def __init__(
        self,
        dim: int,
        num_heads: int,
        mlp_ratio: float,
        act_layer: Type[nn.Module] = QuickGELU,
        norm_layer: Optional[Callable[[int], nn.Module]] = None,
        quant_config: Optional[QuantizationConfig] = None,
        prefix: str = "",
    ) -> None:
        super().__init__(dim, num_heads, mlp_ratio, act_layer, norm_layer,
                         quant_config, prefix)
        self.attn = CustomQwen2VisionAttention(embed_dim=dim,
                                               num_heads=num_heads,
                                               projection_size=dim,
                                               quant_config=quant_config,
                                               prefix=f"{prefix}.attn")


class CustomQwen2VisionPatchMerger(Qwen2VisionPatchMerger):

    def __init__(
        self,
        d_model: int,
        context_dim: int,
        norm_layer: Optional[Callable[[int], nn.Module]] = None,
        spatial_merge_size: int = 2,
        quant_config: Optional[QuantizationConfig] = None,
        prefix: str = "",
    ) -> None:
        super().__init__(d_model, context_dim, norm_layer, spatial_merge_size, quant_config, prefix)
        self.hidden_size = context_dim * (spatial_merge_size**2)
        if norm_layer is None:
            norm_layer = partial(nn.LayerNorm, eps=1e-6)
        self.ln_q = norm_layer(context_dim)
        self.mlp = nn.ModuleList([
            ReplicatedLinear(self.hidden_size,
                                 self.hidden_size,
                                 bias=True,
                                 quant_config=quant_config,
                                 prefix=f"{prefix}.mlp.0"),
            nn.GELU(),
            ReplicatedLinear(self.hidden_size,
                              d_model,
                              bias=True,
                              quant_config=quant_config,
                              prefix=f"{prefix}.mlp.2"),
        ])


class CustomQwen2VisionTransformer(Qwen2VisionTransformer):

    def __init__(
        self,
        vision_config: Qwen2VLVisionConfig,
        norm_eps: float = 1e-6,
        quant_config: Optional[QuantizationConfig] = None,
        prefix: str = "",
    ) -> None:
        super().__init__(vision_config, norm_eps, quant_config, prefix)
        norm_layer = partial(nn.LayerNorm, eps=norm_eps)
        self.blocks = nn.ModuleList([
            CustomQwen2VisionBlock(dim=self.embed_dim,
                                   num_heads=self.num_heads,
                                   mlp_ratio=vision_config.mlp_ratio,
                                   norm_layer=norm_layer,
                                   quant_config=quant_config,
                                   prefix=f"{prefix}.blocks.{layer_idx}")
            for layer_idx in range(vision_config.depth)
        ])
        self.merger = CustomQwen2VisionPatchMerger(
            d_model=vision_config.hidden_size,
            context_dim=self.embed_dim,
            norm_layer=norm_layer,
            quant_config=quant_config,
            prefix=f"{prefix}.merger",
        )

    def forward(
        self,
        x: torch.Tensor,
        grid_thw: torch.Tensor,
    ) -> torch.Tensor:
        rank, world_size = get_rank_world()
        # patchify
        x = x.to(device=self.device, dtype=self.dtype)
        x = self.patch_embed(x)

        # compute position embedding
        rotary_pos_emb = self.rot_pos_emb(grid_thw)

        seq_len = x.size(0)
        merge_size = self.spatial_merge_size ** 2
        padding_size = math.ceil(math.ceil(seq_len / world_size) / merge_size) * merge_size * world_size - seq_len
        if padding_size > 0:
            padding = torch.zeros(
                padding_size, *x.size()[1:],
                dtype=x.dtype, device=x.device
            )
            x = torch.cat([x, padding], dim=0)
            padding_grid = torch.tensor([[1, 1, padding_size]],
                dtype=grid_thw.dtype, device=grid_thw.device
            )    
            grid_thw = torch.cat([grid_thw, padding_grid], dim=0)
            padding_rot = torch.zeros(
                padding_size, *rotary_pos_emb.size()[1:],
                dtype=rotary_pos_emb.dtype, device=rotary_pos_emb.device
            )
            rotary_pos_emb = torch.cat([rotary_pos_emb, padding_rot], dim=0)

        x = extract_local(x, dim=0, rank=rank, world_size=world_size)
        # compute cu_seqlens and avoid cumsum to fit operator unpadFA
        cu_seqlens = torch.repeat_interleave(grid_thw[:, 1] * grid_thw[:, 2],
                                             grid_thw[:,
                                                      0]).cpu().to(torch.int32)

        x = x.unsqueeze(1)
        for blk in self.blocks:
            x = blk(x, cu_seqlens=cu_seqlens, rotary_pos_emb=rotary_pos_emb)

        # adapter
        x = self.merger(x)

        x_gather = all_gather_2d(x, world_size=world_size, group=None)
        if padding_size:
            x_gather = x_gather[:-padding_size // merge_size]
        return x_gather


class CustomQwen2VLForConditionalGeneration(Qwen2VLForConditionalGeneration):

    def __init__(self, *, vllm_config: VllmConfig, prefix: str = ""):
        super().__init__(vllm_config=vllm_config)
        self.visual = CustomQwen2VisionTransformer(
            self.config.vision_config,
            norm_eps=getattr(self.config, "rms_norm_eps", 1e-6),
            quant_config=self._maybe_ignore_quant_config(
                vllm_config.quant_config),
            prefix=maybe_prefix(prefix, "visual"),
        )