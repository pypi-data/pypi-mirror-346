# Copyright (c) Huawei Technologies Co., Ltd. 2024-2025. All rights reserved.
# MindIE is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import mindie_turbo.env as envs
from mindie_turbo.adaptor.base_turbo import BaseTurbo, TurboPatch
from mindie_turbo.adaptor.vllm.model_executor.logits_processor import (
    forward_with_allgather,
)
from mindie_turbo.adaptor.vllm.quantize import (
    ascend_faquant_attention_turbo_fwd_impl,
    fake_rope_forward_oot,
    wrapper_rmsnorm_forward_oot,
    wrapper_rmsnorm_init,
    ascend_faquant_attention_turbo_fwd_impl_v1,
)
from mindie_turbo.adaptor.vllm.weight_utils import (
    wrapper_load_model,
    wrapper_weights_iterator,
)
from mindie_turbo.multimodal.mmdist.qwen2_vl_vit import (
    CustomQwen2VisionAttention,
    CustomQwen2VisionBlock,
    CustomQwen2VisionMLP,
    CustomQwen2VisionPatchMerger,
    CustomQwen2VisionTransformer,
    CustomQwen2VLForConditionalGeneration,
)
from mindie_turbo.utils.logger import logger

DECORATE = "decorate"


class VLLMTurbo(BaseTurbo):
    """VLLM specific Turbo optimization implementation."""

    def check_environment(self) -> None:
        try:
            import torch_npu
        except ImportError as e:
            raise RuntimeError(
                "Failed to import torch_npu, please install it first."
            ) from e

    def setup_environment(self) -> None:
        pass

    def register_patches(self, level: int) -> None:
        """Register vLLM specific optimization patches.
        Level 0: No optimization activated.
        Level 1: Normal optimization approaches, minimizing risks.
        Level 2: Use different kernels, might cause accuracy change.
        Level 3: Use kernels with high degree of fusion.
        """
        if level >= 1:
            import vllm_ascend.ops

            from mindie_turbo.adaptor.vllm.attention import (
                attention_forward_with_mki_ops,
                attention_init,
                v1_attention_forward_mki,
            )

            self.patcher.register_patch(
                "vllm.model_executor.model_loader.weight_utils.safetensors_weights_iterator",
                wrapper_weights_iterator,
                method=DECORATE,
            )
            # Use all_gather to inplace gather for better performance.
            self.patcher.register_patch(
                "vllm.model_executor.layers.logits_processor.LogitsProcessor.forward",
                forward_with_allgather,
                force=True,
            )
            self.patcher.register_patch(
                "vllm.attention.layer.Attention.__init__",
                attention_init,
                force=True,
            )

            self.patcher.register_patch(
                "vllm_ascend.attention.attention.AscendAttentionBackendImpl.forward",
                attention_forward_with_mki_ops,
                force=True,
            )
            self.patcher.register_patch(
                "vllm_ascend.attention.attention_v1.AscendAttentionBackendImpl.forward",
                v1_attention_forward_mki,
                force=True,
            )
            # Qwen-VL related optimization.
            self.patcher.register_patch(
                "vllm_ascend.models.qwen2_vl.CustomQwen2VLForConditionalGeneration",
                CustomQwen2VLForConditionalGeneration,
                force=True,
            )
            self.patcher.register_patch(
                "vllm_ascend.models.qwen2_vl.CustomQwen2VisionTransformer",
                CustomQwen2VisionTransformer,
                force=True,
            )
            self.patcher.register_patch(
                "vllm.model_executor.models.qwen2_vl.Qwen2VisionPatchMerger",
                CustomQwen2VisionPatchMerger,
                force=True,
            )
            self.patcher.register_patch(
                "vllm_ascend.models.qwen2_vl.CustomQwen2VisionBlock",
                CustomQwen2VisionBlock,
                force=True,
            )
            self.patcher.register_patch(
                "vllm_ascend.models.qwen2_vl.CustomQwen2VisionAttention",
                CustomQwen2VisionAttention,
                force=True,
            )
            self.patcher.register_patch(
                "vllm.model_executor.models.qwen2_vl.Qwen2VisionMLP",
                CustomQwen2VisionMLP,
                force=True,
            )

        if level >= 2:
            from mindie_turbo.adaptor.vllm.layernorm import (
                rms_norm_mki_forward_oot,
            )
            from mindie_turbo.adaptor.vllm.model_executor.linear import (
                linear_with_pp_matmul,
            )
            from mindie_turbo.adaptor.vllm.ops import rope_forward_oot
            from mindie_turbo.functional.activation import silu_and_mul_mki

            self.patcher.register_patch(
                "vllm.model_executor.layers.activation.SiluAndMul.forward_oot",
                silu_and_mul_mki,
                force=True,
            )
            self.patcher.register_patch(
                "vllm.model_executor.layers.layernorm.RMSNorm.forward_oot",
                rms_norm_mki_forward_oot,
            )
            self.patcher.register_patch(
                "vllm.model_executor.layers.rotary_embedding.RotaryEmbedding.forward_oot",
                rope_forward_oot,
                force=True,
            )
            self.patcher.register_patch(
                "vllm.model_executor.layers.linear.UnquantizedLinearMethod.apply",
                linear_with_pp_matmul,
                force=True,
            )
            self.patcher.register_patch(
                "vllm_ascend.worker.model_runner.NPUModelRunnerBase.load_model",
                wrapper_load_model,
                method="decorate",
                force=True,
            )
            self.patcher.register_patch(
                "vllm_ascend.worker.model_runner_v1.NPUModelRunner.load_model",
                wrapper_load_model,
                method="decorate",
                force=True,
            )

        if level >= 3:
            self.patcher.register_patch(
                "vllm.model_executor.layers.rotary_embedding.RotaryEmbedding.forward_oot",
                fake_rope_forward_oot,
                force=True,
            )

    def register_extra_patches(self) -> None:
        """Register extra patches that are not activated when import vllm_turbo"""
        rmsnorm_init_target = (
            "vllm.model_executor.layers.layernorm.RMSNorm.__init__"
        )
        rmsnorm_forward_oot_target = (
            "vllm.model_executor.layers.layernorm.RMSNorm.forward_oot"
        )
        turbo_faquant_attention_oot_target = (
            "vllm_ascend.attention.attention.AscendAttentionBackendImpl.forward"
        )
        turbo_model_runner_load_model_target = (
            "vllm_ascend.worker.model_runner.NPUModelRunnerBase.load_model"
        )
        turbo_faquant_attention_oot_v1_target = (
            "vllm_ascend.attention.attention_v1.AscendAttentionBackendImpl.forward"
        )
        self.patcher.register_patch(
            turbo_faquant_attention_oot_v1_target,
            ascend_faquant_attention_turbo_fwd_impl_v1,
            force=True,
        )
        self.patcher.register_patch(
            rmsnorm_init_target,
            wrapper_rmsnorm_init,
            method=DECORATE,
        )
        self.patcher.register_patch(
            rmsnorm_forward_oot_target,
            wrapper_rmsnorm_forward_oot,
            method=DECORATE,
        )
        self.patcher.register_patch(
            turbo_faquant_attention_oot_target,
            ascend_faquant_attention_turbo_fwd_impl,
            force=True,
        )
        self.extra_patch_mapping["anti_outlier"] = [
            rmsnorm_init_target,
            rmsnorm_forward_oot_target,
        ]
        self.extra_patch_mapping["rope_quant_fusion"] = [
            turbo_faquant_attention_oot_target,
            turbo_faquant_attention_oot_v1_target
        ]

    def register_env_patches(self) -> None:
        if envs.USING_SAMPLING_TENSOR_CACHE == "1":
            logger.info(
                "Using sampling tensor cache to optimize sample performance. "
                "This feature has conficts with beam search and chunked-prefill, "
                "so if you are using beam search or chunked-prefill, "
                "please export USING_SAMPLING_TENSOR_CACHE=0. Note that this feature"
                "is only used in V0 vLLM."
            )
            from mindie_turbo.adaptor.vllm.sampler import (
                _apply_min_p_without_changing_minp,
                cache_sampling_tensors_decorator,
            )

            self.patcher.register_patch(
                "vllm.model_executor.layers.sampler.Sampler._init_sampling_tensors",
                cache_sampling_tensors_decorator,
                method=DECORATE,
            )

            self.patcher.register_patch(
                "vllm.model_executor.layers.sampler._apply_min_p",
                _apply_min_p_without_changing_minp,
                force=True,
            )

        if envs.USING_LCCL_COM == "1":
            logger.info(
                "Using LCCL to communicate which currently doesn't support multi-node "
                "communication. If you are running large models like DeepSeek in multi-node "
                "environment, please export USING_LCCL_COM=0."
            )
            from mindie_turbo.adaptor.vllm.distributed.parallel_state import (
                all_gather_with_lccl,
                all_reduce_with_lccl,
                broadcast_tensor_dict_with_lccl,
            )

            self.patcher.register_patch(
                "vllm.distributed.parallel_state.GroupCoordinator.broadcast_tensor_dict",
                broadcast_tensor_dict_with_lccl,
            )

            self.patcher.register_patch(
                "vllm.distributed.device_communicators.base_device_communicator.DeviceCommunicatorBase.all_reduce",
                all_reduce_with_lccl,
            )
            self.patcher.register_patch(
                "vllm.distributed.device_communicators.base_device_communicator.DeviceCommunicatorBase.all_gather",
                all_gather_with_lccl,
            )

    def activate_extra_patches(self, patch_type: str) -> None:
        """Activate patches according to given patch types.

        Args:
            patch_type: Which type of patches to be activated.
        """
        if patch_type not in self.extra_patch_mapping:
            raise ValueError(
                f"Unsupported patch_type: {patch_type}, available patch_type are {self.extra_patch_mapping.keys()}"
            )

        for target in self.extra_patch_mapping[patch_type]:
            self.patcher.patches[target].apply_patch()


# Create global instance with optimization level from environment for import
logger.info("vLLM Turbo activated.")
vllm_optimization_level = int(envs.VLLM_OPTIMIZATION_LEVEL)
vllm_turbo = VLLMTurbo()
vllm_turbo.activate(vllm_optimization_level)
vllm_turbo.register_extra_patches()
TurboPatch.set_frontend(vllm_turbo)
