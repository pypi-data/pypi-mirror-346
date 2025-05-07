# Part of this file was copied from the vLLM team, vLLM project,
# adapted from vllm-ascend/vllm-ascend/ops/layernorm.py
#
# Copyright (c) 2025 Huawei Technologies Co., Ltd. All Rights Reserved.
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
# Copyright (c) Huawei Technologies Co., Ltd. 2024-2025. All rights reserved.

from typing import Any, Dict, Generator, List, Optional, Tuple, Union

import torch
import torch_npu

from mindie_turbo import _ops as ops


def rms_norm_mki_forward_oot(
    self,
    x: torch.Tensor,
    residual: Optional[torch.Tensor] = None,
) -> Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
    if residual is not None:
        x, _, residual = torch_npu.npu_add_rms_norm(x, residual, self.weight,
                                                    self.variance_epsilon)
        return x, residual

    out = torch.empty(x.shape, dtype=x.dtype, device=x.device)
    ops.rms_norm(out, x, self.weight, self.variance_epsilon)
    return out
