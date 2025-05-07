# Adapted from
# https://github.com/vllm-project/vllm/blob/main/vllm/distributed/parallel_state.py

# SPDX-License-Identifier: Apache-2.0

# Copyright 2023 The vLLM team.
# Adapted from
# https://github.com/NVIDIA/Megatron-LM/blob/main/megatron/core/parallel_state.py
# Copyright (c) 2022, NVIDIA CORPORATION. All rights reserved.

# Copyright (c) Huawei Technologies Co., Ltd. 2024-2025. All rights reserved.

from typing import Any, Dict, List, Optional, Tuple, Union
import torch
from torch.distributed import ProcessGroup
from vllm.distributed.parallel_state import _split_tensor_dict, TensorMetadata

from mindie_turbo.distributed.lccl_communication import (
    lccl_broadcast,
    lccl_allreduce,
    lccl_allgather,
)


def broadcast_tensor_dict_with_lccl(
    self,
    tensor_dict: Optional[Dict[str, Union[torch.Tensor, Any]]] = None,
    src: int = 0,
    group: Optional[ProcessGroup] = None,
    metadata_group: Optional[ProcessGroup] = None,
) -> Optional[Dict[str, Union[torch.Tensor, Any]]]:
    """Broadcast the input tensor dictionary.
    NOTE: `src` is the local rank of the source rank.
    """
    # Bypass the function if we are using only 1 GPU.
    if not torch.distributed.is_initialized() or self.world_size == 1:
        return tensor_dict

    group = self.device_group
    metadata_group = self.cpu_group
    if src >= self.world_size:
        raise RuntimeError(f"Invalid src rank ({src})")

    rank_in_group = self.rank_in_group
    if rank_in_group == src:
        metadata_list: List[Tuple[Any, Any]] = []
        if not isinstance(tensor_dict, dict):
            raise RuntimeError(
                f"Expecting a dictionary, got {type(tensor_dict)}"
            )
        metadata_list, tensor_list = _split_tensor_dict(tensor_dict)
        # `metadata_list` lives in CPU memory.
        # `broadcast_object_list` has serialization & deserialization,
        # all happening on CPU. Therefore, we can use the CPU group.
        self.broadcast_object(metadata_list, src=src)
        for tensor in tensor_list:
            if tensor.numel() == 0:
                # Skip broadcasting empty tensors.
                continue
            lccl_broadcast(tensor, rank_in_group, self.world_size, src)
    else:
        metadata_list = self.broadcast_object(None, src=src)
        tensor_dict = {}
        for key, value in metadata_list:
            if isinstance(value, TensorMetadata):
                tensor = torch.empty(
                    value.size, dtype=value.dtype, device=value.device
                )
                if tensor.numel() == 0:
                    # Skip broadcasting empty tensors.
                    tensor_dict[key] = tensor
                    continue
                lccl_broadcast(tensor, rank_in_group, self.world_size, src)
                tensor_dict[key] = tensor
            else:
                tensor_dict[key] = value
    return tensor_dict


def all_reduce_with_lccl(self, x: torch.Tensor) -> torch.Tensor:
    lccl_allreduce(x, self.rank, self.world_size)
    return x


def all_gather_with_lccl(
    self, input_: torch.Tensor, dim: int = -1
) -> torch.Tensor:
    if dim < 0:
        # Convert negative dim to positive.
        dim += input_.dim()
    input_size = input_.size()
    # Lccl All-gather.
    output_tensor = lccl_allgather(input_, self.rank, self.world_size)
    # Reshape
    output_tensor = output_tensor.reshape((self.world_size,) + input_size)
    output_tensor = output_tensor.movedim(0, dim)
    output_tensor = output_tensor.reshape(
        input_size[:dim]
        + (self.world_size * input_size[dim],)
        + input_size[dim + 1:]
    )
    return output_tensor
