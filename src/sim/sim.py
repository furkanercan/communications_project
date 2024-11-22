import os
import datetime
import numpy as np

class Simulation:
    def __init__(self, config, output_folder, sim_size=50):
        self.num_frames = config["loop"]["num_frames"]
        self.num_errors = config["loop"]["num_errors"]
        self.max_frames = config["loop"]["max_frames"]

        self.plot_enable   = config["save"]["plot_enable"]
        self.lutsim_enable = config["save"]["lutsim_enable"]
        self.save_output   = config["save"]["save_output"]

        self.output_path = os.path.join(output_folder, "fec_results.out")
        
        self.snr_points         = np.zeros(sim_size, dtype=float)
        self.count_frame        = np.zeros(sim_size, dtype=int)
        self.count_dec_steps    = np.zeros(sim_size, dtype=int)
        self.count_dec_iters    = np.zeros(sim_size, dtype=int)
        self.count_bit_error    = np.zeros(sim_size, dtype=int)
        self.count_frame_error  = np.zeros(sim_size, dtype=int)
        self.ber                = np.zeros(sim_size, dtype=float)
        self.bler               = np.zeros(sim_size, dtype=float)
        self.avg_steps          = np.zeros(sim_size, dtype=float)
        self.avg_iters          = np.zeros(sim_size, dtype=float)

        self.generate_sim_header()


    def run_simulation(self, idx):
        min_frame_condition = (self.count_frame[idx] < self.num_frames)
        min_error_condition = (self.count_frame_error[idx] < self.num_errors)
        # max_frame_condition = (self.count_frame[idx] > self.max_frames)
        return (min_frame_condition or min_error_condition)# and max_frame_condition )
    

    def collect_run_stats(self, idx, dec_steps, dec_iters, info_data, decoded_data):
        self.count_frame[idx]       += 1
        self.count_dec_steps[idx]   += dec_steps
        self.count_dec_iters[idx]   += dec_iters
        self.count_frame_error[idx] += (1 if (info_data != decoded_data).any() else 0)
        self.count_bit_error[idx]   += np.sum(info_data != decoded_data)


    def update_run_results(self, idx, len_k):
        self.ber[idx]  = self.count_bit_error[idx]/(self.count_frame[idx] * len_k)
        self.bler[idx] = self.count_frame_error[idx]/self.count_frame[idx]
        self.avg_steps[idx] = self.count_dec_steps[idx]/self.count_frame[idx]
        self.avg_iters[idx] = self.count_dec_steps[idx]/self.count_frame[idx]

    def display_run_results_temp(self, idx, snr_point, time_elapsed, prev_status_msg):
        status_msg = f"{snr_point:.3e}   {self.ber[idx]:.5e}   {self.bler[idx]:.5e}   {self.avg_iters[idx]:.2e}   {self.count_frame[idx]:.2e}   {self.count_frame_error[idx]:.2e}   {time_elapsed}"
        status_pad = ' ' * max(0, len(prev_status_msg) - len(status_msg))
        end_char = '\r'
        print(status_msg + status_pad, end=end_char, flush=True)
        return status_msg

    def display_run_results_perm(self, idx, snr_point, time_elapsed, status_msg):
        prev_status_msg = status_msg
        status_msg = f"{snr_point:.3e}   {self.ber[idx]:.5e}   {self.bler[idx]:.5e}   {self.avg_iters[idx]:.2e}   {self.count_frame[idx]:.2e}   {self.count_frame_error[idx]:.2e}   {time_elapsed}"
        status_pad = ' ' * max(0, len(prev_status_msg) - len(status_msg))
        end_char = '\n'
        if self.save_output == 1:
            with open(self.output_path, 'a') as file_o:
                file_o.write(status_msg + "\n")

        print(status_msg + status_pad, end=end_char, flush=True)
        return status_msg
    

    def generate_sim_header(self):
        header_lines = [
            "#################################################################################",
            "#                                                                               #",
            "#  Successive Cancellation Decoder for Polar Codes            __                #",
            "#  Author: Furkan Ercan                               _(\    |@@|               #",
            "#                                                    (__/\__ \--/ __            #",
            "#  Copyright (c) {} Furkan Ercan.                     \___|----|  |   __      #".format(datetime.datetime.now().year),
            "#  All Rights Reserved.                                  \ }{ /\ )_ / _\ _\     #",
            "#                                                           /\__/\ \__O (__     #",
            "#  Version: 0.1                                            (--/\--)    \__/     #",
            "#                                                          _)(  )(_             #",
            "#  Licensed under the MIT License                         `---''---`            #",
            "#  See the LICENSE file for details.                                            #",
            "#                                                                               #",
            "#  ASCII Art Source: https://www.asciiart.eu/                                   #",
            "#                                                                               #",
            "#################################################################################",
            "",
            "SNR (dB)    BER           FER           ITER       Frames     Errors     Time",
        ]

        header = "\n".join(header_lines)
        print(header)
        if self.save_output == 1:
            with open(self.output_path, 'w') as file_o:
                file_o.write(header + "\n")
        return header