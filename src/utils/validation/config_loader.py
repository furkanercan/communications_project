import json
from src.utils.validation.validation_manager import validate_config

# Load config --> Validate config --> Cross-correlate config
# Validate: anything unrecognized should be flagged.
# Validate: types for each data, ranges if applicable
# Validate: if a parameter is missing. If essential, throw error. Otherwise, warning with default value (be conservative)
# Cross-correlate: parameters if applicable. For example, SNR start < SNR end, etc.
# Create calculable config params, but throw in conditions while doing so. e.g. if quant enabled, then calculate the vals.

class ConfigLoader:
    def __init__(self, config_file):
        with open(config_file, "r") as f:
            raw_config = json.load(f)

        self.config = validate_config(raw_config)

    def get(self):
        return self.config


# def calc_config_params(config):
#     quant = config["simulation"]["quant"]

#     quant["step"]         =    2 **  quant["qbits_frac"]
#     quant["chnl_upper"]   = (  2 ** (quant["qbits_chnl"] -1) - 1)/quant["step"]
#     quant["chnl_lower"]   = (-(2 ** (quant["qbits_chnl"] -1)))//  quant["step"]
#     quant["intl_max"]     = (  2 ** (quant["qbits_intl"] -1) - 1)/quant["step"]
#     quant["intl_min"]     = (-(2 ** (quant["qbits_intl"] -1)))//  quant["step"]