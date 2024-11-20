import numpy as np
# from src.common.create_polar_indices import create_polar_indices
from src.tx.tx import Transmitter

def test_transmitter():
    # Initialize test variables
    len_logn = 3
    vec_polar_info_indices = [3, 5, 6, 7]
    uncoded_data = [1, 0, 1, 1]
    
    # Instantiate and call class
    transmitter = Transmitter(vec_polar_info_indices,len_logn)
    transmitted_data = transmitter.tx_chain(uncoded_data)
    
    # Test the outcome
    assert len(transmitted_data) == 8  # Block length for len_logn=3
    # assert (transmitted_data == (np.array(uncoded_data) @ transmitter.encoder.matG_kxN) % 2).all()

    matrices = transmitter.encoder.export_matrices()
    assert matrices["matG_NxN"].shape == (8, 8)
    assert matrices["matG_kxN"].shape == (4, 8)
    assert matrices["matHt"].shape == (8, 4)  # Assuming 4 non-info bits
