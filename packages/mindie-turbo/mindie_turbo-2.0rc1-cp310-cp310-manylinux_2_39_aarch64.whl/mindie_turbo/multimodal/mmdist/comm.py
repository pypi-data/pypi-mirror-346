# Copyright (c) Huawei Technologies Co., Ltd. 2024-2025. All rights reserved.
# Copyright (c) Microsoft Corporation

import torch
import torch_npu
import torch.distributed as dist


def all_to_all_3d(
    input_tensor: torch.tensor, is_seq_to_head: bool, group=None, use_sync: bool = False
) -> torch.tensor:
    """
    Perform all-to-all communication for sequence parallelism.

    Args:
        input_tensor (torch.tensor): A 3D tensor sharded along either the sequence or head dimension.
        is_seq_to_head (bool): If True, scatter sequence dim and gather head dim;
                               if False, scatter head dim and gather sequence dim.
        group: torch process group.
        use_sync (bool): Whether to synchronize after all-to-all.

    Returns:
        torch.tensor: Resharded tensor.
    """
    seq_world_size = dist.get_world_size(group)

    if is_seq_to_head:
        # Scatter sequence dim, gather head dim
        # input_tensor: (seqlen/P, hc, hs) output: (seqlen, hc/P, hs)
        shard_seqlen, hc, hs = input_tensor.shape
        seqlen = shard_seqlen * seq_world_size
        shard_hc = hc // seq_world_size

        # Reshape and transpose for scattering
        # (seqlen/P, hc, hs) -reshape-> (seq_len/P, P, hc/P, hs) -transpose(0,2)-> (P, seq_len/P, hc/P, hs)
        input_t = (
            input_tensor.reshape(shard_seqlen, seq_world_size, shard_hc, hs)
            .transpose(0, 1)
            .contiguous()
        )

        output = torch.empty_like(input_t)
        if seq_world_size > 1:
            dist.all_to_all_single(output, input_t, group=group)
            if use_sync:
                torch.cuda.synchronize()
        else:
            output = input_t
        # Reshape back to (seqlen, hc/P, hs)
        output = output.reshape(seqlen, shard_hc, hs)
        return output

    else:
        # Scatter head dim, gather sequence dim
        # input_tensor: (seqlen, hc/P, hs) output: (seqlen/P, hc, hs)
        seqlen, shard_hc, hs = input_tensor.shape
        hc = shard_hc * seq_world_size
        shard_seqlen = seqlen // seq_world_size

        # Reshape and transpose for scattering
        # (seqlen, hc/P, hs) -reshape-> (P, seq_len/P, hc/P, hs)
        # -transpose(0, 3)-> (hc/P, P, seqlen/P, bs, hs) 
        # -transpose(0, 1) -> (P, hc/P, seqlen/P, hs)
        input_t = (
            input_tensor.reshape(seq_world_size, shard_seqlen, shard_hc, hs)
            .transpose(1, 2)
            .contiguous()
        )

        output = torch.empty_like(input_t)
        if seq_world_size > 1:
            dist.all_to_all_single(output, input_t, group=group)
            if use_sync:
                torch.cuda.synchronize()
        else:
            output = input_t

        # Reshape back to (seqlen/P, hc, hs)
        # (hc, seqlen/P, hs) -tranpose(0,1)-> (seqlen/P, hc, hs)
        output = output.reshape(hc, shard_seqlen, hs).transpose(0, 1).contiguous()
        return output


def all_to_all_4d(
    input_tensor: torch.tensor, is_seq_to_head: bool, group=None, use_sync: bool = False
) -> torch.tensor:
    """
    Perform all-to-all communication for sequence parallelism on 4D tensors.

    Args:
        input_tensor (torch.tensor): A 4D tensor sharded along either the sequence or head dimension.
        is_seq_to_head (bool): If True, scatter sequence dim and gather head dim;
                              if False, scatter head dim and gather sequence dim.
        group: torch process group.
        use_sync (bool): Whether to synchronize after all-to-all.

    Returns:
        torch.tensor: Resharded tensor.
    """
    seq_world_size = dist.get_world_size(group)

    if is_seq_to_head:
        # Scatter sequence dim, gather head dim
        # input_tensor: (bs, seqlen/P, hc, hs) output: (bs, seqlen, hc/P, hs)
        bs, shard_seqlen, hc, hs = input_tensor.shape
        seqlen = shard_seqlen * seq_world_size
        shard_hc = hc // seq_world_size

        # Reshape and transpose for scattering
        # (bs, seqlen/P, hc, hs) -reshape-> (bs, seqlen/P, P, hc/P, hs) -transpose(0,2)-> (P, seqlen/P, bs, hc/P, hs)
        input_t = (
            input_tensor.reshape(bs, shard_seqlen, seq_world_size, shard_hc, hs)
            .transpose(0, 2)
            .contiguous()
        )

        output = torch.empty_like(input_t)
        if seq_world_size > 1:
            dist.all_to_all_single(output, input_t, group=group)
            if use_sync:
                torch.cuda.synchronize()
        else:
            output = input_t

        # Reshape back to (bs, seqlen, hc/P, hs)
        output = output.reshape(seqlen, bs, shard_hc, hs).transpose(0, 1).contiguous()
        return output

    else:
        # Scatter head dim, gather sequence dim
        # input_tensor: (bs, seqlen, hc/P, hs) output: (bs, seqlen/P, hc, hs)
        bs, seqlen, shard_hc, hs = input_tensor.shape
        hc = shard_hc * seq_world_size
        shard_seqlen = seqlen // seq_world_size

        # Reshape and transpose for scattering
        # (bs, seqlen, hc/P, hs) -reshape-> (bs, P, seqlen/P, hc/P, hs)
        # -transpose(0,3)-> (hc/P, P, seqlen/P, bs, hs)
        # -transpose(0,1)-> (P, hc/P, seqlen/P, bs, hs)
        input_t = (
            input_tensor.reshape(bs, seq_world_size, shard_seqlen, shard_hc, hs)
            .transpose(0, 3)
            .transpose(0, 1)
            .contiguous()
            .reshape(seq_world_size, shard_hc, shard_seqlen, bs, hs)
        )

        output = torch.empty_like(input_t)
        if seq_world_size > 1:
            dist.all_to_all_single(output, input_t, group=group)
            if use_sync:
                torch.cuda.synchronize()
        else:
            output = input_t

        # Reshape back to (bs, seqlen/P, hc, hs)
        output = output.reshape(hc, shard_seqlen, bs, hs).transpose(0, 2).contiguous()
        return output.reshape(bs, shard_seqlen, hc, hs)


def all_gather_2d(input_tensor: torch.tensor, world_size: int, group=None) -> torch.tensor:
    s, d = input_tensor.shape[:]
    input_gather = torch.zeros(
        world_size * s, d, dtype=input_tensor.dtype, device=input_tensor.device
    )
    dist.all_gather_into_tensor(input_gather, input_tensor, group=group)

    return input_gather
