import numpy as np
from src.tx.channel_encoder import PolarEncoder
from src.tx.modulator import Modulator

class Transmitter:
    def __init__(self, vec_polar_info_indices, len_logn):
        """
        Initialize the Transmitter with an encoder (abstraction).

        Args:
            vec_polar_info_indices (list): decoder information bit index list
            len_logn (int): log2(N), where N is the block length.
        """
        self.encoder = PolarEncoder(vec_polar_info_indices, len_logn)
        self.modulator = Modulator()
        self.len_logn = len_logn
        self.len_n = 2**len_logn
        
        self.encoded_data = np.empty(self.len_n, dtype=bool)
        self.modulated_data = np.empty(self.len_n, dtype=int)

    def tx_chain(self, uncoded_data):
        self.encoder.encode_chain(self.encoded_data, uncoded_data)
        self.modulator.mod_bpsk(self.modulated_data, self.encoded_data)
        #other functionalities TBD
        # return modulated_data