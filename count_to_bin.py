import numpy as np 

BIN_EDGES = [2, 5, 10, 25, 100]

def count_to_bin(counts):
    return np.digitize(counts, BIN_EDGES)