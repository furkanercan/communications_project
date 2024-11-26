import numpy as np
from src.coding.polar.polarcode import PolarCode

class Code:
    def __init__(self, config):
        self.codes = {
            "polar": PolarCode(config)
        }
        self.type = config["type"].lower()
        self.code = self.codes[self.type]
        self.decoder = config[self.type]["decoder"]["algorithm"].lower()

    def __getattr__(self, name):
        # Forward method calls and attribute access to the encoder instance
        return getattr(self.code, name)