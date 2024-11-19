import numpy as np
# from src.common.create_polar_indices import create_polar_indices
from src.tx.channel_encoder import PolarEncoder

def test_polar_encoder():
    # Initialize test variables
    len_logn = 3
    vec_polar_info_indices = [0, 1, 2, 4]
    uncoded_data = [1, 0, 1, 1]
    
    # Instantiate and call class
    encoder = PolarEncoder(vec_polar_info_indices)
    encoded_data = encoder.encode_chain(uncoded_data, len_logn)
    
    # Test the outcome
    assert len(encoded_data) == 8  # Block length for len_logn=3
    assert (encoded_data == (np.array(uncoded_data) @ encoder.matG_kxN) % 2).all()

    matrices = encoder.export_matrices()
    assert matrices["matG_NxN"].shape == (8, 8)
    assert matrices["matG_kxN"].shape == (4, 8)
    assert matrices["matHt"].shape == (8, 4)  # Assuming 4 non-info bits
