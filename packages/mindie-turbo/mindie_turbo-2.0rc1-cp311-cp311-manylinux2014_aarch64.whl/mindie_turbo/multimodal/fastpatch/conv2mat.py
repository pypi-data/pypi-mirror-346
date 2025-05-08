# Copyright (c) Huawei Technologies Co., Ltd. 2024-2025. All rights reserved.

import torch


def patch_based_conv2d_linear(conv_layer, pixel_values):
    """
    Perform patch-based convolution using a linear layer.
    Automatically handles bias using the linear layer's built-in bias.
    
    Args:
        conv_layer: The convolutional layer with weight and optional bias.
        pixel_values: Input tensor of shape [B, C, H, W].
    
    Returns:
        patch_embeds: Output tensor of shape [B, nH * nW, out_channels].
    """
    # Check if weight has already been transformed
    if not hasattr(conv_layer, 'linear_layer'):
        conv_weight_matrix = conv_layer.weight.data.flatten(1)
        
        in_channels = conv_weight_matrix.size(1)
        out_channels = conv_weight_matrix.size(0)
        if conv_layer.bias is not None:
            linear_layer = nn.Linear(in_channels, out_channels, bias=True)
            linear_layer.weight.data = conv_weight_matrix
            linear_layer.bias.data = conv_layer.bias.data
        else:
            linear_layer = nn.Linear(in_channels, out_channels, bias=False)
            linear_layer.weight.data = conv_weight_matrix
        del conv_layer.weight
        del conv_layer.bias
        conv_layer.linear_layer = linear_layer
    else:
        linear_layer = conv_layer.linear_layer

    patch_height, patch_width = conv_layer.kernel_size
    batch_size, channels, height, width = pixel_values.shape
        
    num_height = height // patch_height
    num_width = width // patch_width

    patch_values = pixel_values.view(
        batch_size, channels, num_height, patch_height, num_width, patch_width
    )
    patch_values = patch_values.permute(0, 2, 4, 1, 3, 5)
    patch_values = patch_values.reshape(
        batch_size, num_height * num_width, channels * patch_height * patch_width
    )

    patch_embeds = linear_layer(patch_values)

    return patch_embeds


def patch_based_conv3d_linear(conv_layer, pixel_values):
    """
    Perform patch-based 3D convolution using a linear layer.
    Automatically handles bias using the linear layer's built-in bias.

    Args:
        conv_layer: The 3D convolutional layer with weight and optional bias.
        pixel_values: Input tensor of shape [B, C, D, H, W].

    Returns:
        patch_embeds: Output tensor of shape [B, nD * nH * nW, out_channels].
    """
    if not hasattr(conv_layer, 'linear_layer'):
        conv_weight_matrix = conv_layer.weight.data.flatten(1)
        
        in_channels = conv_weight_matrix.size(1)
        out_channels = conv_weight_matrix.size(0)
        if conv_layer.bias is not None:
            linear_layer = nn.Linear(in_channels, out_channels, bias=True)
            linear_layer.weight.data = conv_weight_matrix
            linear_layer.bias.data = conv_layer.bias.data
        else:
            linear_layer = nn.Linear(in_channels, out_channels, bias=False)
            linear_layer.weight.data = conv_weight_matrix
        del conv_layer.weight
        del conv_layer.bias
        conv_layer.linear_layer = linear_layer
    else:
        linear_layer = conv_layer.linear_layer

    patch_depth, patch_height, patch_width = conv_layer.kernel_size
    batch_size, channels, depth, height, width = pixel_values.shape
        
    num_depth = depth // patch_depth
    num_height = height // patch_height
    num_width = width // patch_width

    patch_values = pixel_values.view(
        batch_size, channels, 
        num_depth, patch_depth, 
        num_height, patch_height, num_width, patch_width
    )
    patch_values = patch_values.permute(0, 2, 4, 6, 1, 3, 5, 7)
    patch_values = patch_values.reshape(
        batch_size, 
        num_depth * num_height * num_width, 
        channels * patch_depth * patch_height * patch_width
    )

    patch_embeds = linear_layer(patch_values)

    return patch_embeds
    