# Copyright (c) Huawei Technologies Co., Ltd. 2024-2025. All rights reserved.
# MindIE is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

from dataclasses import dataclass
from typing import List
import argparse
import warnings


@dataclass
class BaseConfig:
    """Base configuration for MindIE-Turbo.

    Contains basic settings that are required for all running modes.
    """

    # Add more basic settings here

    def validate(self) -> None:
        # Add validation logic here
        pass


def parse_custom_args(args: argparse.Namespace, unknown: List[str]) -> argparse.Namespace:
    """Parse unknown command line arguments into namespace.

    Args:
        args: Existing argument namespace to update.
        unknown: List of unknown arguments in format ['--key', 'value', ...].

    Returns:
        Updated argument namespace.

    Warns:
        UserWarning: When unknown arguments are detected.
    """
    if unknown:
        warnings.warn(f"\n\n\nDetected unknown arguments: {unknown}\n\n\n", UserWarning)

    for i in range(0, len(unknown), 2):
        key = unknown[i] if i < len(unknown) else None
        values = [unknown[i + 1]] if i + 1 < len(unknown) else []
        if key and key.startswith("--"):
            key = key[2:].replace("-", "_")
            # Handle consecutive flags
            while i + 2 < len(unknown) and not unknown[i + 2].startswith("--"):
                values.append(unknown[i + 2])
                i += 1
            value = values[0] if len(values) == 1 else values if values else True
            setattr(args, key, value)
        elif key:
            warnings.warn(f"Skipping malformed argument: {key}", UserWarning)

    return args


def create_parser() -> argparse.ArgumentParser:
    """Creates argument parser with basic settings.

    Returns:
        Configured argument parser.

    Example:
    args, unknown_args = parser.parse_known_args()
    parse_custom_args(args, unknown_args)

    An example of adding a new argument:
    group = parser.add_argument_group(title="basic_settings")
    group.add_argument(
        '--backend-type',
        type=int,
        default=BaseConfig.backend_type,
        choices=[0, 1],
        help='Backend type: 0 for MindIE mode, 1 for Turbo mode'
    )
    """
    arg_parser = argparse.ArgumentParser(conflict_handler="resolve")
    return arg_parser

parser = create_parser()
