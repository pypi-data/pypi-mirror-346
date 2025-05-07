# Copyright (c) Huawei Technologies Co., Ltd. 2024-2024. All rights reserved.

"""
MindIE Turbo: An LLM inference acceleration framework featuring extensive plugin collections optimized for 
Ascend devices.
"""
__all__ = [
    "vllm_turbo",
    "MindIETurboQuantizer",
]

import os
import stat
from pathlib import Path
from .quantize.quantizer import MindIETurboQuantizer
from .adaptor import vllm_turbo

# Determine whether other regular users have write permissions to the directory
parnet_dir = Path(__file__).parent.absolute()

if (os.stat(parnet_dir).st_mode & stat.S_IWOTH):
    raise PermissionError(f"Other regular users in the current directory [{parnet_dir}] have write permissions")