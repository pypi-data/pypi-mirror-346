# Copyright (c) Huawei Technologies Co., Ltd. 2024-2025. All rights reserved.
# MindIE is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import os
from typing import Dict, Any, Optional

import torch

from mindie_turbo.adaptor.base_turbo import TurboPatch
from .w8a8 import AscendW8A8LinearMethod
from .w8a8_dynamic import AscendW8A8DynamicLinearMethod, AscendW8A8DynamicFusedMoEMethod
from .faquant import AscendFAQuantAttentionMethod


class MindIETurboQuantizer:
    _instance = None

    def __init__(self, quant_description):
        for name in quant_description.keys():
            if "norm.bias" in name:
                TurboPatch.activate_extra_patches("anti_outlier")
                break

    @staticmethod
    def build_linear_method():
        raise NotImplementedError("Linear method is not implemented for the current quant type.")

    @staticmethod
    def build_moe_method():
        raise NotImplementedError("MoE method is not implemented for the current quant type.")

    @staticmethod
    def build_attention_method():
        raise NotImplementedError("Attention method is not implemented for the current quant type.")

    @staticmethod
    def get_linear_quant_type(quant_description: Dict[str, Any], prefix: str, packed_modules_mapping: Dict[str, Any]):
        proj_name = prefix.split(".")[-1]
        if proj_name in packed_modules_mapping:
            quant_type = None
            shard_prefixes = [
                prefix.replace(proj_name, shard_proj_name)
                for shard_proj_name in packed_modules_mapping[proj_name]
            ]
            for shard_prefix in shard_prefixes:
                shard_quant_type = quant_description[shard_prefix + '.weight']

                if quant_type is None:
                    quant_type = shard_quant_type
                elif shard_quant_type != quant_type:
                    raise ValueError(
                        f"Not all shards of {prefix} are quantized with same quant type."
                        f"Shard {proj_name} uses {shard_quant_type}, but another shard"
                        f"use {quant_type}. Please check quantization config.")
        else:
            quant_type = quant_description[prefix + '.weight']
        return quant_type

    @classmethod
    def get_quantizer(cls, quant_description: Dict[str, Any], prefix: str,
                      packed_modules_mapping: Optional[Dict[str, Any]] = None):
        if packed_modules_mapping is None:
            packed_modules_mapping = dict()
        # Attention
        if '.attn' in prefix and 'fa_quant_type' in quant_description.keys():
            quant_type = quant_description['fa_quant_type']
        # Linear
        else:
            quant_type = cls.get_linear_quant_type(quant_description, prefix, packed_modules_mapping)
        if quant_type in SUPPORT_ASCEND_QUANTIZER_TYPE.keys():
            cls = SUPPORT_ASCEND_QUANTIZER_TYPE[quant_type]
            if not cls._instance:
                cls._instance = cls(quant_description)
            return cls._instance
        raise NotImplementedError("Currently, MindIE-Turbo only supports following quant types:" \
                                  f"{list(SUPPORT_ASCEND_QUANTIZER_TYPE.keys())}")


class W8A8Quantizer(MindIETurboQuantizer):
    @staticmethod
    def build_linear_method():
        return AscendW8A8LinearMethod()


class FAQuantizer(MindIETurboQuantizer):
    def __init__(self, quant_description):
        opt_lv = int(os.getenv("VLLM_OPTIMIZATION_LEVEL", "2"))
        if opt_lv > 2:
            TurboPatch.activate_extra_patches("rope_quant_fusion")
        TurboPatch.is_faquant = True
        super().__init__(quant_description)

    @staticmethod
    def build_attention_method():
        return AscendFAQuantAttentionMethod()


class W8A8DYNAMICQuantizer(MindIETurboQuantizer):
    @staticmethod
    def build_linear_method():
        return AscendW8A8DynamicLinearMethod()

    @staticmethod
    def build_moe_method():
        return AscendW8A8DynamicFusedMoEMethod()


SUPPORT_ASCEND_QUANTIZER_TYPE = {
    "W8A8": W8A8Quantizer,
    "FAQuant": FAQuantizer,
    "W8A8_DYNAMIC": W8A8DYNAMICQuantizer,
}
