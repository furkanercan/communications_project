import numpy as np
from src.common.odfm import OFDM

class OFDMReceiver:
    def __init__(self, ofdm_module):
        self.ofdm_module = ofdm_module

    def receive(self, received_signal):
        """Receive and process OFDM data."""
        signal_no_cp = self.ofdm_module.remove_cyclic_prefix(received_signal)
        frequency_domain_signal = self.ofdm_module.perform_fft(signal_no_cp)
        return frequency_domain_signal