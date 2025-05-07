"""GPT2 model configuration mapping.

This module contains the configuration mapping for GPT2 model parameters,
mapping the standard parameter names used in LLM-Probe to the actual
parameter names used in the GPT2 model configuration.
"""

# Configuration table
cfg = {
    "architecture": "architectures",
    "bos_token_id": "bos_token_id",
    "eos_token_id": "eos_token_id",
    "hidden_act": "activation_function",
    "hidden_size": "n_embd",
    "intermediate_size": "n_inner",
    "max_length": "n_positions",
    "num_attention_heads": "n_head",
    "num_hidden_layers": "n_layer",
    "norm_eps": "layer_norm_epsilon",
    "vocab_size": "vocab_size",
}

# Layer naming pattern table
name_pattern = None
