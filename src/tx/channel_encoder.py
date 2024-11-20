import numpy as np

class PolarEncoder():
    """
    PolarEncoder handles encoding and parity-check matrix creation for polar codes.

    Attributes:
        vec_polar_info_indices (list): Indices of information bits.
        vec_polar_non_info_indices (list): Indices of non-information (frozen) bits.
        matG_kxN (ndarray): The pruned polar encoding matrix (kxN).
        matG_NxN (ndarray): The full polar encoding matrix (NxN).
        matHt (ndarray): The transposed parity-check matrix for the polar code (Nx(N-k))

    Methods:
        polar_encode(uncoded_data):
            Encodes the given uncoded data using the pruned encoding matrix.
        create_polar_matrices(len_logn):
            Generates the full encoding matrix and pruned encoding matrix.
        derive_parity_check_direct():
            Creates the parity-check matrix from the full encoding matrix.
    """
    def __init__(self, vec_polar_info_indices):
        """
        Initialize the PolarEncoder with necessary parameters.

        Args:
            vec_polar_info_indices (list): Indices of information bits.

        Raises:
            TypeError: If vec_polar_info_indices is not a list.
        """
        if not isinstance(vec_polar_info_indices, (list, np.ndarray)):
            raise TypeError("vec_polar_info_indices must be a list or a NumPy array.")

        self.vec_polar_info_indices = vec_polar_info_indices
        self.vec_polar_non_info_indices = None
        self.matG_kxN = None
        self.matG_NxN = None
        self.matHt = None

    def encode_chain(self, uncoded_data, len_logn):
        # Function must use generic name 'encode_chain' to ensure abstraction consistency (later on)!
        self.create_polar_matrices(int(len_logn))
        return self.polar_encode(uncoded_data)

    def polar_encode(self, uncoded_data):
        """
        Encodes the uncoded data with the generator matrix

        Returns: 
            np.array: encoded data
        
        Raises:
            TypeError: If uncoded_data is not a list.
            ValueError: If self.matG_kxN is not created yet.
        """
        if not isinstance(uncoded_data, (list, np.ndarray)):
            raise TypeError("uncoded_data must be a list or a NumPy array.")
        uncoded_data = np.array(uncoded_data) # Ensure it's a NumPy array
        if self.matG_kxN is None:
            raise ValueError("The k-by-N generator matrix must be created first.")
        return (uncoded_data @ self.matG_kxN) % 2

    def create_polar_matrices(self, len_logn):
        """
        Creates the polar matrices:
            - matG_kxN: The generator matrix in k-by-N form.
            - matG_NxN: The generator matrix in N-by-N form.
            - matHt   : The transposed parity-check matrix in N-by-(N-k) form.

        Raises:
            TypeError: If len_logn is not a positive integer.
        """
        if not isinstance(len_logn, int) or len_logn <= 0:
            raise TypeError("len_logn must be a positive integer")
        matG_core = np.array([[1, 0], [1, 1]])
        matG = matG_core  # Core matrix as the initial value
        for _ in range(len_logn-1):
            matG = np.kron(matG, matG_core)

        self.matG_NxN = matG                # Full NxN G matrix
        self.matG_kxN = matG[self.vec_polar_info_indices] # Pruned G matrix (kxN)
        self.derive_parity_check_direct()

    def derive_parity_check_direct(self):
        """
        Derives the parity-check matrix H from the full (NxN) encoding matrix G.

        Raises:
            ValueError: If matG_NxN is not yet created.
        """
        if self.matG_NxN is None:
            raise ValueError("Full encoding matrix (matG_NxN) must be created first.")

        N = self.matG_NxN.shape[1] # Total number of columns
        all_indices = set(range(N)) # Create a list of all indices
        self.vec_polar_non_info_indices = list(all_indices - set(self.vec_polar_info_indices)) # Determine the columns not in vec_polar_info_indices
        self.matHt = self.matG_NxN[:, self.vec_polar_non_info_indices] # Select these columns from matG_full and transpose them to form H

    def export_matrices(self):
        """
        Export the created matrices as a dictionary.

        Returns:
            dict: A dictionary containing matG_NxN, matG_kxN, and matHt.
        """
        return {
            "matG_NxN": self.matG_NxN,
            "matG_kxN": self.matG_kxN,
            "matHt": self.matHt
        }