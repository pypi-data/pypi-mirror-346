import numpy as np

def lecun_init(inp, out):
    std = np.sqrt(1 / inp)
    return np.random.randn(inp, out) * std

def xavier_init(inp, out):
    limit = np.sqrt(6 / (inp + out))
    return np.random.uniform(-limit, limit, (inp, out))

def he_init(inp, out):
    std = np.sqrt(2 / inp)
    return np.random.randn(inp, out) * std

def basic_uniform_init(inp, out):
    return np.random.uniform(-0.1, 0.1, (inp, out))

