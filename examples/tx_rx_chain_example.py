import numpy as np
import math
from src.common.polar.polarcode import PolarCode
from src.tx.tx import Transmitter
from src.rx.rx import Receiver
from src.channel.awgn import ChannelAWGN

N = 8
k = 4
enable_crc = False
r = 0
len_logn = int(math.log2(N))
# file_polar         = "src/lib/ecc/polar/3gpp/n256_3gpp.pc"
file_polar         = "src/lib/ecc/polar/n8_awgn_s0.6.pc"

qbits_enable       = False
qbits_chnl         = 5
qbits_intl         = 5
qbits_frac         = 1
quant_step         =    2 **  qbits_frac
quant_chnl_upper   = (  2 ** (qbits_chnl -1) - 1)/quant_step
quant_chnl_lower   = (-(2 ** (qbits_chnl -1)))//  quant_step
quant_intl_max     = (  2 ** (qbits_intl -1) - 1)/quant_step
quant_intl_min     = (-(2 ** (qbits_intl -1)))//  quant_step

pc = PolarCode(file_polar, N, k, enable_crc, r) #(file_polar, k, r) olacak yakinda.

stdev = 0.0

transmitter = Transmitter(pc.info_indices, len_logn)
channel = ChannelAWGN(stdev)
receiver = Receiver(len_logn, pc.frozen_bits, qbits_enable, quant_intl_max, quant_intl_min)

vec_info = np.array([1, 1, 1, 0])

# evaluator = Evaluator() #BER, BLER, ITER, etc.

modulated_data = transmitter.tx_chain(vec_info)
received_data = channel.apply_awgn(modulated_data)
decoded_data = receiver.rx_chain(received_data, channel.variance)

print(decoded_data)


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