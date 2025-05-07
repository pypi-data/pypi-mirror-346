# Copyright Huawei Technologies Co., Ltd. 2023-2024. All rights reserved.
# Copyright 2024 The Qwen team, Alibaba Group and the HuggingFace Inc. team. All rights reserved.
#
# This code is based on EleutherAI's GPT-NeoX library and the GPT-NeoX
# and OPT implementations in this library. It has been modified from its
# original forms to accommodate minor architectural differences compared
# to GPT-NeoX and OPT used by the Meta AI team that trained the model.
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
"""Image processor class for Qwen2-VL."""
from functools import partial
from typing import Dict, List, Optional, Union
from PIL import Image

import torch
import torchvision
import torchvision_npu
from torchvision.transforms import InterpolationMode
from torchvision.transforms import functional as F
from transformers.image_processing_utils import BatchFeature
from transformers.image_utils import (
    ChannelDimension,
    ImageInput,
    PILImageResampling,
    VideoInput,
    get_image_size,
    make_list_of_images,
    make_flat_list_of_images,
    valid_images,
    validate_preprocess_arguments,
)
from transformers.utils import TensorType, logging
from transformers.models.qwen2_vl.image_processing_qwen2_vl import (
    Qwen2VLImageProcessor,
    make_batched_videos,
    smart_resize,
)

from .image_processing_utils import read_image_npu
from .image_processing_utils import prepare_image, is_dvpp_read, reshape_9d


logger = logging.get_logger(__name__)


