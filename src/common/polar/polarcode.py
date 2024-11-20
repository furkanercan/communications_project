import numpy as np
import math

class PolarCode:
    def __init__(self, filepath, len_n, len_k, en_crc, len_r):
        """
        Initialize the PolarCode with information indices and frozen bits.
        """
        self.reliability_indices = self.readfile_polar_rel_idx(filepath)
        self.frozen_bits, self.info_indices = self.create_polar_indices(len_n, len_k, en_crc, len_r)


    def readfile_polar_rel_idx(self, filepath):
        reliability_indices = []

        try:
            with open(filepath, 'r') as file:
                # Read each line from the file and append it to the vector
                for line in file:
                    values = line.split()
                    if not all(value.isdigit() for value in values):
                        raise ValueError("File contains non-integer values.")
                    reliability_indices.extend([int(x) for x in values])
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filepath}' not found.")
        except Exception as e:
            raise RuntimeError(f"An error occurred: {e}")
        
        return reliability_indices


    def create_polar_indices(self, len_n, len_k, en_crc, len_r):
        """
        Create frozen and information bit indices for the polar code.

        Args:
            len_n (int): Block length (N).
            len_k (int): Number of information bits (K).
            en_crc (bool): Whether CRC is enabled.
            len_r (int): Length of CRC (if enabled).

        Raises:
            ValueError: If any of the inputs are invalid.

        Returns:
            frozen_bits (np.ndarray): Updated frozen bit vector.
            info_indices (np.ndarray): Updated information bit indices.
        """
        if not isinstance(len_n, int) or len_n <= 0:
            raise ValueError("len_n must be a positive integer.")
        if not isinstance(len_k, int) or len_k <= 0:
            raise ValueError("len_k must be a positive integer.")
        if not isinstance(en_crc, bool):
            raise ValueError("en_crc must be a boolean value.")
        if not isinstance(len_r, int) or len_r < 0:
            raise ValueError("len_r must be a non-negative integer.")

        frozen_bits = np.ones(len_n, dtype=int)
        vec_polar_info = np.ones(len_n, dtype=int)

        len_i = len_k
        if(en_crc):
            len_i += len_r
        for num, index in enumerate(self.reliability_indices[:len_i], start=0):
            frozen_bits[index] = 0
        for num, index in enumerate(self.reliability_indices[len_i:], start=len_i):
            vec_polar_info[index] = 0 
            
        info_indices = np.nonzero(vec_polar_info)[0]

        return frozen_bits, info_indices


    def __repr__(self):
        truncated_info = self.info_indices[:10]
        truncated_frozen = self.frozen_bits[:10]
        truncated_rel = self.reliability_indices[:10]
        return (
            f"PolarCode("
            f"info_indices={truncated_info}... (truncated), "
            f"frozen_bits={truncated_frozen}... (truncated))"
            f"reliability indices={truncated_rel}... (truncated))"
        )