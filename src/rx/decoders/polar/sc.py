import numpy as np
import math

class PolarDecoder_SC():
    def __init__(self, len_logn, vec_polar_isfrozen, qtz_enable, qtz_int_max, qtz_int_min):
        self.len_logn = int(len_logn)
        self.vec_polar_isfrozen = vec_polar_isfrozen
        self.mem_alpha = None
        self.mem_beta_l = None
        self.mem_beta_r = None
        self.vec_dec_sch = []
        self.vec_dec_sch_size = []
        self.vec_dec_sch_depth = []
        self.vec_dec_sch_dir = []
        self.qtz_enable = qtz_enable
        self.qtz_int_max = qtz_int_max
        self.qtz_int_min = qtz_int_min

    def initialize_decoder(self):
        if not self.vec_dec_sch:
            self.create_decoding_schedule()
            # raise ValueError("Decoder scheduling is not created - it must be created to continue decoding")
        self.mem_alpha =  [np.zeros((2**i)) for i in range(self.len_logn + 1)]
        self.mem_beta_l = [np.zeros((2**i), dtype=np.bool_) for i in range(self.len_logn + 1)]
        self.mem_beta_r = [np.zeros((2**i), dtype=np.bool_) for i in range(self.len_logn + 1)]


    def create_decoding_schedule(self):
        sch_limit = self.len_logn
        vec_dec_sch_init = ['F', 'H', 'G', 'H', 'C']
        self.vec_dec_sch = []
        self.call_decoding_schedule(vec_dec_sch_init, sch_limit)
        self.embed_frozen_nodes()
        self.create_decoding_stages()
        self.create_decoding_direction()


    def call_decoding_schedule(self, base_vector, sch_limit):
        for element in base_vector:
            if(element == 'H' and sch_limit > 1):
                self.call_decoding_schedule(base_vector, sch_limit-1)
            else:
                self.vec_dec_sch.append(element)

    def embed_frozen_nodes(self):
        j = 0 
        for i in range(len(self.vec_dec_sch)):
            if(self.vec_dec_sch[i] == 'H'):
                self.vec_dec_sch[i] = 'R1' if self.vec_polar_isfrozen[j] == 0 else 'R0'
                j+=1 

    def create_decoding_stages(self):
        sch_limit = self.len_logn
        self.vec_dec_sch_size = []
        self.vec_dec_sch_depth = []
        current_stagesize = np.power(2,sch_limit)
        for i in range(len(self.vec_dec_sch)):
            if(self.vec_dec_sch[i] == 'F'):
                self.vec_dec_sch_size.append(int(current_stagesize))
                self.vec_dec_sch_depth.append(int(np.log2(current_stagesize)))
                current_stagesize /= 2
            elif(self.vec_dec_sch[i] == 'G'):
                if(self.vec_dec_sch[i-1] == 'C' or self.isLeaf(self.vec_dec_sch[i-1])):
                    self.vec_dec_sch_size.append(int(current_stagesize*2))
                    self.vec_dec_sch_depth.append(int(np.log2(current_stagesize*2)))
                else:
                    self.vec_dec_sch_size.append(int(current_stagesize))
                    self.vec_dec_sch_depth.append(int(np.log2(current_stagesize)))
                    current_stagesize *= 2
            elif(self.vec_dec_sch[i] == 'C'):
                self.vec_dec_sch_size.append(int(current_stagesize))
                self.vec_dec_sch_depth.append(int(np.log2(current_stagesize)))
                current_stagesize *= 2
            else:
                self.vec_dec_sch_size.append(int(current_stagesize))
                self.vec_dec_sch_depth.append(int(np.log2(current_stagesize)))

    def create_decoding_direction(self):
        sch_limit = self.len_logn
        combine_ctr =  [0] * (sch_limit + 1)
        hard_dec_ctr = [0] * (sch_limit + 1)
        sc_direction = []

        for i in range(len(self.vec_dec_sch)):
            if self.vec_dec_sch[i] == 'C':
                sc_direction.append(combine_ctr[math.floor(math.log2(self.vec_dec_sch_size[i]))] % 2)
                combine_ctr[math.floor(math.log2(self.vec_dec_sch_size[i]))] += 1
            elif (self.vec_dec_sch[i] == 'R0' or self.vec_dec_sch[i] == 'R1'):
                sc_direction.append(hard_dec_ctr[math.floor(math.log2(self.vec_dec_sch_size[i]))] % 2)
                hard_dec_ctr[math.floor(math.log2(self.vec_dec_sch_size[i]))] += 1
            else:
                sc_direction.append(0)
        
        self.vec_dec_sch_dir = sc_direction

    def isLeaf(self, node):
        return node == 'R0' or node == 'R1'

    def dec_sc_f(self, stage_size, stage_depth, is_quantized, max_value):    
        """
        Perform F-node (function node) computation.

        Args:
            stage_size (int): The size of the current stage.
            stage_depth (int): The depth of the current stage in the decoding tree.
        """
        llr_a = self.mem_alpha[stage_depth][:stage_size // 2]
        llr_b = self.mem_alpha[stage_depth][stage_size // 2:]
        
        abs_llr = np.minimum(np.abs(llr_a), np.abs(llr_b))
        sign = np.sign(llr_a * llr_b)
        result = abs_llr * sign

        if is_quantized: #Only possible breach is when the result is 2^q and in 2s complement form.
            result = np.minimum(max_value, result)
        
        self.mem_alpha[stage_depth - 1][:stage_size // 2] = result

    def dec_sc_g(self, stage_size, stage_depth, is_quantized, max_value, min_value):
        """
        Perform G-node (function node) computation.

        Args:
            stage_size (int): The size of the current stage.
            stage_depth (int): The depth of the current stage in the decoding tree.
            is_quantized (bool): Whether the LLRs are quantized
            max_value (int): Max quantization value
            min_value (int): Min quantization value
        """
        llr_a = self.mem_alpha[stage_depth][:stage_size // 2]
        llr_b = self.mem_alpha[stage_depth][stage_size // 2:]

        mem_beta_slice = self.mem_beta_l[stage_depth - 1][:stage_size // 2]
        mem_alpha_slice = np.where(mem_beta_slice == 0, llr_b + llr_a, llr_b - llr_a)        

        if is_quantized:
            mem_alpha_slice = np.clip(mem_alpha_slice, min_value, max_value)

        self.mem_alpha[stage_depth - 1][:stage_size // 2] = mem_alpha_slice

    def dec_sc_c(self, stage_size, stage_depth, stage_dir):
        """
        Perform C-node (function node) computation.

        Args:
            stage_size (int): The size of the current stage.
            stage_depth (int): The depth of the current stage in the decoding tree.
            stage_dir (bool): The direction of the current stage.
        """
        beta_src1 = self.mem_beta_l[stage_depth][:stage_size]
        beta_src2 = self.mem_beta_r[stage_depth][:stage_size]
        beta_src1_int = beta_src1.astype(int)
        beta_src2_int = beta_src2.astype(int)
        
        if(stage_dir == 0):
            self.mem_beta_l[stage_depth + 1][:stage_size] = np.bitwise_xor(beta_src1_int, beta_src2_int)
            self.mem_beta_l[stage_depth + 1][stage_size:] = beta_src2_int
        else:
            self.mem_beta_r[stage_depth + 1][:stage_size] = np.bitwise_xor(beta_src1_int, beta_src2_int)
            self.mem_beta_r[stage_depth + 1][stage_size:] = beta_src2_int

    def dec_sc_h(self, llr, stage_dir):
        """
        Perform H-node (function node) computation.

        Args:
            llr (double): The LLR value to decode.
            stage_dir (bool): The direction of the current stage.
        """
        if(stage_dir == 0):
            self.mem_beta_l[0][0] = 1 if llr < 0 else 0
        else:
            self.mem_beta_r[0][0] = 1 if llr < 0 else 0


    def dec_sc(self, vec_llr):
        self.mem_alpha[self.len_logn][:] = vec_llr # Place LLRs to bottom row of mem_alpha
        vec_decoded = []
        info_ctr = 0
        for i in range(len(self.vec_dec_sch)):
            if self.vec_dec_sch[i] == 'F':
                self.dec_sc_f(self.vec_dec_sch_size[i], self.vec_dec_sch_depth[i], self.qtz_enable, self.qtz_int_max)
            elif self.vec_dec_sch[i] == 'G':
                self.dec_sc_g(self.vec_dec_sch_size[i], self.vec_dec_sch_depth[i], self.qtz_enable, self.qtz_int_max, self.qtz_int_min)
            elif self.vec_dec_sch[i] == 'C':
                self.dec_sc_c(self.vec_dec_sch_size[i], self.vec_dec_sch_depth[i], self.vec_dec_sch_dir[i])
            elif self.vec_dec_sch[i] == 'R0':
                if(self.vec_dec_sch_dir[i] == 0):
                    self.mem_beta_l[0][0] = 0
                else:
                    self.mem_beta_r[0][0] = 0
            elif self.vec_dec_sch[i] == 'R1':
                self.dec_sc_h(self.mem_alpha[0][0], self.vec_dec_sch_dir[i])
                if(self.vec_dec_sch_dir[i] == 0):
                    vec_decoded.append(self.mem_beta_l[0][0]) # May revert to POCO style if too slow.
                else:
                    vec_decoded.append(self.mem_beta_r[0][0])
                info_ctr += 1

        return vec_decoded