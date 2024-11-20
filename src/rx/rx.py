from src.rx.decoders.polar.sc import PolarDecoder_SC
from src.rx.demodulator import Demodulator

class Receiver:
    def __init__(self, len_logn, vec_polar_isfrozen, qbits_enable=False, quant_intl_max=7, quant_intl_min=-7):
        """
        Initialize the Receiver with a decoder (abstraction).

        Args:
            vec_llr (list): Log-likelihood ratio (LLR) values for decoding.
            len_logn (int): log2(N), where N is the block length.
            vec_polar_isfrozen (list): Frozen bit indicator list.
            qbits_enable (bool): Whether quantization is enabled (default: False).
            quant_intl_max (int): Maximum quantization value.
            quant_intl_min (int): Minimum quantization value.
        """
        self.demodulator = Demodulator()
        self.decoder = PolarDecoder_SC(len_logn, vec_polar_isfrozen, qbits_enable, quant_intl_max, quant_intl_min)
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

