from src.utils.validation.config_validator_polar import *
from src.utils.validation.validate_keys import *

def validate_config_code(config):
    required_keys = {
        "type": str,
    }

    optional_keys = {
        "polar": dict # delegate to validate_polar
    }

    validate_required_keys(config, required_keys, "code")
        
    if "polar" in config:
        config["polar"] = validate_config_polar(config["polar"])
    # Other codes will follow here. (LDPC, Turbo, CRC, RS, BCH, OSD, etc.)

    return config




def validate_config_modulator(config):
    required_keys = {
        "type": str,
    }

    validate_required_keys(config, required_keys, "code")

    return config




def validate_config_channel(config):
    required_keys = {
        "type": str
    }
    optional_keys = {
        "snr": dict  # Delegate to `validate_channel_snr_config`
        # "ebn0": dict  # Delegate to `validate_channel_ebn0_config`
    }

    validate_required_keys(config, required_keys, "config")

    if "snr" in config:
        config["snr"] = validate_config_channel_snr(config["snr"])

    return config



def validate_config_channel_snr(config):
    required_keys = {
        "start": (int, float),
        "end": (int, float),
        "step": (int, float)
    }

    validate_required_keys(config, required_keys, "channel.snr")

    return config




def validate_config_sim(config):
    required_keys = {
        "loop": dict,  # Delegate to `validate_loop_config`
        "save": dict    # Delegate to `validate_save_config`
    }

    validate_required_keys(config, required_keys, "sim")

    config["loop"] = validate_config_sim_loop(config["loop"])
    config["save"] = validate_config_sim_save(config["save"])

    return config



def validate_config_sim_loop(config):
    required_keys = {
        "num_frames": int,  
        "num_errors": int   
    }
    optional_keys = {
        "num_max_frames": (int, 1e7),  
    }

    validate_required_keys(config, required_keys, "sim.loop")
    validate_optional_keys(config, optional_keys, "sim.loop")

    return config



def validate_config_sim_save(config):
    optional_keys = {
        "plot_enable": (int, 0),
        "lutsim_enable": (int, 0),
        "save_output": (int, 1) 
    }

    validate_optional_keys(config, optional_keys, "sim.loop")

    return config