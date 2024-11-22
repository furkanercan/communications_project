import numpy as np
import math


class Modulator:
    def __init__(self):
        pass

    def mod_bpsk(self, modulated_data, bool_data):
        """
        Perform BPSK modulation.

        Args:
            bool_data (np.ndarray): Array of binary input bits (0s and 1s).

        Returns:
            np.ndarray: Array of modulated values (-1 and +1).
        
        Raises:
            ValueError: If bool_data contains values other than 0 or 1.
        """
        if not np.all(np.logical_or(bool_data == 0, bool_data == 1)):
            raise ValueError("input data to modulator must be Boolean.")
        
        bool_data = np.asarray(bool_data) # Ensure data type
        
        modulated_data[:] = 1 - 2 * bool_data