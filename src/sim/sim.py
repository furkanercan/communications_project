import numpy as np

class Simulation:
    def __init__(self, config):
        self.num_frames = config["loop"]["num_frames"]
        self.num_errors = config["loop"]["num_errors"]
        self.max_frames = config["loop"]["max_frames"]