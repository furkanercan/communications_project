import numpy as np
import math


class Modulator:
    def __init__(self, config):
        self.scheme = config["type"].lower()
        self.validate_scheme()

    def validate_scheme(self):
        valid_schemes = ["bpsk", "qpsk", "16qam", "64qam"]
        if self.scheme not in valid_schemes:
            raise ValueError(f"Unsupported modulation scheme: {self.scheme}. Supported schemes: {valid_schemes}")

    def modulate(self, modulated_data, bool_data):
        """
        Modulate the given data based on the selected scheme.
        Args:
            data (np.ndarray): Input bits to modulate (1D array of 0s and 1s).

        Returns:
            np.ndarray: Modulated symbols.
        """
        
        if self.scheme == "bpsk":
            self.mod_bpsk(modulated_data, bool_data)
        elif self.scheme == "qpsk":
            self.mod_qpsk(modulated_data, bool_data)
        # elif self.scheme == "16qam":
        #     self.mod_qam(modulated_data, bool_data)
        # elif self.scheme == "64qam":
        #     self.mod_qam(modulated_data, bool_data)

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

    def mod_qpsk(self, modulated_data, bool_data):
        """QPSK modulation: Map bits to quadrature phase"""
        
        if len(bool_data) % 2 != 0:
            raise ValueError("Number of input bits must be even for QPSK.") #Solve this later.
        
        bool_data = bool_data.reshape(-1, 2)  # Reshape to pairs of bits
        mapping = {0:  1, 
                   1: -1}
        i = np.array([mapping[bit] for bit in bool_data[:, 0]])  # In-phase
        q = np.array([mapping[bit] for bit in bool_data[:, 1]])  # Quadrature
        modulated_data[:] =  i + 1j * q