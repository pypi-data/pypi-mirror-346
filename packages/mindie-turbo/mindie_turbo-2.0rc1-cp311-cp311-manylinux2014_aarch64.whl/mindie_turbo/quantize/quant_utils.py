# Copyright (c) Huawei Technologies Co., Ltd. 2024-2025. All rights reserved.
# MindIE is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import torch
import torch_npu

from mindie_turbo import _ops as ops


SRC_DTYPE_TO_ACL_DTYPE = {
    torch.float16: 1,
    torch.bfloat16: 27,
}


def quant_per_tensor(
    in_tensor: torch.Tensor,
    input_scale: torch.Tensor,
    input_offset: torch.Tensor
) -> None:
    return ops.quant_pertensor(
        in_tensor,
        input_scale,
        input_offset
    )