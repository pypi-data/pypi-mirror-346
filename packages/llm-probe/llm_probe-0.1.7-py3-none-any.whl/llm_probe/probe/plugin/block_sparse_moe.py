"""Plugin for block sparse MoE module."""

import logging
import re
from typing import List, Optional, Tuple, Union

import torch
from torch import nn
from transformers import AutoModelForCausalLM

from llm_probe.models import get_hf_config, get_hf_name_pattern
from llm_probe.utils import check_model_architecture

# Get the logger
logger = logging.getLogger(__name__)


class BlockSparseMoE:
    """Block sparse MoE module."""

    def __init__(self, model: AutoModelForCausalLM) -> None:
        """Initialize the block sparse MoE module.

        Args:
            model: The model to probe.
        """
        self.model = model

        # Initialize the patterns
        self.gate_name_pattern: str = ""
        self.w1_name_pattern: str = ""
        self.w2_name_pattern: str = ""
        self.w3_name_pattern: str = ""

        # Verify the layer pattern
        if self.is_moe_model():
            self._verify_layer_pattern()

    def is_moe_model(self) -> bool:
        """Check if the model is a MoE model.

        Returns:
            True if the model is a MoE model, False otherwise.
        """
        # Check if the model architecture is supported
        return check_model_architecture(self.model.config, "MixtralForCausalLM")

    def is_moe_block(self, module: Union[str, nn.Module]) -> bool:
        """Check if the module is a MoE block.

        Args:
            module: The module to check.

        Returns:
            True if the module is a MoE block, False otherwise.
        """
        # If the model is not a MoE model, raise an error
        self._verify_moe_model()

        # To check if the module is a MoE layer, the module must be a string type.
        if not isinstance(module, str):
            err_msg = """
                To check if the module is a MoE block, the module must be a string type.
                Please give the name of the module.
            """
            raise TypeError(err_msg)

        # Check if the module is a MoE layer
        if self.is_moe_layer(module):
            return True
        return self._is_gate_layer(module)

    def is_moe_layer(self, module: Union[str, nn.Module]) -> bool:
        """Check if the module is a MoE layer.

        Args:
            module: The module to check.

        Returns:
            True if the module is a MoE layer, False otherwise.
        """
        # If the model is not a MoE model, raise an error
        self._verify_moe_model()

        # To check if the module is a MoE layer, the module must be a string type.
        if not isinstance(module, str):
            err_msg = """
                To check if the module is a MoE layer, the module must be a string type.
                Please give the name of the module.
            """
            raise TypeError(err_msg)

        # Check if the module is a MoE layer
        if self._is_w1_layer(module):
            return True
        if self._is_w2_layer(module):
            return True
        return self._is_w3_layer(module)

    def extract_layer_idx(self, module: Union[str, nn.Module]) -> int:
        """Extract the layer index from the module.

        Args:
            module: The module to get the layer index from.

        Returns:
            The layer index.
        """
        # If the model is not a MoE model, raise an error
        self._verify_moe_model()

        # To check if the module is a MoE layer, the module must be a string type.
        if not isinstance(module, str):
            err_msg = """
                To check if the module is a MoE layer, the module must be a string type.
                Please give the name of the module.
            """
            raise TypeError(err_msg)

        # Initialize the layer index
        layer_idx: Optional[int] = None

        if self._is_gate_layer(module):
            layer_idx = _extract_layer_idx(module, self.gate_name_pattern)
        elif self._is_w1_layer(module):
            layer_idx = _extract_layer_idx(module, self.w1_name_pattern)
        elif self._is_w2_layer(module):
            layer_idx = _extract_layer_idx(module, self.w2_name_pattern)
        elif self._is_w3_layer(module):
            layer_idx = _extract_layer_idx(module, self.w3_name_pattern)

        # If the layer index is not found, raise an error
        if layer_idx is None:
            err_msg = "The layer index is not found in the module."
            raise ValueError(err_msg)
        return layer_idx

    def extract_expert_idx(self, module: Union[str, nn.Module]) -> int:
        """Extract the expert index from the module.

        Args:
            module: The module to get the expert index from.

        Returns:
            The expert index.
        """
        # If the model is not a MoE model, raise an error
        self._verify_moe_model()

        # To check if the module is a MoE layer, the module must be a string type.
        if not isinstance(module, str):
            err_msg = """
                To check if the module is a MoE layer, the module must be a string type.
                Please give the name of the module.
            """
            raise TypeError(err_msg)

        # Initialize the expert index
        expert_idx: Optional[int] = None

        if self._is_w1_layer(module):
            expert_idx = _extract_expert_idx(module, self.w1_name_pattern)
        elif self._is_w2_layer(module):
            expert_idx = _extract_expert_idx(module, self.w2_name_pattern)
        elif self._is_w3_layer(module):
            expert_idx = _extract_expert_idx(module, self.w3_name_pattern)

        # If the expert index is not found, raise an error
        if expert_idx is None:
            err_msg = "The expert index is not found in the module."
            raise ValueError(err_msg)
        return expert_idx

    def get_all_expert_modules(self, module: Union[str, nn.Module], layer_idx: int) -> Tuple[str, List[str]]:
        """Get all the expert modules.

        Args:
            module: The module to get the expert modules from.
            layer_idx: The layer index to get the expert modules from.

        Returns:
            The list of expert modules.
        """
        # If the model is not a MoE model, raise an error
        self._verify_moe_model()

        # To check if the module is a MoE layer, the module must be a string type.
        if not isinstance(module, str):
            err_msg = """
                To get the expert modules, the module must be a string type.
                Please give the name of the module.
            """
            raise TypeError(err_msg)

        # Get the expert modules
        pattern: str = ""
        if self._is_w1_layer(module):
            pattern = self.w1_name_pattern
        elif self._is_w2_layer(module):
            pattern = self.w2_name_pattern
        elif self._is_w3_layer(module):
            pattern = self.w3_name_pattern

        # Get the expert modules in moe layer
        expert_modules: List[str] = []
        for i in range(get_hf_config(self.model, "num_local_experts")):
            moe_layer = _switch_layer_idx(pattern, layer_idx)
            moe_layer = _switch_expert_idx(moe_layer, i)
            expert_modules.append(moe_layer)

        # Get the routing gate module
        gate_module = _switch_layer_idx(self.gate_name_pattern, layer_idx)

        return gate_module, expert_modules

    def get_expert_ids(self, gate_output: torch.Tensor) -> torch.Tensor:
        """Get the expert IDs from the gate output.

        Args:
            gate_output: The gate output.

        Returns:
            The expert IDs.
        """
        # If the model is not a MoE model, raise an error
        self._verify_moe_model()

        num_experts_per_tok: int = get_hf_config(self.model, "num_experts_per_tok")
        num_local_experts: int = get_hf_config(self.model, "num_local_experts")

        # Check the dimension of the gate output
        if gate_output.ndim != 2:
            err_msg = "The gate output must be a 2D tensor."
            raise ValueError(err_msg)
        if gate_output.shape[1] != num_local_experts:
            err_msg = "The number of experts per token must match the number of experts per token in the model config."
            raise ValueError(err_msg)

        # Get the expert IDs
        _, expert_ids = torch.topk(gate_output, num_experts_per_tok, dim=1)
        return expert_ids

    def get_expert_tensor(self, gate_output: torch.Tensor, moe_tensor: List[torch.Tensor]) -> torch.Tensor:
        """Get the MoE input/output tensor.

        Args:
            gate_output: The gate output.
            moe_tensor: The MoE input/output tensor.

        Returns:
            The MoE input/output tensor.
        """
        # If the model is not a MoE model, raise an error
        self._verify_moe_model()

        # Get the expert IDs
        expert_ids = self.get_expert_ids(gate_output)

        # Get the each dimension of the expert output
        seq_len: int = gate_output.shape[0]
        num_experts_per_tok: int = get_hf_config(self.model, "num_experts_per_tok")
        num_local_experts: int = get_hf_config(self.model, "num_local_experts")
        hidden_size: int = moe_tensor[0].shape[1]

        # Initialize the expert output
        expert_tensor = torch.zeros(seq_len, num_experts_per_tok, hidden_size)
        # Initialize the counter for each expert
        expert_counter: List[int] = [0] * num_local_experts

        # Get the expert output for each token
        for seq in range(seq_len):
            for expert_idx in range(num_experts_per_tok):
                expert_id = expert_ids[seq, expert_idx]
                expert_tensor[seq, expert_idx, :] = moe_tensor[expert_id][expert_counter[expert_id], :]
                # Update the counter for the expert
                expert_counter[expert_id] += 1

        # Check if the expert counter is equal to the shape of the MoE output
        if not all(counter == moe_tensor[i].shape[0] for i, counter in enumerate(expert_counter)):
            err_msg = "The expert counter is not equal to the shape of the MoE output."
            raise ValueError(err_msg)

        return expert_tensor

    def _verify_moe_model(self) -> None:
        # Check if the model architecture is supported
        if not self.is_moe_model():
            err_msg = "The model is not a MoE model. Please check the model architecture."
            raise ValueError(err_msg)

    def _verify_layer_pattern(self) -> None:
        # Check if the layer pattern is correct for routing gate
        self.gate_name_pattern = get_hf_name_pattern(self.model, "gate_name_pattern")
        if "<l>" not in self.gate_name_pattern:
            err_msg = "The gate name pattern must contain <l>."
            raise ValueError(err_msg)

        # Check if the layer pattern is correct for the weight matrices
        self.w1_name_pattern = get_hf_name_pattern(self.model, "w1_name_pattern")
        if "<l>" not in self.w1_name_pattern and "<e>" not in self.w1_name_pattern:
            err_msg = "The weight matrix name pattern must contain <l> or <e>."
            raise ValueError(err_msg)
        self.w2_name_pattern = get_hf_name_pattern(self.model, "w2_name_pattern")
        if "<l>" not in self.w2_name_pattern and "<e>" not in self.w2_name_pattern:
            err_msg = "The weight matrix name pattern must contain <l> or <e>."
            raise ValueError(err_msg)
        self.w3_name_pattern = get_hf_name_pattern(self.model, "w3_name_pattern")
        if "<l>" not in self.w3_name_pattern and "<e>" not in self.w3_name_pattern:
            err_msg = "The weight matrix name pattern must contain <l> or <e>."
            raise ValueError(err_msg)

    def _is_gate_layer(self, module: str) -> bool:
        return _compare_layer_pattern(
            target=module,
            pattern=self.gate_name_pattern,
            has_layer_idx=True,
            has_expert_idx=False,
        )

    def _is_w1_layer(self, module: str) -> bool:
        return _compare_layer_pattern(
            target=module,
            pattern=self.w1_name_pattern,
            has_layer_idx=True,
            has_expert_idx=True,
        )

    def _is_w2_layer(self, module: str) -> bool:
        return _compare_layer_pattern(
            target=module,
            pattern=self.w2_name_pattern,
            has_layer_idx=True,
            has_expert_idx=True,
        )

    def _is_w3_layer(self, module: str) -> bool:
        return _compare_layer_pattern(
            target=module,
            pattern=self.w3_name_pattern,
            has_layer_idx=True,
            has_expert_idx=True,
        )


