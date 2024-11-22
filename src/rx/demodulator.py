import numpy as np
import math

class Demodulator:
    def __init__(self, config):
        self.scheme = config["type"].lower()
        self.demod_type = config["demod_type"].lower()


    def demodulate(self, vec_output, input_data, awgn_var=None):
        """
        Wrapper function to handle modulation or demodulation.

        Args:
            mod_scheme (str): Modulation scheme ('bpsk' or 'qpsk').
            demod_type (str): Demodulation type ('soft' or 'hard').
            vec_output (np.ndarray): Output array to store results (LLRs or bits).
            input_data (np.ndarray): Input data for modulation/demodulation.
            awgn_var (float, optional): Noise variance for soft demodulation.

        Returns:
            None: Updates `vec_output` in place.
        """
        if self.scheme == "bpsk":
            if self.demod_type == "soft":
                if awgn_var is None:
                    raise ValueError("Noise variance is required for soft demodulation.")
                self.softDemod_bpsk(vec_output, input_data, awgn_var)
            elif self.demod_type == "hard":
                self.hardDemod_bpsk(vec_output, input_data)
            else:
                raise ValueError(f"Unsupported demodulation type: {self.demod_type}")
        elif self.scheme == "qpsk":
            if self.demod_type == "soft":
                if awgn_var is None:
                    raise ValueError("Noise variance is required for soft demodulation.")
                self.softDemod_qpsk(vec_output, input_data, awgn_var)
            elif self.demod_type == "hard":
                self.hardDemod_qpsk(vec_output, input_data)
            else:
                raise ValueError(f"Unsupported demodulation type: {self.demod_type}")
        else:
            raise ValueError(f"Unsupported modulation scheme: {self.scheme}")


    def softDemod_bpsk(self, vec_llr, input_data, awgn_var):
        vec_llr[:] = 2 * (input_data) / awgn_var 

    def hardDemod_bpsk(self, vec_hd, input_data):
        input_data = np.array(input_data)
        vec_hd[:] = np.where(input_data < 0, 1, 0)
        
    def hardDemod_qpsk(self, vec_hd, input_data):
        """
        QPSK demodulation: Recover bits from QPSK symbols.

        Args:
            input_data (np.ndarray): Complex QPSK symbols.

        Returns:
            np.ndarray: Recovered bit sequence.
        """
        i = np.real(input_data)  # In-phase component
        q = np.imag(input_data)  # Quadrature component

        # Map signs to bits
        bits_i = (i > 0).astype(int)
        bits_q = (q > 0).astype(int)

        # Combine bits and flatten
        return np.column_stack((bits_i, bits_q)).flatten()
    

    def softDemod_qpsk(self, vec_llr, input_data, awgn_var):
        """
        Perform QPSK soft demodulation to compute LLRs.

        Args:
            input_data (np.ndarray): Complex QPSK symbols (received).
            awgn_var (float): Noise variance (sigma^2).

        Returns:
            np.ndarray: LLRs for each bit (1D array, 2 LLRs per symbol).
        """
        # Compute scaling factor for LLRs
        scaling_factor = 2 / awgn_var

        # Extract real and imaginary parts
        llr_i = scaling_factor * np.real(input_data)  # LLR for in-phase bits
        llr_q = scaling_factor * np.imag(input_data)  # LLR for quadrature bits

        # Interleave LLRs: [LLR_i1, LLR_q1, LLR_i2, LLR_q2, ...]
        # llrs = np.empty(2 * len(input_data))
        vec_llr[0::2] = llr_i  # Place LLRs for in-phase bits in even indices
        vec_llr[1::2] = llr_q  # Place LLRs for quadrature bits in odd indices
