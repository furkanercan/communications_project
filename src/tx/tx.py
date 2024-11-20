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
        self.encoder = PolarEncoder(vec_polar_info_indices)
        self.modulator = Modulator()
        self.len_logn = len_logn

    def tx_chain(self, uncoded_data):
        encoded_data = self.encoder.encode_chain(uncoded_data, self.len_logn)
        modulated_data = self.modulator.mod_bpsk(encoded_data)
        #other functionalities TBD
        return modulated_data