"""Mixtral model configuration mapping.

This module contains the configuration mapping for Mixtral model parameters,
mapping the standard parameter names used in LLM-Probe to the actual
parameter names used in the Mixtral model configuration.
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
    "num_experts_per_tok": "num_experts_per_tok",
    "num_local_experts": "num_local_experts",
    "norm_eps": "rms_norm_eps",
    "rope_base": "rope_theta",
    "vocab_size": "vocab_size",
}

# Layer naming pattern table
name_pattern = {
    "gate_name_pattern": "model.layers.<l>.block_sparse_moe.gate",
    "w1_name_pattern": "model.layers.<l>.block_sparse_moe.experts.<e>.w1",
    "w2_name_pattern": "model.layers.<l>.block_sparse_moe.experts.<e>.w2",
    "w3_name_pattern": "model.layers.<l>.block_sparse_moe.experts.<e>.w3",
}
