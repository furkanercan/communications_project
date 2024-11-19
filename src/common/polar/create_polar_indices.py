import numpy as np

def create_polar_indices(len_n, len_k, en_crc, len_r, flip_max_iters, vec_polar_rel_idx):
    vec_polar_isfrozen = np.ones(len_n, dtype=int)
    vec_polar_info = np.ones(len_n, dtype=int)

    len_i = len_k
    if(en_crc):
        len_i += len_r
    for num, index in enumerate(vec_polar_rel_idx[:len_i], start=0):
        vec_polar_isfrozen[index] = 0
    for num, index in enumerate(vec_polar_rel_idx[len_i:], start=len_i):
        vec_polar_info[index] = 0 
        
    vec_polar_info_indices = np.nonzero(vec_polar_info)[0]

    return vec_polar_info_indices, vec_polar_isfrozen