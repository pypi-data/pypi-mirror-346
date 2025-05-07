# coding=utf-8
# Copyright 2024 The HuggingFace Inc. team.
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

from functools import lru_cache, partial
from typing import Any, Dict, Iterable, List, Optional, Tuple, TypedDict, Union

import numpy as np
import torch
import torchvision
import torchvision_npu
from torchvision.transforms import functional as F
import transforms
from transformers.image_processing_utils import (
    BaseImageProcessor,
    BatchFeature,
    get_size_dict,
)
from transformers.image_transforms import (
    convert_to_rgb,
    get_resize_output_image_size,
)
from transformers.image_utils import (
    ChannelDimension,
    ImageInput,
    ImageType,
    SizeDict,
    get_image_size,
    get_image_type,
    infer_channel_dimension_format,
)
from PIL import Image


def is_dvpp_read(image: ImageInput):
    dvpp_flag = (
        isinstance(image, torch.Tensor)
        and infer_channel_dimension_format(image) == ChannelDimension.FIRST
        and image.device.type == "npu"
    )
    return dvpp_flag


def prepare_image(
    image: ImageInput,
    do_convert_rgb: Optional[bool] = None,
    input_data_format: Optional[Union[str, ChannelDimension]] = None,
    device: Optional["torch.device"] = None,
) -> "torch.Tensor":

    image_type = get_image_type(image)
    if image_type not in [ImageType.PIL, ImageType.TORCH, ImageType.NUMPY]:
        raise ValueError(f"Unsupported input image type {image_type}")

    if do_convert_rgb:
        image = convert_to_rgb(image)

    if image_type == ImageType.PIL:
        image = F.pil_to_tensor(image)
    elif image_type == ImageType.NUMPY:
        # not using F.to_tensor as it doesn't handle (C, H, W) numpy arrays
        image = torch.from_numpy(image).contiguous()

    # Infer the channel dimension format if not provided
    if input_data_format is None:
        input_data_format = infer_channel_dimension_format(image)

    if input_data_format == ChannelDimension.LAST:
        # We force the channel dimension to be first for torch tensors as this is what torchvision expects.
        image = image.permute(2, 0, 1).contiguous()

    # Now that we have torch tensors, we can move them to the right device
    if device is not None:
        image = image.to(device)

    return image


def reshape_9d(patches, target_shape):
    # aclnnInplaceCopy cannot be larger than 8 dimensions
    grid_t = patches.shape[0]
    target_shape_new = ((target_shape[0] // grid_t),) + target_shape[1:]
    all_batches = []
    for i in range(grid_t):
        batch = patches[i]
        flattened_batch = batch.reshape(target_shape_new)
        all_batches.append(flattened_batch)
    flatten_patches = torch.cat(all_batches, dim=0)
    return flatten_patches


def read_image_npu(image_path):
    torchvision.set_image_backend("npu")
    # Use Torchvision to read images and output NPU tensors.
    try:
        image_obj = torchvision.datasets.folder.default_loader(image_path)
    except Exception as e:
        raise RuntimeError("Open image failed.") from e
    if isinstance(image_obj, Image.Image):
        image_obj = (
            transforms.functional.pil_to_tensor(image_obj).contiguous().to("npu")
        )
    return image_obj