class Qwen2VLImageProcessorNPU(Qwen2VLImageProcessor):

    def preprocess_npu(
        self,
        images: Union[ImageInput, VideoInput],
        do_resize: bool = None,
        resample: PILImageResampling = None,
        do_rescale: bool = None,
        rescale_factor: float = None,
        do_normalize: bool = None,
        image_mean: Optional[Union[float, List[float]]] = None,
        image_std: Optional[Union[float, List[float]]] = None,
        do_convert_rgb: bool = None,
        data_format: Optional[ChannelDimension] = ChannelDimension.FIRST,
        input_data_format: Optional[Union[str, ChannelDimension]] = None,
        device: Optional[Union[str, torch.device]] = "npu",
    ):
        images = make_list_of_images(images)

        if not is_dvpp_read(images[0]):
            process_image_fn = partial(
                prepare_image,
                do_convert_rgb=do_convert_rgb,
                input_data_format=input_data_format,
                device=device,
            )
            images = [process_image_fn(image) for image in images]

        height, width = get_image_size(images[0], channel_dim=ChannelDimension.FIRST)
        resized_height, resized_width = height, width

        # Group images by size for batched resizing
        stacked_images = torch.stack(images, dim=0)  # 1,3,1372,2044, uint8
        if do_resize:
            resized_height, resized_width = smart_resize(
                height,
                width,
                factor=self.patch_size * self.merge_size,
                min_pixels=self.min_pixels,
                max_pixels=self.max_pixels,
            )
            stacked_images = F.resize(
                stacked_images,
                size=(resized_height, resized_width),
                interpolation=InterpolationMode.BICUBIC,
                antialias=True,
            ).float()

        if do_rescale:
            stacked_images = torch.mul(stacked_images, rescale_factor)

        if do_normalize:
            stacked_images = F.normalize(stacked_images, mean=image_mean, std=image_std)

        if stacked_images.shape[0] % self.temporal_patch_size != 0:
            repeats = (
                stacked_images[-1]
                .unsqueeze(0)
                .repeat(self.temporal_patch_size - 1, 1, 1, 1)
            )
            stacked_images = torch.cat([stacked_images, repeats], dim=0)

        channel = stacked_images.shape[1]
        grid_t = stacked_images.shape[0] // self.temporal_patch_size
        grid_h, grid_w = (
            resized_height // self.patch_size,
            resized_width // self.patch_size,
        )
        patches = stacked_images.view(
            grid_t,
            self.temporal_patch_size,
            channel,
            grid_h // self.merge_size,
            self.merge_size,
            self.patch_size,
            grid_w // self.merge_size,
            self.merge_size,
            self.patch_size,
        )
        patches = patches.permute(0, 3, 6, 4, 7, 2, 1, 5, 8)

        # aclnnInplaceCopy cannot be larger than 8 dimensions
        flatten_patches = reshape_9d(
            patches,
            (
                grid_t * grid_h * grid_w,
                channel * self.temporal_patch_size * self.patch_size * self.patch_size,
            ),
        )

        return flatten_patches, (grid_t, grid_h, grid_w)

    def update_if_none(self, param1, param2):
        return param1 if param1 is not None else param2

    def preprocess(
        self,
        images: ImageInput,
        videos: VideoInput = None,
        do_resize: bool = None,
        size: Dict[str, int] = None,
        resample: PILImageResampling = None,
        do_rescale: bool = None,
        rescale_factor: float = None,
        do_normalize: bool = None,
        image_mean: Optional[Union[float, List[float]]] = None,
        image_std: Optional[Union[float, List[float]]] = None,
        do_convert_rgb: bool = None,
        return_tensors: Optional[Union[str, TensorType]] = None,
        data_format: Optional[ChannelDimension] = ChannelDimension.FIRST,
        input_data_format: Optional[Union[str, ChannelDimension]] = None,
    ):
        do_resize = self.update_if_none(do_resize, self.do_resize)
        size = self.update_if_none(size, self.size)
        resample = self.update_if_none(resample, self.resample)
        rescale_factor = self.update_if_none(rescale_factor, self.rescale_factor)
        do_normalize = self.update_if_none(do_normalize, self.do_normalize)
        image_mean = self.update_if_none(image_mean, self.image_mean)
        image_std = self.update_if_none(image_std, self.image_std)
        do_convert_rgb = self.update_if_none(do_convert_rgb, self.do_convert_rgb)

        if images is not None:
            images = make_flat_list_of_images(images)
        if videos is not None:
            videos = make_batched_videos(videos)

        if images is not None and not valid_images(images):
            raise ValueError(
                "Invalid image type. Must be of type PIL.Image.Image, numpy.ndarray, "
                "torch.Tensor, tf.Tensor or jax.ndarray."
            )

        validate_preprocess_arguments(
            rescale_factor=rescale_factor,
            do_normalize=do_normalize,
            image_mean=image_mean,
            image_std=image_std,
            do_resize=do_resize,
            size=size,
            resample=resample,
        )

        if do_normalize:
            in_norm = False
            out_norm = True
        else:
            in_norm = False
            out_norm = False

        if images is not None:
            pixel_values, vision_grid_thws = [], []
            for image in images:
                patches, image_grid_thw = self.preprocess_npu(
                    image,
                    do_resize=do_resize,
                    resample=resample,
                    do_rescale=do_rescale,
                    rescale_factor=rescale_factor,
                    do_normalize=in_norm,
                    image_mean=image_mean,
                    image_std=image_std,
                    data_format=data_format,
                    do_convert_rgb=do_convert_rgb,
                    input_data_format=input_data_format,
                )
                pixel_values.append(patches)
                vision_grid_thws.append(image_grid_thw)
            pixel_values = torch.cat(pixel_values, dim=0)
            if out_norm:
                image_mean = torch.tensor(
                    image_mean, dtype=pixel_values.dtype, device=pixel_values.device
                )
                image_std = torch.tensor(
                    image_std, dtype=pixel_values.dtype, device=pixel_values.device
                )
                pixel_values = (
                    pixel_values.float()
                    .reshape(
                        -1,
                        image_mean.shape[0],
                        self.temporal_patch_size * self.patch_size * self.patch_size,
                    )
                    .transpose(1, 2)
                )
                pixel_values = (pixel_values - image_mean) / image_std
                pixel_values = pixel_values.transpose(1, 2).reshape(
                    pixel_values.shape[0], -1
                )
            vision_grid_thws = torch.tensor(vision_grid_thws)
            data = {"pixel_values": pixel_values, "image_grid_thw": vision_grid_thws}

        if videos is not None:
            pixel_values, vision_grid_thws = [], []
            for images in videos:
                patches, video_grid_thw = self.preprocess_npu(
                    images,
                    do_resize=do_resize,
                    resample=resample,
                    do_rescale=do_rescale,
                    rescale_factor=rescale_factor,
                    do_normalize=in_norm,
                    image_mean=image_mean,
                    image_std=image_std,
                    data_format=data_format,
                    do_convert_rgb=do_convert_rgb,
                    input_data_format=input_data_format,
                )
                pixel_values.append(patches)
                vision_grid_thws.append(video_grid_thw)
            pixel_values = torch.cat(pixel_values, dim=0)
            if out_norm:
                image_mean = torch.tensor(
                    image_mean, dtype=pixel_values.dtype, device=pixel_values.device
                )
                image_std = torch.tensor(
                    image_std, dtype=pixel_values.dtype, device=pixel_values.device
                )
                pixel_values = (
                    pixel_values.float()
                    .reshape(
                        -1,
                        image_mean.shape[0],
                        self.temporal_patch_size * self.patch_size * self.patch_size,
                    )
                    .transpose(1, 2)
                )
                pixel_values = (pixel_values - image_mean) / image_std
                pixel_values = pixel_values.transpose(1, 2).reshape(
                    pixel_values.shape[0], -1
                )
            vision_grid_thws = torch.tensor(vision_grid_thws)
            data = {
                "pixel_values_videos": pixel_values,
                "video_grid_thw": vision_grid_thws,
            }

        return BatchFeature(data=data, tensor_type=return_tensors)


def fetch_image_npu(
    ele: dict[str, str | Image.Image], size_factor: int = 28
) -> Image.Image:
    if "image" in ele:
        image = ele["image"]
    else:
        image = ele["image_url"]
    image_obj = read_image_npu(image)
    if "resized_height" in ele and "resized_width" in ele:
        resized_height, resized_width = smart_resize(
            ele["resized_height"],
            ele["resized_width"],
            factor=size_factor,
        )
    else:
        height, width = image_obj.shape[-2:]
        min_pixels = ele.get("min_pixels", 4 * 28 * 28)
        max_pixels = ele.get("max_pixels", 16384 * 28 * 28)
        resized_height, resized_width = smart_resize(
            height,
            width,
            factor=size_factor,
            min_pixels=min_pixels,
            max_pixels=max_pixels,
        )
    image = transforms.functional.resize(
        image_obj,
        [resized_height, resized_width],
        interpolation=InterpolationMode.BICUBIC,
        antialias=True,
    ).float()
    return image
