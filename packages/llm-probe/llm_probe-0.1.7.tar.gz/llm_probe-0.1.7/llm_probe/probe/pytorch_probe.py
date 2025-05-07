"""Model probe for extracting intermediate outputs and weights from PyTorch models.

This module provides a probe class for extracting intermediate outputs and weights
from PyTorch models. It allows for setting hooks on specific layers of PyTorch models
to extract intermediate input/output tensors, weights, and biases.
"""

import logging
from typing import Any, Callable, Optional, Tuple, Union

import torch
from torch import nn

from llm_probe.utils import get_all_module_list

# Logger for llm probe framework
logger = logging.getLogger(__name__)


class PTModelProbe:
    """A probe class for extracting intermediate outputs and weights from PyTorch models.

    This class provides functionality to register hooks on specific layers of PyTorch models
    to extract intermediate input/output tensors, weights, and biases.
    """

    def __init__(self, model: nn.Module) -> None:
        """Initialize the PyTorch model probe.

        Args:
            model: The PyTorch model to be probed.
        """
        # Store the model
        self.model = model

        # Initialize the hook list
        self.hook_list: dict[nn.Module, torch.utils.hooks.RemovableHandle] = {}
        # Intermediate intermediate input/output
        self.intermediate_input: dict[nn.Module, torch.Tensor] = {}
        self.intermediate_output: dict[nn.Module, torch.Tensor] = {}

    def set_hook(self, module: Union[str, nn.Module]) -> None:
        """Set a hook for extracting intermediate data from a specific module.

        Args:
            module: The module or module name to set the hook on.
        """
        # For input tensor, we need to register hook function
        logger.debug(f"Setting hook for module {module}")
        self.register_hook(module, self._hook_fn)

    def set_hooks(self, module_list: list[Union[str, nn.Module]]) -> None:
        """Set hooks on multiple modules for extracting intermediate data.

        Args:
            module_list: The list of modules or module names to set hooks on.
        """
        for module in module_list:
            self.set_hook(module)

    def get_intermediate_input(
        self,
        module: Union[str, nn.Module],
        dtype: Optional[torch.dtype] = None,
    ) -> torch.Tensor:
        """Get the intermediate input tensor of a module.

        Args:
            module: The module or module name to get the intermediate input from.
            dtype: The tensor data type to convert to.

        Returns:
            The intermediate input tensor.

        Raises:
            RuntimeError: If the intermediate input does not exist.
        """
        # Check the module type
        module = self._verify_module(module)
        # Check if the intermediate input exists
        if self.intermediate_input.get(module, None) is None:
            logger.error(f"Intermediate input for module {module} does not exist. You may need to set the hook.")
            error_message = "Intermediate input does not exist."
            raise RuntimeError(error_message)
        # Get the intermediate input
        data = self.intermediate_input.get(module, None)
        # Check if data is None
        if data is None:
            error_message = "Intermediate input does not exist."
            raise RuntimeError(error_message)
        # Check the dtype
        if dtype is None:
            return data
        return data.to(dtype)

    def get_intermediate_output(
        self,
        module: Union[str, nn.Module],
        dtype: Optional[torch.dtype] = None,
    ) -> torch.Tensor:
        """Get the intermediate output tensor of a module.

        Args:
            module: The module or module name to get the intermediate output from.
            dtype: The tensor data type to convert to.

        Returns:
            The intermediate output tensor.

        Raises:
            RuntimeError: If the intermediate output does not exist.
        """
        # Check the module type
        module = self._verify_module(module)
        # Check if the intermediate output exists
        if self.intermediate_output.get(module, None) is None:
            logger.error(f"Intermediate output for module {module} does not exist. You may need to set the hook.")
            error_message = "Intermediate output does not exist."
            raise RuntimeError(error_message)
        # Get the intermediate output
        data = self.intermediate_output.get(module, None)
        # Check if data is None
        if data is None:
            error_message = "Intermediate input does not exist."
            raise RuntimeError(error_message)
        # Check the dtype
        if dtype is None:
            return data
        return data.to(dtype)

    def get_intermediate_weight(
        self,
        module: Union[str, nn.Module],
        dtype: Optional[torch.dtype] = None,
    ) -> torch.Tensor:
        """Get the weight tensor of a module.

        Args:
            module: The module or module name to get the weight from.
            dtype: The tensor data type to convert to.

        Returns:
            The weight tensor.

        Raises:
            RuntimeError: If the module does not have a weight attribute or the weight is None.
        """
        # Check the module type
        module = self._verify_module(module)
        # Check if the module has weight
        if not hasattr(module, "weight"):
            logger.error(f"Module {module} does not have a weight attribute.")
            raise RuntimeError(f"Module {module} does not have a weight attribute.")
        # Get the weight
        weight: torch.Tensor = module.weight
        # Check if the module is a linear layer
        if isinstance(module, nn.Linear):
            weight = weight.t()
        # Check if the weight is None
        if weight is None:
            error_message = "Weight does not exist."
            raise RuntimeError(error_message)
        # Check the dtype
        if dtype is None:
            return weight
        # Return the weight
        return weight.to(dtype)

    def get_intermediate_bias(
        self,
        module: Union[str, nn.Module],
        dtype: Optional[torch.dtype] = None,
    ) -> torch.Tensor:
        """Get the bias tensor of a module.

        Args:
            module: The module or module name to get the bias from.
            dtype: The tensor data type to convert to.

        Returns:
            The bias tensor.

        Raises:
            RuntimeError: If the module does not have a bias attribute or the bias is None.
        """
        # Check the module type
        module = self._verify_module(module)
        # Check if the module has bias
        if not hasattr(module, "bias"):
            logger.error(f"Module {module} does not have a bias attribute.")
            raise RuntimeError(f"Module {module} not found in the model.")
        # Get the bias
        bias: torch.Tensor = module.bias
        # Check if the bias is None
        if bias is None:
            error_message = "Bias does not exist."
            raise RuntimeError(error_message)
        # Check the dtype
        if dtype is None:
            return bias
        # Return the bias
        return bias.to(dtype)

    def clear_intermediate_data(self) -> None:
        """Clear the intermediate input and output data."""
        self.intermediate_input.clear()
        self.intermediate_output.clear()

    def _hook_fn(self, module: nn.Module, inputs: Tuple[torch.Tensor], outputs: torch.Tensor) -> None:
        # Log the shape of the input and output
        logger.debug(f"Module: {module}")
        logger.debug(f"Input shape: {inputs[0].shape}")
        logger.debug(f"Output shape: {outputs.shape}")
        # Store the input and output
        if self.intermediate_input.get(module, None) is None:
            self.intermediate_input[module] = inputs[0]
        else:
            self.intermediate_input[module] = torch.cat([self.intermediate_input[module], inputs[0]], dim=1)
        if self.intermediate_output.get(module, None) is None:
            self.intermediate_output[module] = outputs
        else:
            self.intermediate_output[module] = torch.cat([self.intermediate_output[module], outputs], dim=1)

    def register_hook(
        self,
        target: Union[str, nn.Module],
        hook_fn: Callable[[nn.Module, Tuple[torch.Tensor], Any], None],
    ) -> None:
        """Register a custom hook function on a module.

        Args:
            target: The module or module name to register the hook on.
            hook_fn: The hook function to register.
        """
        # Check the target type
        module = self._verify_module(target)
        # Check if the hook already exists
        if self.hook_list.get(module, None) is not None:
            logger.warning(f"Hook for module {module} already exists.")
            return
        # Register the hook
        hook = module.register_forward_hook(hook_fn)
        # Append the hook to the hook list
        self.hook_list[module] = hook

    def remove_hooks(self) -> None:
        """Remove all registered hooks."""
        # Remove all hooks
        for hook in self.hook_list.values():
            hook.remove()
        # Clear the hook list
        self.hook_list.clear()

    def forward(self, *args: Any, **kwargs: Any) -> torch.Tensor:
        """Perform a forward pass through the model.

        Args:
            *args: Positional arguments to pass to the model.
            **kwargs: Keyword arguments to pass to the model.

        Returns:
            The model output tensor.

        Raises:
            TypeError: If the model output is not a torch.Tensor.
        """
        output = self.model(*args, **kwargs)
        if not isinstance(output, torch.Tensor):
            error_message = "Expected the model output to be a torch.Tensor"
            raise TypeError(error_message)
        return output

    def get_all_module_list(self) -> list[nn.Module]:
        """Get a list of all modules in the model.

        Returns:
            A list of all modules in the model.
        """
        return get_all_module_list(self.model)

    def get_all_module_name(self) -> list[str]:
        """Get a list of all module names in the model.

        Returns:
            A list of all module names in the model.
        """
        return [name for name, _ in self.model.named_modules() if name]

    # Check the module type
    def _verify_module(self, module: Union[str, nn.Module]) -> nn.Module:
        # Check the module type
        # If the module is a string, find the module
        if isinstance(module, str):
            mod: nn.Module = dict(self.model.named_modules()).get(module, None)
            return mod
        if not isinstance(module, nn.Module):
            logger.error("Module must be a string or an nn.Module instance.")
            error_message = "Module must be a string or an nn.Module instance."
            raise TypeError(error_message)
        # Return the module
        return module
