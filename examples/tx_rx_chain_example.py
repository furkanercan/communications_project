import numpy as np
from src.common.create_polar_indices import create_polar_indices
from src.tx.channel_encoder import PolarEncoder
# from src.tx.modulator import bpsk_modulate
# from src.channel.awgn import add_awgn
# from src.rx.demodulator import bpsk_demodulate
# from src.rx.channel_decoder import polar_decode


def test_polar_encoder():
    len_logn = 3
    vec_polar_info_indices = [0, 1, 4, 5]
    uncoded_data = [1, 0, 1, 1]
    
    encoder = PolarEncoder(vec_polar_info_indices)
    encoder.create_polar_matrices(len_logn)
    
    encoded_data = encoder.polar_encode(uncoded_data)
    assert len(encoded_data) == 8  # Block length for len_logn=3
    assert (encoded_data == (np.array(uncoded_data) @ encoder.matG_kxN) % 2).all()

    matrices = encoder.export_matrices()
    assert matrices["matG_NxN"].shape == (8, 8)
    assert matrices["matG_kxN"].shape == (4, 8)
    assert matrices["matH"].shape == (4, 8)  # Assuming 4 non-info bits

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