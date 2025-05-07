# Adapted from
# https://github.com/vllm-project/vllm/blob/main/vllm/env.py
# Copyright 2023 The vLLM team.

# Copyright (c) Huawei Technologies Co., Ltd. 2024-2025. All rights reserved.

import os
from typing import Any, Callable, Dict

env_variables: Dict[str, Callable[[], Any]] = {
    # This varialbe controls MindIE Turbo's optimization level over vLLM.
    "VLLM_OPTIMIZATION_LEVEL": lambda: os.getenv("VLLM_OPTIMIZATION_LEVEL", "2"),
    "MAX_JOBS": lambda: os.getenv("MAX_JOBS", None),
    "CMAKE_BUILD_TYPE": lambda: os.getenv("CMAKE_BUILD_TYPE"),
    # If set, MindIE Turbo will print verbose logs during installation
    "VERBOSE": lambda: bool(int(os.getenv("VERBOSE", "0"))),
    "ASCEND_HOME_PATH": lambda: os.environ.get("ASCEND_HOME_PATH", None),
    "LD_LIBRARY_PATH": lambda: os.environ.get("LD_LIBRARY_PATH", None),
    "ATB_HOME_PATH": lambda: os.environ.get("ATB_HOME_PATH", None),
    # Whether cache the sampling tensors to reduce overhead. 
    # Note that this feature can't be activated in beam search and chunked-prefill situation.
    "USING_SAMPLING_TENSOR_CACHE": lambda: os.environ.get("USING_SAMPLING_TENSOR_CACHE", "0"),
    # Whether to enable LCCL communiation.
    # Note that currently LCCL doesn't support multi-node communication.
    "USING_LCCL_COM": lambda: os.environ.get("USING_LCCL_COM", "1"),
}


def __getattr__(name: str):
    # lazy evaluation of environment variables
    if name in env_variables:
        return env_variables[name]()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return list(env_variables.keys())
