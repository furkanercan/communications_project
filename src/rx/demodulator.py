import numpy as np
import math

class Demodulator:
    def __init__(self):
        pass

    def softDemod_bpsk(self, vec_llr, input_data, awgn_var):
        vec_llr[:] = 2 * (input_data) / awgn_var 

    def hardDemod_bpsk(self, vec_hd, input_data):
        input_data = np.array(input_data)
        vec_hd[:] = np.where(input_data < 0, 1, 0)
        
