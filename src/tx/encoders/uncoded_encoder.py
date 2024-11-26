import numpy as np

class UncodedEncoder():
    """
    UncodedEncoder is a placeholder for uncoded codewords. It does not have any real function.
    """
    def __init__(self):
        pass

    def encode_chain(self, encoded_data, uncoded_data):
        encoded_data[:] = uncoded_data

