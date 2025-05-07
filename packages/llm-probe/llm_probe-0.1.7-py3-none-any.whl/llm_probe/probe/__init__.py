"""Model probe for extracting intermediate outputs and weights from models.

This module provides a probe class for extracting intermediate outputs and weights
from PyTorch and HuggingFace models. It allows for setting hooks on specific
modules to extract intermediate data, and provides methods for accessing model
configuration, tokenization, text generation, and rotary embeddings (RoPE).
"""

from .huggingface_probe import HFModelProbe

# Export the module list
__all__ = ["HFModelProbe"]
