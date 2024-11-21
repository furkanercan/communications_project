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

    start = config["start"]
    end = config["end"]
    step = config["step"]

    # Ensure 'end' is greater than or equal to 'start'
    if end < start:
        raise ValueError(f"'channel.snr.end' ({end}) must be greater than or equal to 'channel.snr.start' ({start}).")

    # Ensure 'step' is positive
    if step <= 0:
        raise ValueError(f"'channel.snr.step' ({step}) must be positive.")

    # # Ensure 'step' is not larger than the range
    # if step > (end - start):
    #     raise ValueError(f"'channel.snr.step' ({step}) cannot be larger than the range ('end' - 'start' = {end - start}).")

    # # Ensure the range can produce at least one value
    # if start == end and step > 0:
    #     raise ValueError(f"'channel.snr' range [{start}, {end}] with step {step} produces no values. Check the configuration.")

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

    num_frames = config["num_frames"]
    num_errors = config["num_errors"]
    num_max_frames = config["num_max_frames"]

    if num_frames < 0:
        raise ValueError(f"'sim.loop.num_frames' ({num_frames}) must be a non-negative value.")
    if num_errors < 0:
        raise ValueError(f"'sim.loop.num_errors' ({num_errors}) must be a non-negative value.")
    if num_max_frames < 0:
        raise ValueError(f"'sim.loop.num_max_frames' ({num_max_frames}) must be a non-negative value.")

    return config



def validate_config_sim_save(config):
    optional_keys = {
        "plot_enable": (bool, False),
        "lutsim_enable": (bool, False),
        "save_output": (bool, True)
    }

    validate_optional_keys(config, optional_keys, "sim.loop")

    return config