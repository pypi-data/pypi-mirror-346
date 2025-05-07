# Copyright (c) Huawei Technologies Co., Ltd. 2024-2025. All rights reserved.
# MindIE is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NONINFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

from typing import Any, Dict, Generator, List, Optional, Tuple, Union

import torch
import torch_npu
from vllm.model_executor.layers.layernorm import RMSNorm
from vllm_ascend.attention.attention_v1 import AscendAttentionState
from mindie_turbo.quantize.faquant import AscendFAQuantAttentionMethod

from mindie_turbo import _ops as ops


# func refers to RMSNorm.__init__
def wrapper_rmsnorm_init(func):
    def init(self, hidden_size: int, **extra_args) -> None:
        func(self, hidden_size, **extra_args)
        self.ignore_anti = True
        self.bias = torch.nn.Parameter(torch.zeros(hidden_size), requires_grad=False)

    return init


# func refers to RMSNorm.forward_oot
def wrapper_rmsnorm_forward_oot(func):
    def _rmsnorm_forward_oot(
        self,
        x: torch.Tensor,
        residual: Optional[torch.Tensor] = None,
    ) -> Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        if not self.ignore_anti:
            if residual is not None:
                out = ops.add_rms_norm_quant(
                    residual,
                    x,
                    self.weight,
                    self.bias,
                    self.input_scale,
                    self.input_offset,
                    self.variance_epsilon,
                )
                return out, residual
            out = ops.rms_norm_quant(
                x,
                self.weight,
                self.bias,
                self.input_scale,
                self.input_offset,
                self.variance_epsilon,
            )
            return out

        if residual is not None:
            x, residual = func(self, x, residual)
            return x.add_(self.bias), residual

        return func(self, x).add_(self.bias)

    return _rmsnorm_forward_oot


def fake_rope_forward_oot(
    self,
    positions: torch.Tensor,
    query: torch.Tensor,
    key: torch.Tensor,
    offsets: Optional[torch.Tensor] = None,
) -> Tuple[torch.Tensor, torch.Tensor]:
    from mindie_turbo.adaptor.base_turbo import TurboPatch

    # we need to read this context info during runtime, because rope will instantiation before the
    # patch take effect, which may invalidate the patcher. so we use static patch wtih runtime check
    # to wa this issue.
    if TurboPatch.is_faquant:
        # if faqunat is activated, we adapt this fake rope for more aggressive fusion in
        # attention impl part
        metadata = {
            "positions": positions,
            "cos_sin_cache": self.cos_sin_cache,
            "head_size": self.head_size,
            "is_neox_style": self.is_neox_style,
        }
        # set metadata to attention for aggressive fusion impl, this patch
        # can only take effect when opt level is greater than 2
        AscendFAQuantAttentionMethod.set_attn_metadata(**metadata)
    else:
        # normal quant process
        if self.cos_sin_cache.device != query.device:
            self.cos_sin_cache = self.cos_sin_cache.to(query.device)
        if self.cos_sin_cache.dtype != query.dtype:
            self.cos_sin_cache = self.cos_sin_cache.to(query.dtype)
        if offsets is not None:
            raise NotImplementedError(
                "Batched rotary embedding is currently not supported on NPU."
            )
        else:
            from mindie_turbo import turbo_torch

            query, key = turbo_torch.rotary_embedding(
                positions,
                query,
                key,
                self.cos_sin_cache,
                self.head_size,
                self.is_neox_style,
            )
    return query, key


def ascend_faquant_attention_turbo_fwd_impl(
    self,
    layer,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    kv_cache: torch.Tensor,
    attn_metadata,
    attn_type: str = "decoder",
    output: Optional[torch.Tensor] = None,
):
    import numpy as np

    num_tokens = query.shape[0]
    value = value.view(-1, self.num_kv_heads, self.head_size)
    value = value.contiguous()

    if kv_cache.numel() > 0:
        if self.key_cache is None:
            self.key_cache, self.value_cache = kv_cache[0], kv_cache[1]
    is_prefill = True if attn_metadata.num_prefills > 0 else False
    if is_prefill:
        seq_lens = attn_metadata.prefill_metadata.seq_lens
    else:
        seq_lens = attn_metadata.decode_metadata.seq_lens
    block_tables = (
        attn_metadata.decode_metadata.block_tables
        if attn_metadata.decode_metadata
        else None
    )
    # Details of kv_cache arrangement in attention quantization
    # are implemented by quant_method.
    output = layer.quant_method.apply(
        layer,
        query,
        key,
        value,
        self.key_cache,
        self.value_cache,
        self.scale,
        block_tables,
        is_prefill,
        attn_metadata,
        None,
        seq_lens_tensor_cpu=seq_lens,
    )
    return output


def ascend_faquant_attention_turbo_fwd_impl_v1(
    self,
    layer,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    kv_cache: torch.Tensor,
    attn_metadata,
    output: Optional[torch.Tensor] = None,
):
    import numpy as np

    num_tokens = query.shape[0]
    if attn_metadata is None:
        # Profiling run.
        output = torch.empty(
            num_tokens,
            self.num_heads,
            self.head_size,
            dtype=query.dtype,
            device=query.device,
        )
        return output.view(num_tokens, self.hidden_size)
    value = value.view(-1, self.num_kv_heads, self.head_size)
    value = value.contiguous()

    if kv_cache.numel() > 0:
        if self.key_cache is None:
            self.key_cache, self.value_cache = kv_cache[0], kv_cache[1]
    is_prefill = (attn_metadata.attn_state == AscendAttentionState.PrefillNoCache)
    block_tables = attn_metadata.block_tables
    # Details of kv_cache arrangement in attention quantization
    # are implemented by quant_method.
    output = layer.quant_method.apply(
        layer,
        query,
        key,
        value,
        self.key_cache,
        self.value_cache,
        self.scale,
        block_tables,
        is_prefill,
        attn_metadata,
        None,
        seq_lens_tensor_cpu=attn_metadata.context_lens.tolist(),
    )
    return output
