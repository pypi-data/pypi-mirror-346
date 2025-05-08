# Copyright (c) Huawei Technologies Co., Ltd. 2024-2025. All rights reserved.
# MindIE is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import argparse
from abc import ABC, abstractmethod
from typing import Optional

from mindie_turbo.utils.cli import parser, parse_custom_args
from mindie_turbo.utils.patcher import Patcher


class BaseTurbo(ABC):
    """Base class for Turbo optimizations.

    This abstract base class defines the interface and common functionalityfor all Turbo optimization implementations.
    """

    def __init__(self):
        self._args: Optional[argparse.Namespace] = None
        self.patcher = Patcher
        self.optimization_levels: dict[int, str] = {
            0: "basic",
            1: "advanced",
            2: "high-advanced",
            3: "experimental",
        }
        self.extra_patch_mapping = {}

    @property
    def args(self) -> argparse.Namespace:
        """Get parsed arguments with lazy initialization."""
        pass

    @abstractmethod
    def check_environment(self) -> None:
        """Check if the required environment is ready."""
        pass

    @abstractmethod
    def setup_environment(self) -> None:
        """Setup necessary environment variables and configurations."""
        pass

    @abstractmethod
    def register_patches(self, level: int) -> None:
        """Register optimization patches for the specified level.

        Args:
            level: Optimization level indicating which patches to register.
        """
        pass

    @abstractmethod
    def register_env_patches(self) -> None:
        """Register optimization patches according to environmental variables.
        """
        pass

    def activate(self, level: int = 0) -> None:
        """Activate optimizations at the specified level.

        Args:
            level: Optimization level to apply. Defaults to 0.
        """
        if level not in self.optimization_levels:
            raise ValueError(
                f"Unsupported optimization level: {level}, available levels are {self.optimization_levels.values()}"
            )

        self.check_environment()
        self.setup_environment()
        self.register_patches(level)
        self.register_env_patches()
        self.patcher.apply_patches()


# Note: This class maybe should consider another name, we need a singleton to store all the
# context related information. Maybe TurboContext in the future
class TurboPatch:
    """
    A singleton class indicates which frontend is used.
    """

    _frontend = None
    is_faquant: bool = False

    @classmethod
    def set_frontend(cls, frontend: BaseTurbo) -> None:
        """Set the frontend that should be add patches.

        Args:
            frontend: An object that is instantiated by a
            class inherited from BaseTurbo.
        """
        if not cls._frontend:
            cls._frontend = frontend

    @classmethod
    def activate_extra_patches(cls, patch_type: str) -> None:
        """Activate patches according to given patch types.

        Args:
            patch_type: Which type of patches to be activated.
        """
        cls._frontend.activate_extra_patches(patch_type)
