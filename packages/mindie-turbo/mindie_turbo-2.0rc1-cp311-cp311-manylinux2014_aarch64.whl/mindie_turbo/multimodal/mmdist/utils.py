# Copyright (c) Huawei Technologies Co., Ltd. 2024-2025. All rights reserved.

import math
import torch
import torch_npu
import torch.distributed as dist


def get_rank_world():
    rank = dist.get_rank()
    world_size = dist.get_world_size()
    return rank, world_size


def extract_local(x, dim, rank, world_size, *args, **kwargs):
    return x.chunk(world_size, dim=dim)[rank].detach().clone()


def pad_to_divisible(x, world_size):
    batch_size = x.size(0)
    padding_size = math.ceil(batch_size / world_size) * world_size - batch_size
    if padding_size > 0:
        padding = torch.zeros(
            padding_size, *x.size()[1:], dtype=x.dtype, device=x.device
        )
        x = torch.cat([x, padding], dim=0)

    return x
