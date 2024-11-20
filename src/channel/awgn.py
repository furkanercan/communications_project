import numpy as np
import math

class ChannelAWGN:
    def __init__(self, stdev):
        self.mean = 0
        self.stdev = stdev
        self.variance = stdev**2

    def apply_awgn(self, vec_mod):
        len_n = len(vec_mod)
        vec_awgn = np.random.normal(loc=0, scale=self.stdev, size=(len_n)) # Generate noise
        return vec_mod + vec_awgn