from typing import List

import torch
from transformers import PretrainedConfig


def get_all_module_list(model: torch.nn.Module) -> List[torch.nn.Module]:
    """Get all modules from the model.

    Args:
        model: The model to get all modules from.

    Returns:
        A list of all modules from the model.
    """
    # Get all modules with for loop
    module_list = []
    for _, module in model.named_modules():
        module_list.append(module)
    return module_list


def check_model_architecture(config: PretrainedConfig, architecture: str) -> bool:
    """Check if the model architecture is supported.

    Args:
        config: The configuration of the model.
        architecture: The architecture of the model.

    Returns:
        True if the model architecture is supported, False otherwise.
    """
    return architecture in config.architectures
