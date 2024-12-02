import numpy as np
from src.common.odfm import OFDM

class OFDMTransmitter:
    def __init__(self, ofdm_module):
        self.ofdm_module = ofdm_module

    def transmit(self, modulated_data):
        """Transmit modulated data using OFDM."""
        time_domain_signal = self.ofdm_module.perform_ifft(modulated_data)
        return self.ofdm_module.add_cyclic_prefix(time_domain_signal)
    
    