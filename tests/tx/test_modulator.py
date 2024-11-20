import numpy as np
from src.tx.modulator import Modulator

def test_modulator_bpsk():
    data = np.array([1,  0,  0,  1,  1,  1,  0,  1])
    soln = np.array([-1, 1,  1,  -1, -1, -1, 1, -1])
    modulator = Modulator()
    data_mod = modulator.mod_bpsk(data)
    np.testing.assert_array_equal(data_mod, soln, err_msg="BPSK modulator test failed.")
    