def _compare_layer_pattern(
    target: str,
    pattern: str,
    has_layer_idx: bool = True,
    has_expert_idx: bool = True,
) -> bool:
    """Compare the layer pattern.

    Args:
        target: The target to compare.
        pattern: The pattern to compare.
        has_layer_idx: Whether the layer index is in the pattern.
        has_expert_idx: Whether the expert index is in the pattern.

    Returns:
        True if the target matches the pattern, False otherwise.
    """
    pattern = pattern.replace("<l>", r"\d+" if has_layer_idx else r"")
    pattern = pattern.replace("<e>", r"\d+" if has_expert_idx else r"")
    return bool(re.match(pattern, target))


def _extract_layer_idx(target: str, pattern: str) -> Optional[int]:
    """Extract the layer index from the target.

    Args:
        target: The target to extract the layer index from.
        pattern: The pattern to extract the layer index from.

    Returns:
        The layer index.
    """
    # Get the layer index
    parts_pattern = pattern.split(".")
    parts_name = target.split(".")

    # Check if the length of the parts pattern and the parts name are the same
    if len(parts_pattern) != len(parts_name):
        return None

    # Extract the layer index
    for i, part in enumerate(parts_pattern):
        if part == "<l>":
            return int(parts_name[i])
    # If the layer index is not found, return None
    return None


def _extract_expert_idx(target: str, pattern: str) -> Optional[int]:
    """Extract the expert index from the target.

    Args:
        target: The target to extract the expert index from.
        pattern: The pattern to extract the expert index from.

    Returns:
        The expert index.
    """
    # Get the expert index
    parts_pattern = pattern.split(".")
    parts_name = target.split(".")

    # Check if the length of the parts pattern and the parts name are the same
    if len(parts_pattern) != len(parts_name):
        return None

    # Extract the expert index
    for i, part in enumerate(parts_pattern):
        if part == "<e>":
            return int(parts_name[i])
    # If the expert index is not found, return None
    return None


def _switch_layer_idx(target: str, layer_idx: int) -> str:
    """Switch the layer index.

    Args:
        target: The target to switch the layer index.
        layer_idx: The layer index to switch to.
    """
    return target.replace("<l>", str(layer_idx))


def _switch_expert_idx(target: str, expert_idx: int) -> str:
    """Switch the expert index.

    Args:
        target: The target to switch the expert index.
        expert_idx: The expert index to switch to.

    Returns:
        The switched module.
    """
    return target.replace("<e>", str(expert_idx))
