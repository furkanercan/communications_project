import numpy as np
from src.channel.awgn import ChannelAWGN
from src.utils.validation.config_validator import validate_config_channel

def test_awgn_channel():
    config = {
        'type': 'SNR',
        'snr': {
            'start': -2,
            'end': 15,
            'step': 0.5,
            'demod_type': 'hard'
        }
    }

    validate_config_channel(config)

    vec_mod = np.random.choice([-1, 1], size=100000)
    stdev = 0.35
    variance = stdev**2
    channel = ChannelAWGN(config)  # Pass the config to ChannelAWGN
    vec_awgn = channel.apply_awgn(vec_mod, stdev, variance)

    noise = vec_awgn - vec_mod

    # Assertions to check if the noise characteristics are as expected
    assert np.isclose(noise.mean(), 0, atol=1e-2), "Mean of noise is not close to 0."
    assert np.isclose(noise.std(), stdev, atol=1e-2), f"Stdev of noise is not close to {stdev}."

    