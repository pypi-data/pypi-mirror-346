# Copyright (c) Huawei Technologies Co., Ltd. 2024-2025. All rights reserved.
# MindIE is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

from typing import Any, Dict, Tuple, List, Optional
from dataclasses import dataclass
import os

import torch
import torch_npu

from mindie_turbo import _ops as ops
from .quant_utils import quant_per_tensor, SRC_DTYPE_TO_ACL_DTYPE


@dataclass
class AscendFAMetaData:
    # metadata for lv2 optimization rope_quant fusion
    positions: torch.Tensor
    cos_sin_cache: torch.Tensor
    head_size: int = 0
    is_neox_style: bool = True


class AscendFAQuantAttentionMethod:
    """Linear method for Ascend FAQuant.
    """

    cls_metadata: AscendFAMetaData = None

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def get_quant_param() -> List[str]:
        return ["fa_q.scale", "fa_q.offset", "fa_k.scale", "fa_k.offset", "fa_v.scale", "fa_v.offset"]
    
    @staticmethod
    def get_extra_module_names() -> List[str]:
        return ["fa_q", "fa_k", "fa_v"]

    @staticmethod
    def process_weights_after_loading(layer):
        fa_qscale = layer.fa_q.scale
        fa_kscale = layer.fa_k.scale
        fa_vscale = layer.fa_v.scale
        repeated_query_scale = layer.fa_q.scale.repeat(1, 128)
        layer.fa_qscale = torch.nn.Parameter(repeated_query_scale, requires_grad=False)
        repeated_query_offset = layer.fa_q.offset.repeat(1, 128)
        layer.fa_qoffset = torch.nn.Parameter(repeated_query_offset, requires_grad=False)
        repeated_fa_kscale = layer.fa_k.scale.repeat(1, 128)
        layer.fa_kscale = torch.nn.Parameter(repeated_fa_kscale, requires_grad=False)
        repeated_fa_koffset = layer.fa_k.offset.repeat(1, 128)
        layer.fa_koffset = torch.nn.Parameter(repeated_fa_koffset, requires_grad=False)
        repeated_fa_vscale = layer.fa_v.scale.repeat(1, 128)
        layer.fa_vscale = torch.nn.Parameter(repeated_fa_vscale, requires_grad=False)
        repeated_fa_voffset = layer.fa_v.offset.repeat(1, 128)
        layer.fa_voffset = torch.nn.Parameter(repeated_fa_voffset, requires_grad=False)
        
        if fa_kscale.shape[0] <= 0:
            raise ValueError("Expected size of fa_kscale in dimension 0 should be greater than 0"
                             f"but got {fa_kscale.shape[0]}.")
        gqa_size = fa_qscale.shape[0] // fa_kscale.shape[0]
        fa3_k_scale, fa3_v_scale = fa_kscale.repeat(1, gqa_size).view(-1, 1), fa_vscale.repeat(1, gqa_size).view(-1, 1)
        qk_scale = torch.nn.Parameter(
            torch.squeeze(fa_qscale * fa3_k_scale).to(torch.float),
            requires_grad=False)
        layer.register_parameter("qk_scale", qk_scale)
        fa3_v_scale = torch.nn.Parameter(
            torch.squeeze(fa3_v_scale).contiguous().to(torch.float),
            requires_grad=False)
        layer.register_parameter("fa3_v_scale", fa3_v_scale)

    @classmethod
    def apply_opt_lv1(
        cls,
        layer: torch.nn.Module,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        *extra_args,
        **optional_args
    ) -> torch.Tensor:
        key_cache, value_cache, scale, block_tables, \
            is_prefill, mask, slots, output = extra_args
        seq_lens_tensor_cpu = optional_args.get("seq_lens_tensor_cpu", None)
        if is_prefill: 
            if key_cache is not None:
                key_int8 = quant_per_tensor(
                    key,
                    layer.fa_kscale,
                    layer.fa_koffset,
                )
                value_int8 = quant_per_tensor(
                    value,
                    layer.fa_vscale,
                    layer.fa_voffset,
                )
                ops.reshape_and_cache(key_int8, value_int8, key_cache, value_cache, slots)
            if (block_tables is None or block_tables.numel() == 0):
                if mask is None:
                    raise ValueError("attn_metadata.attn_mask is Null. Please check.")
                output = ops.unpad_flash_attention(query=query, key=key, value=value,
                                                   num_kv_heads=layer.num_kv_heads, num_heads=layer.num_heads,
                                                   scale=scale, seq_lens=seq_lens_tensor_cpu,
                                                   mask=mask)
            else:
                raise RuntimeError(
                    "Prefix cache and chunked prefill are currently not supported when using quanzation."
                )
        else:
            if key_cache is None:
                raise ValueError("KV Cache can't be None in decoding phase. Got None. Please check.")
            query_int8 = quant_per_tensor(
                query,
                layer.fa_qscale,
                layer.fa_qoffset,
            )
            key_int8 = quant_per_tensor(
                key,
                layer.fa_kscale,
                layer.fa_koffset,
            )
            value_int8 = quant_per_tensor(
                value,
                layer.fa_vscale,
                layer.fa_voffset,
            )
            ops.reshape_and_cache(key_int8, value_int8, key_cache, value_cache, slots)
            output = ops.pa_qkvquant(query_int8, key_cache, value_cache, layer.num_kv_heads, layer.num_heads, scale,
                     block_tables, seq_lens_tensor_cpu, layer.qk_scale, layer.fa3_v_scale, query.dtype)
        return output


    @classmethod
    def apply_opt_lv2(
        cls,
        layer: torch.nn.Module,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        *extra_args,
        **optional_args
    ) -> torch.Tensor:
        return cls.apply_opt_lv1(layer, query, key, value, *extra_args, **optional_args)

    @classmethod
    def apply_opt_lv3(
        cls,
        layer: torch.nn.Module,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        *extra_args,
        **optional_args
    ) -> torch.Tensor:
        import mindie_turbo.turbo_torch as turbo_ops
        key_cache, value_cache, scale, block_tables, \
            is_prefill, mask, slots, output = extra_args
        seq_lens_tensor_cpu = optional_args.get("seq_lens_tensor_cpu", None)
        if is_prefill: 
            if key_cache is not None:
                query, key = turbo_ops.rotary_embedding(
                    cls.cls_metadata.positions,
                    query,
                    key,
                    cls.cls_metadata.cos_sin_cache,
                    cls.cls_metadata.head_size,
                    cls.cls_metadata.is_neox_style
                )
                key_int8 = quant_per_tensor(
                    key,
                    layer.fa_kscale,
                    layer.fa_koffset,
                )
                value_int8 = quant_per_tensor(
                    value,
                    layer.fa_vscale,
                    layer.fa_voffset,
                )
                ops.reshape_and_cache(key_int8, value_int8, key_cache, value_cache, slots)
            else:
                query, key = turbo_ops.rotary_embedding(
                    cls.cls_metadata.positions,
                    query,
                    key,
                    cls.cls_metadata.cos_sin_cache,
                    cls.cls_metadata.head_size,
                    cls.cls_metadata.is_neox_style
                )
            if mask is None:
                raise ValueError("attn_metadata.attn_mask is Null. Please check.")
            output = ops.unpad_flash_attention(query=query, key=key, value=value,
                                                num_kv_heads=layer.num_kv_heads, num_heads=layer.num_heads,
                                                scale=scale, seq_lens=seq_lens_tensor_cpu,
                                                mask=mask)
        else:
            if key_cache is None:
                raise ValueError("KV Cache can't be None in decoding phase. Got None. Please check.")

            query_int8, key_int8 = turbo_ops.rotary_embedding_quant(
                cls.cls_metadata.positions,
                query,
                key,
                cls.cls_metadata.cos_sin_cache,
                layer.fa_qscale,
                layer.fa_kscale,
                layer.fa_qoffset,
                layer.fa_koffset,
                cls.cls_metadata.head_size,
                cls.cls_metadata.is_neox_style
            )
            value_int8 = quant_per_tensor(
                value,
                layer.fa_vscale,
                layer.fa_voffset,
            )
            ops.reshape_and_cache(key_int8, value_int8, key_cache, value_cache, slots)
            output = ops.pa_qkvquant(query_int8, key_cache, value_cache, layer.num_kv_heads, layer.num_heads, scale,
                     block_tables, seq_lens_tensor_cpu, layer.qk_scale, layer.fa3_v_scale, query.dtype)
        return output


    @classmethod
    def apply(
        cls,
        layer: torch.nn.Module,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        *extra_args,
        **optional_args
    ) -> torch.Tensor:
        opt_lv = int(os.getenv("VLLM_OPTIMIZATION_LEVEL", "2"))
        if opt_lv <= 1:
            return cls.apply_opt_lv1(layer, query, key, value, *extra_args, **optional_args)
        elif opt_lv == 2:
            return cls.apply_opt_lv2(layer, query, key, value, *extra_args, **optional_args)
        elif opt_lv == 3:
            return cls.apply_opt_lv3(layer, query, key, value, *extra_args, **optional_args)
        else:
            raise RuntimeError(f"unexpected optimization level {opt_lv}")


    @classmethod
    def set_attn_metadata(
        cls,
        **kwargs
    ) -> None:
        # update FAMetaData for further optimization
        
        if cls.cls_metadata is None:
            cls.cls_metadata = AscendFAMetaData(**kwargs)
            return 
        cls.cls_metadata.__dict__.update(**kwargs)


    @classmethod
    def create_weights(
        cls,
        layer: torch.nn.Module
    ) -> Dict[str, Any]:
        extra_module_names = cls.get_extra_module_names()
        for name in extra_module_names:
            setattr(layer, name, torch.nn.Module())

        params_dtype = torch.get_default_dtype()

        params_dict = {}
        
        params_dict["fa_q.scale"] = torch.empty((layer.num_heads, 1), dtype=params_dtype)
        params_dict["fa_q.offset"] = torch.empty((layer.num_heads, 1), dtype=torch.int8)
        params_dict["fa_k.scale"] = torch.empty((layer.num_kv_heads, 1), dtype=params_dtype)
        params_dict["fa_k.offset"] = torch.empty((layer.num_kv_heads, 1), dtype=torch.int8)
        params_dict["fa_v.scale"] = torch.empty((layer.num_kv_heads, 1), dtype=params_dtype)
        params_dict["fa_v.offset"] = torch.empty((layer.num_kv_heads, 1), dtype=torch.int8)

        for name, weight in params_dict.items():
            module_name, weight_name = name.split('.')
            module = getattr(layer, module_name)
            module.register_parameter(
                weight_name, torch.nn.Parameter(weight, requires_grad=False))