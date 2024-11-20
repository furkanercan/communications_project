import numpy as np
from src.channel.awgn import ChannelAWGN

def test_awgn_channel():
    
    vec_mod = np.random.choice([-1, 1], size=100000)
    stdev = 0.35
    channel = ChannelAWGN()
    vec_awgn = channel.apply_awgn(vec_mod, stdev)

    noise = vec_awgn - vec_mod

    assert np.isclose(noise.mean(), 0, atol=1e-2), "Mean of noise is not close to 0."
    assert np.isclose(noise.std(), stdev, atol=1e-2), f"Stdev of noise is not close to {stdev}."
    