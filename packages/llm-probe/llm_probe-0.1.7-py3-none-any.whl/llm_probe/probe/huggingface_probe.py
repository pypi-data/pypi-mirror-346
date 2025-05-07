"""HF Model probe for extracting intermediate outputs and weights from models.

This module provides a probe class for extracting intermediate outputs and weights
from HuggingFace models. It allows for setting hooks on specific modules to extract
intermediate data, and provides methods for accessing model configuration, tokenization,
text generation, and rotary embeddings (RoPE).
"""

import logging
from typing import Any, List, Optional, Tuple, Union

import torch
from torch import nn
from transformers import AutoModel, AutoTokenizer

from llm_probe.models import get_hf_config
from llm_probe.probe.plugin.block_sparse_moe import BlockSparseMoE
from llm_probe.probe.plugin.rotary_embedding import RotaryEmbedding
from llm_probe.probe.pytorch_probe import PTModelProbe

# Logger for llm probe framework
logger = logging.getLogger(__name__)


class HFModelProbe(PTModelProbe):
    """A probe class for extracting intermediate outputs and weights from HuggingFace models.

    This class extends PTModelProbe to support HuggingFace models and tokenizers.
    It provides methods for accessing model configuration, tokenization, text generation,
    and rotary embeddings (RoPE).
    """

    def __init__(self, model: AutoModel, tokenizer: AutoTokenizer) -> None:
        """Initialize the HuggingFace model probe.

        Args:
            model: The HuggingFace model to be probed.
            tokenizer: The HuggingFace tokenizer for the model.
        """
        super().__init__(model)
        self.tokenizer = tokenizer
        self.output_ids: Union[torch.Tensor, None] = None

        # Add plugins for additional probing features
        self.rotary_emb = RotaryEmbedding(self.model.config)
        self.block_sparse_moe = BlockSparseMoE(self.model)

    def set_hook(self, module: Union[str, nn.Module]) -> None:
        """Set a hook for extracting intermediate data from a specific module.

        Args:
            module: The module or module name to set the hook on.
        """
        # If the model is a MoE model, and the module is a MoE layer, we need to set the hook for the MoE layer
        if self.block_sparse_moe.is_moe_model() and self.block_sparse_moe.is_moe_layer(module):
            logger.info("To set the hook for the MoE layer, we need to use the BlockSparseMoE plugin.")
            # Get the all expert modules
            layer_idx = self.block_sparse_moe.extract_layer_idx(module)
            gate_module, expert_modules = self.block_sparse_moe.get_all_expert_modules(module, layer_idx)
            # Set the hook for the all experts
            for expert_module in expert_modules:
                super().set_hook(expert_module)
            # Set the hook for the routing gate
            super().set_hook(gate_module)
        # Otherwise, we can use the default hook function
        else:
            super().set_hook(module)

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
        # If the model is a MoE model, and the module is a MoE layer, we need to get the intermediate input for the MoE layer
        if self.block_sparse_moe.is_moe_model() and self.block_sparse_moe.is_moe_layer(module):
            logger.info("To get the intermediate input for the MoE layer, we need to use the BlockSparseMoE plugin.")
            # Get the all expert modules
            layer_idx = self.block_sparse_moe.extract_layer_idx(module)
            gate_module, expert_modules = self.block_sparse_moe.get_all_expert_modules(module, layer_idx)
            # Get the intermediate output for the routing gate
            gate_output = super().get_intermediate_output(gate_module, dtype)
            # Get the intermediate input for the all experts
            expert_inputs = []
            for expert_module in expert_modules:
                expert_inputs.append(super().get_intermediate_input(expert_module, dtype))
            # Return the MoE input tensor for all experts
            return self.block_sparse_moe.get_expert_tensor(gate_output, expert_inputs)

        # Otherwise, we can use the default hook function
        return super().get_intermediate_input(module, dtype)

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
        # If the model is a MoE model, and the module is a MoE layer, we need to get the intermediate output for the MoE layer
        if self.block_sparse_moe.is_moe_model() and self.block_sparse_moe.is_moe_layer(module):
            logger.info("To get the intermediate output for the MoE layer, we need to use the BlockSparseMoE plugin.")
            # Get the all expert modules
            layer_idx = self.block_sparse_moe.extract_layer_idx(module)
            gate_module, expert_modules = self.block_sparse_moe.get_all_expert_modules(module, layer_idx)
            # Get the intermediate output for the routing gate
            gate_output = super().get_intermediate_output(gate_module, dtype)
            # Get the intermediate output for the all experts
            expert_outputs = []
            for expert_module in expert_modules:
                expert_outputs.append(super().get_intermediate_output(expert_module, dtype))
            # Return the MoE output tensor for all experts
            return self.block_sparse_moe.get_expert_tensor(gate_output, expert_outputs)

        # Otherwise, we can use the default hook function
        return super().get_intermediate_output(module, dtype)

    def get_architecture(self) -> str:
        """Get the architecture name of the model.

        Returns:
            The architecture name of the model.
        """
        return get_hf_config(self.model, "architecture")[0]

    def get_bos_token_id(self) -> int:
        """Get the beginning-of-sequence token ID.

        Returns:
            The BOS token ID.
        """
        return self.tokenizer.bos_token_id

    def get_eos_token_id(self) -> int:
        """Get the end-of-sequence token ID.

        Returns:
            The EOS token ID.
        """
        return self.tokenizer.eos_token_id

    def get_hidden_act(self) -> str:
        """Get the hidden activation function name from model config.

        Returns:
            The hidden activation function name.
        """
        return get_hf_config(self.model, "hidden_act")

    def get_hidden_size(self) -> int:
        """Get the hidden size from model config.

        Returns:
            The hidden size value.
        """
        return get_hf_config(self.model, "hidden_size")

    def get_intermediate_size(self) -> int:
        """Get the intermediate size from model config.

        Returns:
            The intermediate size value.
        """
        return get_hf_config(self.model, "intermediate_size")

    def get_max_length(self) -> int:
        """Get the maximum sequence length from model config.

        Returns:
            The maximum sequence length.
        """
        return get_hf_config(self.model, "max_length")

    def get_num_attention_heads(self) -> int:
        """Get the number of attention heads from model config.

        Returns:
            The number of attention heads.
        """
        return get_hf_config(self.model, "num_attention_heads")

    def get_num_key_value_heads(self) -> int:
        """Get the number of key/value heads from model config.

        Returns:
            The number of key/value heads.
        """
        return get_hf_config(self.model, "num_key_value_heads")

    def get_rope_base(self) -> float:
        """Get the RoPE base value from model config.

        Returns:
            The RoPE base value.
        """
        return get_hf_config(self.model, "rope_base")

    def get_num_hidden_layers(self) -> int:
        """Get the number of hidden layers from model config.

        Returns:
            The number of hidden layers.
        """
        return get_hf_config(self.model, "num_hidden_layers")

    def get_norm_eps(self) -> int:
        """Get the normalization epsilon from model config.

        Returns:
            The normalization epsilon value.
        """
        return get_hf_config(self.model, "norm_eps")

    def get_vocab_size(self) -> int:
        """Get the vocabulary size from model config.

        Returns:
            The vocabulary size.
        """
        return get_hf_config(self.model, "vocab_size")

    def get_num_experts_per_tok(self) -> int:
        """Get the number of experts per token from model config.

        Returns:
            The number of experts per token.
        """
        return get_hf_config(self.model, "num_experts_per_tok")

    def get_num_local_experts(self) -> int:
        """Get the number of local experts from model config.

        Returns:
            The number of local experts.
        """
        return get_hf_config(self.model, "num_local_experts")

    def get_input_ids(self, inputs: Union[str, List[str]], dtype: Optional[torch.dtype] = None, **kwargs: Any) -> Any:
        """Convert input text to token IDs.

        Args:
            inputs: The input text or list of texts.
            dtype: The tensor data type to convert to.
            **kwargs: Additional arguments to pass to the tokenizer.

        Returns:
            The tokenized input IDs.
        """
        # Check the input type
        if isinstance(inputs, str):
            inputs = [inputs]
        # Set the padding token to eos token
        self.tokenizer.pad_token = self.tokenizer.eos_token
        # Tokenize the batched inputs
        input_ids = self.tokenizer(inputs, return_tensors="pt", padding=True, truncation=True, **kwargs)["input_ids"]
        # Check the dtype
        if dtype is None:
            return input_ids
        # Return the input
        return input_ids.to(dtype)

    def get_output_ids(self, dtype: Optional[torch.dtype] = None) -> torch.Tensor:
        """Get the output token IDs from text generation.

        Args:
            dtype: The tensor data type to convert to.

        Returns:
            The generated output token IDs or None if no generation has been performed.
        """
        # Check if output_ids is None
        if self.output_ids is None:
            err_msg = "No generation has been performed."
            raise ValueError(err_msg)

        # Check the dtype
        if dtype is None:
            return self.output_ids
        # Return the output
        return self.output_ids.to(dtype)

    def generate(self, input_ids: torch.Tensor, **kwargs: Any) -> torch.Tensor:
        """Generate text using the model.

        Args:
            input_ids: The input token IDs.
            **kwargs: Additional arguments to pass to the model's generate method.

        Returns:
            The generated token IDs.

        Raises:
            TypeError: If the model output is not a torch.Tensor.
        """
        self.output_ids = self.model.generate(input_ids, **kwargs)
        if not isinstance(self.output_ids, torch.Tensor):
            error_message = "Expected the model output to be a torch.Tensor"
            raise TypeError(error_message)
        return self.output_ids

    def get_rotary_embedding(self, max_length: Optional[int] = None) -> Tuple[torch.Tensor, torch.Tensor]:
        """Get the rotary embedding from the model.

        Args:
            max_length: The maximum length of the input tensor.

        Returns:
            The rotary embedding. (cos, sin)
        """
        # If max_length is not provided, use the maximum length from the model config
        if max_length is None:
            max_length = self.get_max_length()

        # Get the rotary embedding
        return self.rotary_emb.get_rotary_embedding(max_length)
