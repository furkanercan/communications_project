import numpy as no
from src.tx.encoders.polar_encoder import PolarEncoder
from src.tx.encoders.uncoded_encoder import UncodedEncoder

def create_encoder(code):
    if code.type == "polar":
        return PolarEncoder(code)
    elif code.type == "uncoded":
        return UncodedEncoder()
    else:
        raise ValueError(f"Unsupported encoder (code) type: {code.type}")

class Encoder:
    def __init__(self, code):
        self.encoder_type = code.type
        self.encoder = create_encoder(code)

    def __getattr__(self, name):
        # Forward method calls and attribute access to the encoder instance
        return getattr(self.encoder, name)

