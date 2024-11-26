import numpy as np
from src.rx.decoders.polar.sc import PolarDecoder_SC

def create_decoder(code):
    if code.type == "polar":
        if code.decoder == "SC".lower():
            return PolarDecoder_SC(code)
        else:
            raise ValueError(f"Unsupported polar decoder type: {code.decoder}")    
    else:
        raise ValueError(f"Unsupported code type: {code.type}")


class Decoder:
    def __init__(self, code):
        self.decoder_type = code.type
        self.decoder = create_decoder(code)

    def __getattr__(self, name):
        # Forward method calls and attribute access to the decoder instance
        return getattr(self.decoder, name)
