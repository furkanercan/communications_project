import numpy as np
from src.tx.encoders.encoder import Encoder
from src.tx.modulator import Modulator

class Transmitter:
    def __init__(self, mod_config, code):
        """
        Initialize the Transmitter with an encoder (abstraction).

        Args:
            vec_polar_info_indices (list): decoder information bit index list
            len_logn (int): log2(N), where N is the block length.
        """
        # self.encoder = PolarEncoder(vec_polar_info_indices, len_logn)
        self.encoder = Encoder(code)
        self.modulator = Modulator(mod_config)
        
        self.encoded_data = np.empty(code.len_n, dtype=bool)
        
        self.modulation_scheme = mod_config["type"].lower()

        if self.modulation_scheme == "bpsk":
            self.modulated_data = np.empty(code.len_n, dtype=int)  # Real values for BPSK
        elif self.modulation_scheme == "qpsk":
            self.modulated_data = np.empty(code.len_n // 2, dtype=complex)  # Complex values for QPSK
        elif self.modulation_scheme == "16qam":
            self.modulated_data = np.empty(code.len_n // 4, dtype=complex)  # Complex values for QPSK
        elif self.modulation_scheme == "64qam":
            self.modulated_data = np.empty(code.len_n // 6, dtype=complex)  # Complex values for QPSK
        elif self.modulation_scheme == "256qam":
            self.modulated_data = np.empty(code.len_n // 8, dtype=complex)  # Complex values for QPSK
        else:
            raise ValueError(f"Unsupported modulation scheme: {self.modulation_scheme}")

    def tx_chain(self, uncoded_data):
        self.encoder.encoder.encode_chain(self.encoded_data, uncoded_data)
        self.modulator.modulate(self.modulated_data, self.encoded_data)
        #other functionalities TBD
        # return modulated_data