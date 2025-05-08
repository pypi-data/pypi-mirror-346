# Part of this file was copied from the vLLM team, vLLM project,
# adapted from vllm/vllm/attention/layer.py
# The source file has no copyright and license description.
# Some codes have been modified for compatibility with FAQuant.

# Part of this file was copied from vllm-ascend, vLLM project,
# adapted from vllm_ascend/vllm_ascend/attention/attention.py
#
# Copyright (c) 2025 Huawei Technologies Co., Ltd. All Rights Reserved.
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
#

from typing import Optional

import numpy as np
import torch
import torch_npu
from torch.nn.functional import scaled_dot_product_attention
from vllm.attention import Attention, AttentionType
from vllm.attention.backends.abstract import AttentionLayer, AttentionType
from vllm.attention.selector import backend_name_to_enum, get_attn_backend
from vllm.config import get_current_vllm_config
from vllm.model_executor.layers.quantization.kv_cache import BaseKVCacheMethod
from vllm_ascend.attention.attention import AscendMetadata
from vllm_ascend.attention.attention_v1 import AscendAttentionState

from mindie_turbo import _ops as ops


def attention_init(
    self,
    num_heads: int,
    head_size: int,
    scale: float,
    **extra_impl_args,
) -> None:
    super(Attention, self).__init__()
    num_kv_heads = extra_impl_args.pop("num_kv_heads", None)
    alibi_slopes = extra_impl_args.pop("alibi_slopes", None)
    cache_config = extra_impl_args.pop("cache_config", None)
    quant_config = extra_impl_args.pop("quant_config", None)
    blocksparse_params = extra_impl_args.pop("blocksparse_params", None)
    logits_soft_cap = extra_impl_args.pop("logits_soft_cap", None)
    per_layer_sliding_window = extra_impl_args.pop(
        "per_layer_sliding_window", None
    )
    use_mla = extra_impl_args.pop("use_mla", False)
    prefix = extra_impl_args.pop("prefix", "")
    attn_type = extra_impl_args.pop("attn_type", AttentionType.DECODER)

    if per_layer_sliding_window is not None:
        # per-layer sliding window
        self.sliding_window = per_layer_sliding_window
    elif cache_config is not None:
        # model-level sliding window
        self.sliding_window = cache_config.sliding_window
    else:
        self.sliding_window = None

    if cache_config is not None:
        self.kv_cache_dtype = cache_config.cache_dtype
        block_size = cache_config.block_size
        is_attention_free = cache_config.is_attention_free
        self.calculate_kv_scales = cache_config.calculate_kv_scales
    else:
        self.kv_cache_dtype = "auto"
        block_size = 16
        is_attention_free = False
        self.calculate_kv_scales = False
    if num_kv_heads is None:
        num_kv_heads = num_heads

    # MindIE-Turbo attention quantization does not use following variables.
    # However, to keep compatibility with vLLM original attention, we need
    # maintain these codes.
    setattr(self, "_k_scale_float", 1.0)
    setattr(self, "_v_scale_float", 1.0)
    self.k_range = None
    self.v_range = None

    # should move following three lines before quant method instantiated.
    self.num_heads = num_heads
    self.head_size = head_size
    self.num_kv_heads = num_kv_heads

    # Not on cuda-alike or cpu platforms. self.use_direct_call is set to True.
    self.use_direct_call = True

    # During model initialization, the default dtype is set as the model
    # weight and activation dtype.
    self.dtype = torch.get_default_dtype()

    # Initialization of other member variables.
    self.layer_name = prefix
    self.attn_type = attn_type

    quant_method = (
        quant_config.get_quant_method(self, prefix=prefix)
        if quant_config
        else None
    )
    if quant_method is not None:
        if not isinstance(quant_method, BaseKVCacheMethod):
            raise TypeError(
                "quant_method must be an instance of BaseKVCacheMethod"
                f"but got {quant_method}"
            )
        if self.kv_cache_dtype not in ["int8", "auto"]:
            raise ValueError(
                "MindIE-Turbo attention quantizaton only support "
                f"int8 kv cache dtype, but got {self.kv_cache_dtype}"
            )
        self.quant_method = quant_method
        self.quant_method.create_weights(self)

    # Initialize attention.
    attn_backend = get_attn_backend(
        self.head_size,
        self.dtype,
        self.kv_cache_dtype,
        block_size,
        is_attention_free,
        blocksparse_params is not None,
        use_mla=use_mla,
    )
    impl_cls = attn_backend.get_impl_cls()
    self.impl = impl_cls(
        self.num_heads,
        self.head_size,
        scale,
        self.num_kv_heads,
        alibi_slopes,
        self.sliding_window,
        self.kv_cache_dtype,
        blocksparse_params,
        logits_soft_cap,
        attn_type,
        **extra_impl_args,
    )
    self.backend = backend_name_to_enum(attn_backend.get_name())
    self.use_output = attn_backend.accept_output_buffer

    compilation_config = get_current_vllm_config().compilation_config
    if prefix in compilation_config.static_forward_context:
        raise ValueError(f"Duplicate layer name: {prefix}")
    compilation_config.static_forward_context[prefix] = self

    init_cache_size = (
        get_current_vllm_config().parallel_config.pipeline_parallel_size
    )
    self.kv_cache = [torch.tensor([]) for _ in range(init_cache_size)]


