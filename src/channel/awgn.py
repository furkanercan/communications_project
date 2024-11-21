import numpy as np
import math

class ChannelAWGN:
    def __init__(self, config):
        self.source = config["type"].lower()
        self.simpoints = config["snr"]["simpoints"]
        self.lenpoints = config["snr"]["len_points"]
        if(self.source == "snr"):
            snr_linear = 10 ** (self.simpoints / 10) 
            self.variance = 1/snr_linear
            self.stdev = np.sqrt(self.variance)
        else:
            TypeError("Current version only supports SNR(dB) type simulation!")

        self.mean = 0

    def apply_awgn(self, vec_mod, stdev):
        len_n = len(vec_mod)
        vec_awgn = np.random.normal(loc=0, scale=stdev, size=(len_n)) # Generate noise
        return vec_mod + vec_awgn