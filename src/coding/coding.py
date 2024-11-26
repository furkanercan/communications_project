import numpy as np
from src.coding.polar.polarcode import PolarCode
from src.coding.uncoded import Uncoded

def create_code(config):
    if config["type"].lower() == "polar":
        return PolarCode(config)
    elif config["type"].lower() == "uncoded":
        return Uncoded(config)   
    else:
        raise ValueError(f"Unsupported code type")

class Code:
    def __init__(self, config):
        self.type = config["type"].lower()
        self.code = create_code(config)
        self.decoder = config[self.type]["decoder"]["algorithm"].lower()

    def __getattr__(self, name):
        # Forward method calls and attribute access to the encoder instance
        return getattr(self.code, name)