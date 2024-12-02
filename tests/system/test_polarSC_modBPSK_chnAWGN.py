import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import numpy as np
import math
import string
import time

from src.coding.coding import Code
from src.sim.sim import Simulation
from src.channel.awgn import ChannelAWGN
from src.utils.validation.config_loader import ConfigLoader
from src.utils.output_handler import *
from src.utils.create_run_id import *
from src.utils.timekeeper import *

from src.tx.encoders.encoder import PolarEncoder
from src.tx.modulator import Modulator
from src.rx.demodulator import Demodulator

from src.coding.coding import Code
from src.rx.decoders.polar.sc import PolarDecoder_SC

def parse_reference_data(config):
    """
    Parse reference data (SNR, BER, BLER) from the config dictionary.
    The data should be in scientific notation as lists of floats.
    """
    reference_data = config.get("reference", {})

    snr = reference_data.get("snr", [])
    ber = reference_data.get("ber", [])
    bler = reference_data.get("bler", [])

    # Convert to floating-point numbers, ensuring correct parsing of scientific notation
    snr = [float(val) for val in snr]
    ber = [float(val) for val in ber]
    bler = [float(val) for val in bler]

    return snr, ber, bler

def main_test_polar_sc(config_file):
    seed = 42
    np.random.seed(seed)
    configloader = ConfigLoader(config_file)
    config = configloader.get()
    ref_snr, ref_ber, ref_bler = parse_reference_data(configloader.raw_config)

    code_config    = config["code"]
    channel_config = config["channel"]
    mod_config     = config["mod"]
    sim_config     = config["sim"]

    sim         = Simulation(sim_config)
    code        = Code(code_config) 
    encoder     = PolarEncoder(code)
    modulator   = Modulator(mod_config)
    channel     = ChannelAWGN(channel_config, seed)
    demodulator = Demodulator(mod_config)
    decoder     = PolarDecoder_SC(code)
    decoder.initialize_decoder()

    len_k = code.len_k
    len_n = code.len_n
    # status_msg, prev_status_msg = [], []

    info_data      = np.empty(len_k, dtype=np.int32) 
    encoded_data   = np.empty(len_n, dtype=np.int32) 
    modulated_data = np.empty(len_n, dtype=np.int32) #CONFIG MUST BE BPSK!
    received_data  = np.empty(len_n, dtype=np.float32) 
    vec_llr        = np.empty(len_n, dtype=np.float32)
    decoded_data   = np.empty(len_k, dtype=np.bool)

    tolerance = 1e-6

    for idx, (stdev, var) in enumerate(zip(channel.stdev, channel.variance)):
        # time_start = time.time()
        snr_point = config["channel"]["snr"]["simpoints"]
        while(sim.run_simulation(idx)):
            info_data[:] = np.random.randint(0, 2, size=len_k)
            encoder.encode_chain(encoded_data, info_data)
            modulator.modulate(modulated_data, encoded_data)
            received_data[:] = channel.apply_awgn(modulated_data, stdev, var)
            demodulator.demodulate(vec_llr, received_data, var)
            decoder.decode_chain(decoded_data, vec_llr)
            sim.collect_run_stats(idx, 1023, 1, info_data, decoded_data)

            # if(sim.count_frame[idx] % 100 == 0):
            #     time_end = time.time()
            #     time_elapsed = time_end - time_start
            #     sim.update_run_results(idx, len_k)
            #     status_msg = sim.display_run_results_temp(idx, snr_point[idx], format_time(time_elapsed), prev_status_msg)
            #     prev_status_msg = status_msg

        # time_end = time.time()
        # time_elapsed = time_end - time_start   
        sim.update_run_results(idx, len_k)

        # Validate against the reference data with tolerance
        assert abs(snr_point[idx] - ref_snr[idx])  <= tolerance, f"SNR mismatch at point {snr_point[idx]} (expected {ref_snr[idx]})"
        assert abs(sim.ber[idx]   - ref_ber[idx])  <= tolerance, f"BER mismatch at point {sim.ber[idx]} (expected {ref_ber[idx]})"
        assert abs(sim.bler[idx]  - ref_bler[idx]) <= tolerance, f"BLER mismatch at point {sim.bler[idx]} (expected {ref_bler[idx]})"

        
        # status_msg = sim.display_run_results_perm(idx, snr_point[idx], format_time(time_elapsed), prev_status_msg)
        # prev_status_msg = status_msg


def test_polar_sc():
    config_file1 = "tests/system/config_test_polarSC_modBPSK_chnAWGN.json5"
    main_test_polar_sc(config_file1)

# test_polar_sc()

## Check exactness, and closeness (issue warning for closeness - put notes on what are the current versions of things, etc.)
## Test for library versions????