def v1_attention_forward_mki(
    self,
    layer: AttentionLayer,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    kv_cache: torch.Tensor,
    attn_metadata: AscendMetadata,
    output: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    """Forward pass with Ascend attention.
    Args:
        query: shape = [batch_size, seq_len, num_heads * head_size]
        key: shape = [batch_size, seq_len, num_kv_heads * head_size]
        value: shape = [batch_size, seq_len, num_kv_heads * head_size]
        kv_cache: shape = [2, num_blocks, block_size,
                           num_kv_heads * head_size]
                  key_cache = [num_blocks, block_size,
                               num_kv_heads * head_size]
                  value_cache = [num_blocks, block_size,
                                 num_kv_heads * head_size]
        attn_metadata: Metadata for attention.
    Returns:
        shape = [batch_size * seq_len, num_heads, head_size]
    """
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
    attn_type = self.attn_type
    if attn_type != AttentionType.DECODER:
        raise NotImplementedError(
            "Encoder self-attention and "
            "encoder/decoder cross-attention "
            "are not implemented for "
            "PallasAttentionBackendImpl"
        )
    # View q k v to BSH.
    query = query.view(-1, self.num_heads, self.head_size)
    key = key.view(-1, self.num_kv_heads, self.head_size)
    value = value.view(-1, self.num_kv_heads, self.head_size)
    value = value.contiguous()

    if kv_cache.numel() > 0:
        if self.key_cache is None:
            self.key_cache, self.value_cache = kv_cache[0], kv_cache[1]
        slots = attn_metadata.slot_mapping
        ops.reshape_and_cache(
            key, value, self.key_cache, self.value_cache, slots
        )

    if hasattr(layer, "quant_method"):
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
    # V0-Style scheduler situation.
    elif attn_metadata.attn_state == AscendAttentionState.PrefillNoCache:
        mask = attn_metadata.attn_mask
        output = ops.unpad_flash_attention(
            query,
            key,
            value,
            mask,
            self.num_kv_heads,
            self.num_heads,
            self.scale,
            attn_metadata.context_lens.tolist(),
        )
    elif attn_metadata.attn_state == AscendAttentionState.PrefillCacheHit:
        output = torch.empty(
            num_tokens,
            self.num_heads,
            self.head_size,
            dtype=query.dtype,
            device=query.device,
        )
        compress_mask = attn_metadata.attn_mask
        torch_npu._npu_flash_attention_qlens(
            query=query,
            key_cache=self.key_cache,
            value_cache=self.value_cache,
            block_table=attn_metadata.block_tables,
            mask=compress_mask,
            seq_len=attn_metadata.seq_lens,
            context_lens=attn_metadata.context_lens,
            num_kv_heads=self.num_kv_heads,
            num_heads=self.num_heads,
            scale_value=self.scale,
            out=output)
        output = output.view(num_tokens, self.hidden_size)
    elif attn_metadata.attn_state == AscendAttentionState.DecodeOnly:
        block_tables = attn_metadata.block_tables
        output = ops.paged_attention_v1(
            query,
            self.key_cache,
            self.value_cache,
            self.num_kv_heads,
            self.num_heads,
            self.scale,
            block_tables,
            attn_metadata.context_lens.tolist(),
        )
    # Normal V1 situation.
    else:
        output = torch.empty(
            num_tokens,
            self.num_heads,
            self.head_size,
            dtype=query.dtype,
            device=query.device,
        )
        # use paged attention
        torch_npu._npu_paged_attention_splitfuse(
            query=query,
            key_cache=self.key_cache,
            value_cache=self.value_cache,
            mask=attn_metadata.attn_mask,
            block_table=attn_metadata.block_tables,
            seq_len=attn_metadata.seq_lens,
            context_lens=attn_metadata.context_lens,
            num_kv_heads=self.num_kv_heads,
            num_heads=self.num_heads,
            scale_value=self.scale,
            out=output,
        )
        output = output.view(num_tokens, self.hidden_size)
    return output


def attention_forward_with_mki_ops(
    self,
    layer: AttentionLayer,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    kv_cache: torch.Tensor,
    attn_metadata: AscendMetadata,
    attn_type: str = AttentionType.DECODER,
    output: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    # View q k v to BSH.
    num_tokens = query.shape[0]
    query = query.view(-1, self.num_heads, self.head_size)
    key = key.view(-1, self.num_kv_heads, self.head_size)
    value = value.view(-1, self.num_kv_heads, self.head_size)
    attn_type = self.attn_type

    if kv_cache.numel() > 0:
        if self.key_cache is None:
            self.key_cache, self.value_cache = kv_cache[0], kv_cache[1]
        slots = attn_metadata.slot_mapping

    if hasattr(layer, "quant_method"):
        output = attention_quant_method(
            layer,
            query,
            key,
            value,
            self.key_cache,
            self.value_cache,
            self.scale,
            attn_metadata
        )
    else:
        if self.key_cache is not None:
            ops.reshape_and_cache(
                key, value, self.key_cache, self.value_cache, slots
            )

        if attn_metadata.num_prefills > 0:
            # Prefix cache disabled  and  chunk prefill disabled  or  no prefix cache hit
            if (
                attn_metadata.block_tables is None
                or attn_metadata.block_tables.numel() == 0
            ):
                if attn_type == AttentionType.ENCODER_ONLY:
                    output = attention_encoder_only(
                        num_tokens,
                        self.num_heads,
                        self.head_size,
                        query,
                        key,
                        value,
                        self.scale,
                        attn_metadata
                    )
                else:
                    mask = attn_metadata.attn_mask
                    output = ops.unpad_flash_attention(
                        query,
                        key,
                        value,
                        mask,
                        self.num_kv_heads,
                        self.num_heads,
                        self.scale,
                        attn_metadata.prefill_metadata.seq_lens,
                    )
            elif (
                attn_metadata.num_decode_tokens == 0
                and not attn_metadata.chunked_prefill_enabled
            ):
                output = torch.empty(
                    num_tokens,
                    self.num_heads,
                    self.head_size,
                    dtype=query.dtype,
                    device=query.device,
                )
                self.seq_lens_tensor_cpu = torch.from_numpy(
                    np.array(attn_metadata.prefill_metadata.seq_lens).astype(
                        np.int32
                    )
                )
                self.query_lens_tensor_cpu = torch.from_numpy(
                    np.array(attn_metadata.prefill_metadata.query_lens).astype(
                        np.int32
                    )
                )
                block_tables = attn_metadata.prefill_metadata.block_tables
                compress_mask = attn_metadata.compress_mask
                torch_npu._npu_flash_attention_qlens(
                    query=query,
                    key_cache=self.key_cache,
                    value_cache=self.value_cache,
                    block_table=block_tables,
                    mask=compress_mask,
                    seq_len=self.query_lens_tensor_cpu,
                    context_lens=self.seq_lens_tensor_cpu,
                    num_kv_heads=self.num_kv_heads,
                    num_heads=self.num_heads,
                    scale_value=self.scale,
                    out=output,
                )
                output = output.view(num_tokens, self.hidden_size)
            # Splitfuse
            else:
                output = torch.empty(
                    num_tokens,
                    self.num_heads,
                    self.head_size,
                    dtype=query.dtype,
                    device=query.device,
                )
                self.seq_lens_tensor_cpu = torch.from_numpy(
                    np.array(attn_metadata.seq_lens).astype(np.int32)
                )
                self.query_lens_tensor_cpu = torch.from_numpy(
                    np.array(attn_metadata.query_lens).astype(np.int32)
                )
                block_tables = attn_metadata.block_tables
                chunk_mask = attn_metadata.chunk_mask
                torch_npu._npu_paged_attention_splitfuse(
                    query=query,
                    key_cache=self.key_cache,
                    value_cache=self.value_cache,
                    block_table=block_tables,
                    context_lens=self.seq_lens_tensor_cpu,
                    mask=chunk_mask,
                    seq_len=self.query_lens_tensor_cpu,
                    num_kv_heads=self.num_kv_heads,
                    num_heads=self.num_heads,
                    scale_value=self.scale,
                    out=output,
                )
                output = output.view(num_tokens, self.hidden_size)
        # Decode only
        else:
            block_tables = attn_metadata.decode_metadata.block_tables
            output = ops.paged_attention_v1(
                query,
                self.key_cache,
                self.value_cache,
                self.num_kv_heads,
                self.num_heads,
                self.scale,
                block_tables,
                attn_metadata.decode_metadata.seq_lens,
            )

    return output


def attention_quant_method(
    layer: AttentionLayer,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    key_cache: torch.Tensor,
    value_cache: torch.Tensor,
    scale: float,
    attn_metadata: AscendMetadata,
) -> torch.Tensor:
    value = value.contiguous()
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
    return layer.quant_method.apply(
        layer,
        query,
        key,
        value,
        key_cache,
        value_cache,
        scale,
        block_tables,
        is_prefill,
        attn_metadata,
        None,
        seq_lens_tensor_cpu=seq_lens,
    )


def attention_encoder_only(
    num_tokens: int,
    num_heads: int,
    head_size: int,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    scale: float,
    attn_metadata: AscendMetadata,
) -> torch.Tensor:
    output = torch.empty(
        num_tokens,
        num_heads,
        head_size,
        dtype=query.dtype,
        device=query.device,
    )
    query = query.movedim(0, query.dim() - 2)
    key = key.movedim(0, key.dim() - 2)
    value = value.movedim(0, value.dim() - 2)

    if attn_metadata.seq_lens is not None:
        seq_lens_q = seq_lens_kv = attn_metadata.seq_lens
    attn_masks = [None] * len(seq_lens_q)
    start_q, start_kv = 0, 0
    for seq_len_q, seq_len_kv, mask in zip(
        seq_lens_q, seq_lens_kv, attn_masks
    ):
        end_q = start_q + seq_len_q
        end_kv = start_kv + seq_len_kv
        sub_out = (
            scaled_dot_product_attention(
                query[None, :, start_q:end_q, :],
                key[None, :, start_kv:end_kv, :],
                value[None, :, start_kv:end_kv, :],
                attn_mask=mask,
                dropout_p=0.0,
                is_causal=False,
                scale=scale,
            )
            .squeeze(0)
            .movedim(query.dim() - 2, 0)
        )
        output[start_q:end_q, :, :] = sub_out
        start_q, start_kv = end_q, end_kv
    hidden_size = num_heads * head_size
    return output.view(num_tokens, hidden_size)
