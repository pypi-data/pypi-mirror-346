##########################################################################
##  HugigngFace Model Config Parser
##
##  Authors:  Junsoo    Kim   ( js.kim@hyperaccel.ai        )
##  Version:  0.0.10
##  Date:     2025-01-15      ( v0.0.10, init               )
##
##########################################################################

from typing import Any

from transformers import AutoModelForCausalLM

from llm_probe.models.gpt2 import cfg as gpt2_cfg
from llm_probe.models.gpt2 import name_pattern as gpt2_pat
from llm_probe.models.llama import cfg as llama_cfg
from llm_probe.models.llama import name_pattern as llama_pat
from llm_probe.models.mixtral import cfg as mixtral_cfg
from llm_probe.models.mixtral import name_pattern as mixtral_pat
from llm_probe.utils import check_model_architecture

##########################################################################
## Function
##########################################################################


def get_hf_config(model: AutoModelForCausalLM, key: str) -> Any:
    """Get the model configuration from the model.

    Args:
        model: The model to get the configuration from.
        key: The key to get the configuration from.

    Returns:
        The model configuration.
    """
    # Get the model architecture
    architectures = model.config.architectures

    # Check if the model architecture is in the configuration table
    if check_model_architecture(model.config, "GPT2LMHeadModel"):
        cfg = gpt2_cfg
    elif check_model_architecture(model.config, "LlamaForCausalLM"):
        cfg = llama_cfg
    elif check_model_architecture(model.config, "MixtralForCausalLM"):
        cfg = mixtral_cfg
    else:
        err_msg = f"Unsupported model architecture: {architectures}"
        raise NotImplementedError(err_msg)

    # Check if the key is in the configuration table
    if key not in cfg:
        err_msg = f"Invalid key: {key} in this architecture"
        raise ValueError(err_msg)
    # Check if the key is in the model configuration
    if not hasattr(model.config, cfg[key]):
        err_msg = f"Invalid key: {key} in this model"
        raise ValueError(err_msg)
    return getattr(model.config, cfg[key])


def get_hf_name_pattern(model: AutoModelForCausalLM, key: str) -> Any:
    """Get the model name pattern from the model.

    Args:
        model: The model to get the name pattern from.
        key: The key to get the name pattern from.
    """
    # Get the model architecture
    architectures = model.config.architectures

    # Check if the model architecture is in the configuration table
    if check_model_architecture(model.config, "MixtralForCausalLM"):
        pat = mixtral_pat
    else:
        err_msg = f"Unsupported model architecture: {architectures}"
        raise NotImplementedError(err_msg)

    # Check if the key is in the configuration table
    if key not in pat:
        err_msg = f"Invalid key: {key} in this architecture"
        raise ValueError(err_msg)
    return pat[key]


##########################################################################
