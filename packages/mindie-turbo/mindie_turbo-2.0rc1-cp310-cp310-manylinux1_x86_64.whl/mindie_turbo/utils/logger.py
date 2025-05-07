# Copyright (c) Huawei Technologies Co., Ltd. 2024-2025. All rights reserved.
# MindIE is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import logging


def setup_logger(name: str, log_file: str, level: int, fmt: str) -> logging.Logger:
    formatter = logging.Formatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")
    logger_instance = logging.getLogger(name)
    logger_instance.setLevel(level)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger_instance.addHandler(stream_handler)

    return logger_instance


logger = setup_logger(
    name="MindIE-Turbo",
    # NOTE(Yizhou): parametrize this path and level
    log_file="Turbo.log",
    level=logging.ERROR,
    fmt="%(levelname)-8s - %(asctime)s - PID:%(process)d - %(threadName)s - %(filename)s:%(lineno)d - %(message)s",
)
