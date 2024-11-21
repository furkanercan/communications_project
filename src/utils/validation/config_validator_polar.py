import warnings
import numpy as np
from src.utils.validation.validate_keys import *

def validate_config_polar(config):
    required_keys = {
        "polar_file": str,
        "len_k": int
    }

    optional_keys = {
        "crc": dict,      # Delegate to `validate_crc_config`
        "decoder": dict,  # Delegate to `validate_decoder_config`
        "quantize": dict,    # Delegate to `validate_quant_config`
        "fast_enable": dict, # Delegate to `fast enable`
        "fast_max_size": dict # Delegate to `fast max size`
    }

    validate_required_keys(config, required_keys, "polar")

    # Validate optional nested sections
    if "crc" in config:
        config["crc"] = validate_config_polar_crc(config["crc"])
    if "decoder" in config:
        config["decoder"] = validate_config_polar_decoder(config["decoder"])
    if "quantize" in config:
        config["quantize"] = validate_config_polar_quantize(config["quantize"])
    if "fast_enable" in config:
        config["fast_enable"] = validate_config_polar_fast_enable(config["fast_enable"])
    if "fast_max_size" in config:
        config["fast_max_size"] = validate_config_polar_fast_max_size(config["fast_max_size"])

    return config



def validate_config_polar_fast_enable(config):

    optional_keys = {
        "rate0": (int, 0),
        "rate1": (int, 0),
        "rep": (int, 0),
        "spc": (int, 0),
        "ml_0101": (int, 0),
        "ml_0011": (int, 0)
    }

    validate_optional_keys(config, optional_keys, "polar.fast_enable")

    return config


def validate_config_polar_fast_max_size(config):

    optional_keys = {
        "rate0": (int, 4),
        "rate1": (int, 4),
        "rep": (int, 4),
        "spc": (int, 4)
    }

    validate_optional_keys(config, optional_keys, "polar.fast_max_size")

    return config



def validate_config_polar_decoder(config):
    required_keys = {
        "algorithm": str
    }

    optional_keys = {
        "flip_max_iters": (int, 10),
        "list_size": (int, 8)
    }

    validate_required_keys(config, required_keys, "polar.decoder")
    validate_optional_keys(config, optional_keys, "polar.decoder")

    return config




def validate_config_polar_crc(config):
    required_keys = {
        "enable": int,
        "length": int
    }

    validate_required_keys(config, required_keys, "polar.crc")

    return config



def validate_config_polar_quantize(config):
    optional_keys = {
        "enable": (int, 0),
        "bits_chnl": (int, 5),
        "bits_intl": (int, 6),
        "bits_frac": (int, 1)
    }

    validate_optional_keys(config, optional_keys, "polar.quantize")

    return config


