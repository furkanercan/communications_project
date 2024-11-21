from src.rx.decoders.polar.sc import PolarDecoder_SC
from src.rx.demodulator import Demodulator

class Receiver:
    def __init__(self, len_logn, vec_polar_isfrozen, qtz_enable, qtz_int_max, qtz_int_min):
        """
        Initialize the Receiver with a decoder (abstraction).

        Args:
            vec_llr (list): Log-likelihood ratio (LLR) values for decoding.
            len_logn (int): log2(N), where N is the block length.
            vec_polar_isfrozen (list): Frozen bit indicator list.
            qtz_enable (bool): Whether quantization is enabled (default: False).
            qtz_int_max (int): Maximum quantization value.
            qtz_int_min (int): Minimum quantization value.
        """
        self.demodulator = Demodulator()
        self.decoder = PolarDecoder_SC(len_logn, vec_polar_isfrozen, qtz_enable, qtz_int_max, qtz_int_min)
        self.decoder.initialize_decoder()
        

    def rx_chain(self, channel_data, awgn_var):
        """
        Perform the receive chain, including decoding.

        Returns:
            list: Decoded data.
        """
        # Placeholder for more functionalities (e.g., channel equalization)
        vec_llr = self.demodulator.softDemod_bpsk(channel_data, awgn_var)
        decoded_data = self.decoder.dec_sc(vec_llr)
        return decoded_data

