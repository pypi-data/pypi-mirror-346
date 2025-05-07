# Copyright (c) Huawei Technologies Co., Ltd. 2024-2025. All rights reserved.
# MindIE is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import importlib
import sys
import types
from typing import Callable, Literal


def initialize_placeholder(func_name):
    """Create a placeholder function that raises an error when called"""

    def placeholder_function(*args, **kwargs):
        raise RuntimeError(
            f"Function {func_name} requires implementation."
            f"This is not supposed to happen, did you forget to implement the function?"
        )

    return placeholder_function


class Patch:
    """
    A class that handles function/method patching operations.
    Supports both replacement and decoration of existing functions.
    """

    def __init__(
        self,
        target: str,  # Target path in format "module.submodule.function"
        substitute: Callable = None,
        method: Literal["replace", "decorate"] = "replace",
        create: bool = False,  # Whether to create dummy modules if not exist
    ):
        self.target_module, self.target_function = target.rsplit(".", 1) if "." in target else (target, None)

        self.original_module = None
        self.original_function = None
        self.candidate: Callable = None
        self.patch_function = None
        self.wrappers = []
        self.applied = False
        self.create = create

        substitute = substitute or initialize_placeholder(target)

        match method:
            case "replace":
                self.set_replacement(substitute)
            case "decorate":
                self.add_decorator(substitute)

    @property
    def original_function_id(self):
        return id(self.original_function)

    def set_replacement(self, replacement: Callable, force: bool = False):
        """Direct replacement of the target function"""
        if self.candidate and not force:
            raise RuntimeError(
                f"Patch function {self.target_function} is already set, "
                "please use force=True to override the patch function."
            )

        self.candidate = replacement
        self.applied = False

    def add_decorator(self, decorator: Callable):
        """Add a decorator to wrap the target function"""
        self.wrappers.append(decorator)
        self.applied = False

    def apply_patch(self):
        """Apply the patch to the target function and propagate changes to all references"""
        if self.applied:
            return

        self.original_module, self.original_function = Patch.parse_path(
            self.target_module, self.target_function, self.create
        )

        if self.candidate is None:
            self.candidate = self.original_function
        for wrapper in self.wrappers:
            self.candidate = wrapper(self.candidate)
        if self.target_function is not None:
            setattr(self.original_module, self.target_function, self.candidate)

        for key, value in sys.modules.copy().items():
            if (
                self.target_function is not None
                and hasattr(value, self.target_function)
                and id(getattr(value, self.target_function)) == self.original_function_id
            ):
                setattr(value, self.target_function, self.candidate)
        self.applied = True

    @staticmethod
    def parse_path(module_path, function_name, create_dummy):
        """
        Parse module path and resolve/create modules as needed.

        Args:
            module_path: Dot-separated module path
            function_name: Target function name (None for module only)
            create_dummy: Create dummy modules/functions when missing

        Returns:
            Tuple of (resolved module, target function/none)

        Raises:
            ModuleNotFoundError: If module path is invalid and create_dummy=False
            AttributeError: If function is missing and create_dummy=False
        """
        from importlib.machinery import ModuleSpec

        def create_dummy_module(full_path, parent=None):
            """Create and register a placeholder module"""
            dummy = types.ModuleType(full_path)
            dummy.__file__ = "mindie_turbo.dummy_module.py"
            dummy.__spec__ = ModuleSpec(full_path, None)
            sys.modules[full_path] = dummy
            if parent:
                setattr(parent, full_path.split(".")[-1], dummy)
            return dummy

        def create_placeholder_function(func_name):
            """Create dummy function that raises when called"""

            def placeholder(*args, **kwargs):
                raise NotImplementedError(f"Function {func_name} is a placeholder")

            placeholder.__name__ = func_name
            return placeholder

        modules = module_path.split(".")
        current_module = None
        processed_path = []

        for idx, part in enumerate(modules):
            current_path = ".".join(modules[: idx + 1])
            parent_path = ".".join(modules[:idx]) if idx > 0 else None

            try:
                current_module = importlib.import_module(current_path)
            except ModuleNotFoundError:
                # Handle missing module
                if parent_path:
                    parent = importlib.import_module(parent_path)
                    if hasattr(parent, part):
                        # Use existing attribute from parent
                        current_module = getattr(parent, part)
                        # Check for early function resolution
                        if function_name:
                            if hasattr(current_module, function_name):
                                return current_module, getattr(current_module, function_name)
                            if create_dummy:
                                ph_func = create_placeholder_function(function_name)
                                setattr(current_module, function_name, ph_func)
                                return current_module, ph_func
                            raise AttributeError(f"Function {function_name} missing in {current_path}")
                else:
                    if not create_dummy:
                        raise
                    # Create and register dummy module
                    current_module = create_dummy_module(
                        current_path, parent=importlib.import_module(parent_path) if parent_path else None
                    )

            processed_path.append(part)

        # Final function handling
        final_module = sys.modules[module_path]
        if function_name is not None:
            if not hasattr(final_module, function_name):
                if create_dummy:
                    ph_func = create_placeholder_function(function_name)
                    setattr(final_module, function_name, ph_func)
                else:
                    setattr(final_module, function_name, None)
            return final_module, getattr(final_module, function_name)

        return final_module, None


class Patcher:
    """
    Static utility class for managing multiple patches.
    Provides a simplified interface for patch registration and application.
    """

    patches: dict[str, Patch] = {}

    @staticmethod
    def register_patch(
        target: str,
        substitute: Callable = None,
        method: Literal["replace", "decorate"] = "replace",
        create: bool = False,
        force: bool = False,
    ):
        """Register a new patch or update existing one"""
        if target not in Patcher.patches:
            Patcher.patches[target] = Patch(target, substitute, method, create)
        elif method == "replace":
            Patcher.patches.get(target).set_replacement(substitute, force)
        elif method == "decorate":
            Patcher.patches.get(target).add_decorator(substitute)
        else:
            raise ValueError(f"Invalid patch method {method}")

    @staticmethod
    def apply_patches():
        """Apply all registered patches"""
        for patch in Patcher.patches.values():
            patch.apply_patch()
