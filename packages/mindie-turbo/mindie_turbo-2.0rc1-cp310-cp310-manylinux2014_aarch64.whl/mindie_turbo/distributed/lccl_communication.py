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


def lccl_broadcast(
    data: torch.Tensor,
    rank: int,
    world_size: int,
    src: int = 0,
):
    ops.lccl_broadcast(data, rank, world_size, src)


def lccl_allreduce(
    data: torch.Tensor,
    rank: int,
    world_size: int,
):
    ops.lccl_allreduce(data, rank, world_size)


def lccl_allgather(
    data: torch.Tensor,
    rank: int,
    world_size: int,
) -> torch.Tensor:
    return ops.lccl_allgather(data, rank, world_size)
