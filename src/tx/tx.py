from src.tx.channel_encoder import PolarEncoder

class Transmitter:
    def __init__(self, vec_polar_info_indices, len_logn):
        """
        Initialize the Transmitter with an encoder (abstraction).

        Args:
            encoder (PolarEncoder): Polar encoder class
            len_logn (int): log2(N), where N is the block length.
        """
        self.encoder = PolarEncoder(vec_polar_info_indices)
        self.len_logn = len_logn

    def tx_chain(self, uncoded_data):
        encoded_data = self.encoder.encode_chain(uncoded_data, self.len_logn)
        #other functionalities TBD
        return encoded_data