import numpy as np
import math
import string

from src.common.polar.polarcode import PolarCode
from src.tx.tx import Transmitter
from src.rx.rx import Receiver
from src.sim.sim import Simulation
from src.channel.awgn import ChannelAWGN
from src.utils.validation.config_loader import ConfigLoader
from src.utils.output_handler import *
from src.utils.create_run_id import *


seed = 42
config_file = "config.json5"
config = ConfigLoader(config_file).get()
run_id = create_run_id(config["code"]["type"], seed)
output_folder = create_output_folder(run_id)
save_config_to_folder(config, output_folder)

code_config = config["code"]
channel_config = config["channel"]
mod_config = config["mod"]
sim_config = config["sim"]

sim = Simulation(sim_config)
pc = PolarCode(code_config) # This need to be in receiver??
transmitter = Transmitter(pc.info_indices, pc.len_logn)
channel = ChannelAWGN(channel_config)
receiver = Receiver(pc.len_logn, pc.frozen_bits, pc.qtz_enable, pc.qtz_int_max, pc.qtz_int_min)

frame_count        = np.zeros(channel.lenpoints, dtype=int)
bit_error          = np.zeros(channel.lenpoints, dtype=int)
frame_error        = np.zeros(channel.lenpoints, dtype=int)
ber                = np.zeros(channel.lenpoints, dtype=float)
bler               = np.zeros(channel.lenpoints, dtype=float)

for idx, (stdev, var) in enumerate(zip(channel.stdev, channel.variance)):
    while((frame_count[idx] < sim.num_frames or frame_error[idx] < sim.num_errors) and frame_count[idx] > sim.max_frames):
        vec_info = np.zeros(pc.len_k)
        modulated_data = transmitter.tx_chain(vec_info)
        received_data = channel.apply_awgn(modulated_data, stdev)
        decoded_data = receiver.rx_chain(received_data, var)

        frame_count[idx] = frame_count[idx] + 1
        frame_error[idx] = frame_error[idx] + 1

        # print(decoded_data)

# evaluator = Evaluator() #BER, BLER, ITER, etc.
# # 1. Generate random data
# data = np.random.randint(0, 2, size=1000)

# # 2. Channel encoding
# vec_polar_info_indices, vec_polar_isfrozen, scfrel_flip_indices = create_polar_indices(self.len_n, self.len_k, self.en_crc, self.len_r, self.flip_max_iters, self.vec_polar_rel_idx)
# create_polar_enc_matrix(len_logn, vec_polar_info_indices)
# generator_matrix = ...  # Define generator matrix
# encoded_data = polar_encode(data, generator_matrix)

# # 3. Modulation
# modulated_signal = bpsk_modulate(encoded_data)

# # 4. Add noise (AWGN)
# noisy_signal = add_awgn(modulated_signal, snr_db=10)

# # 5. Demodulation
# received_bits = bpsk_demodulate(noisy_signal)

# # 6. Channel decoding
# decoded_data = polar_decode(received_bits, generator_matrix)

# # 7. Analyze performance
# ber = calculate_ber(data, decoded_data)
# print(f"Bit Error Rate: {ber}")