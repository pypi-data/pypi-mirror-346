"""Plugin for rotary embedding module."""

import logging
from typing import Any, Tuple

import torch
from transformers import PretrainedConfig

from llm_probe.utils import check_model_architecture

# Get the logger
logger = logging.getLogger(__name__)


class RotaryEmbedding:
    """Rotary embedding module."""

    def __init__(self, config: PretrainedConfig) -> None:
        """Initialize the rotary embedding module.

        Args:
            config: The configuration of the model.
        """
        self.config = config

        # Verify the architecture and get the rotary embedding
        self.rotary_emb: torch.nn.Module = self._verify_architecture()

    def get_rotary_embedding(self, max_length: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """Get the rotary embedding.

        Args:
            max_length: The maximum length of the input tensor.

        Returns:
            The cosine and sine values of the rotary embedding.
        """
        # Check if the rotary embedding is None
        if self.rotary_emb is None:
            err_msg = "The rotary embedding is not supported for this model."
            raise ValueError(err_msg)

        # Prepare the dummy input tensor and position ids
        x = torch.zeros((1, max_length, self.config.hidden_size))
        position_ids = torch.arange(0, max_length).reshape(1, 1, -1)

        # Get the rotary embedding
        cos, sin = self.rotary_emb(x, position_ids)

        # Resize the rotary embedding
        cos = cos.reshape(-1, max_length).permute(1, 0)
        sin = sin.reshape(-1, max_length).permute(1, 0)

        return cos, sin

    def _verify_architecture(self) -> Any:
        # Get the rotary embedding for each model architecture
        if check_model_architecture(self.config, "LlamaForCausalLM"):
            try:
                from transformers.models.llama.modeling_llama import LlamaRotaryEmbedding
            except ImportError as err:
                raise ImportError(
                    "LlamaRotaryEmbedding is not installed. Please check the version of the transformers library."
                ) from err
            rotary_emb = LlamaRotaryEmbedding(self.config)
        elif check_model_architecture(self.config, "MixtralForCausalLM"):
            try:
                from transformers.models.mixtral.modeling_mixtral import MixtralRotaryEmbedding
            except ImportError as err:
                raise ImportError(
                    "MixtralRotaryEmbedding is not installed. Please check the version of the transformers library."
                ) from err
            rotary_emb = MixtralRotaryEmbedding(self.config)
        else:
            logger.info(
                f"The model architecture {self.config.architectures[0]} is not supported for rotary embedding."
            )
            rotary_emb = None

        return rotary_emb
