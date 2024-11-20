import numpy as np
from src.rx.demodulator import Demodulator


def test_demodulator_bpsk_hard():
    demodulator = Demodulator()
    data = np.array([-4, 0, 3, 8, 1, -9.1, 0.5, 0.001])
    soln = np.array([1, 0, 0, 0, 0, 1, 0, 0])
    demod_data = demodulator.hardDemod_bpsk(data)
    
    np.testing.assert_array_equal(demod_data, soln, err_msg="BPSK hard demodulator failed")

def test_demodulator_bpsk_soft():
    demodulator = Demodulator()
    data = np.array([-4, 0, 3, 8, 1, -9.1, 0.5, 0.001])
    variance = 0.25
    soln = 2*data/variance
    demod_data = demodulator.softDemod_bpsk(data, variance)
    
    np.testing.assert_array_equal(demod_data, soln, err_msg="BPSK soft demodulator failed")
