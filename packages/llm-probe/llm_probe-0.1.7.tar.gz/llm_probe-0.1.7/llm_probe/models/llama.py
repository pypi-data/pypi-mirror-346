"""Llama model configuration mapping.

This module contains the configuration mapping for Llama model parameters,
mapping the standard parameter names used in LLM-Probe to the actual
parameter names used in the Llama model configuration.
"""

# Configuration table
cfg = {
    "architecture": "architectures",
    "bos_token_id": "bos_token_id",
    "eos_token_id": "eos_token_id",
    "hidden_act": "hidden_act",
    "hidden_size": "hidden_size",
    "intermediate_size": "intermediate_size",
    "max_length": "max_position_embeddings",
    "num_attention_heads": "num_attention_heads",
    "num_hidden_layers": "num_hidden_layers",
    "num_key_value_heads": "num_key_value_heads",
    "norm_eps": "rms_norm_eps",
    "rope_base": "rope_theta",
    "vocab_size": "vocab_size",
}

# Layer naming pattern table
name_pattern = None
