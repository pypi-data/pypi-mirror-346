import numpy as np
from .initializers import he_init, xavier_init, lecun_init, basic_uniform_init

class _linear:
    def __init__(self):
        pass
    def get_function(self):
        return lambda x: x
    def get_derivative(self):
        return lambda x: 1
    def get_weights(self, inp, out):
        return basic_uniform_init(inp, out)

class _relu:
    def __init__(self):
        pass
    def get_function(self):
        return lambda x: np.maximum(0, x)
    def get_derivative(self):
        return lambda x: np.where(x > 0, 1, 0)
    def get_weights(self, inp, out):
        return he_init(inp, out)

class _sigmoid:
    def __init__(self):
        pass
    def get_function(self):
        return lambda x: 1 / (1 + np.exp(-x))
    def get_derivative(self):
        return lambda x: x * (1 - x)
    def get_weights(self, inp, out):
        return lecun_init(inp, out)

class _swish:
    def __init__(self):
        pass
    def get_function(self):
        return lambda x: x / (1 + np.exp(-x))
    def get_derivative(self):
        return lambda x: (1 + x + x * np.exp(-x)) / np.square(1 + np.exp(-x))
    def get_weights(self, inp, out):
        return he_init(inp, out)

class _tanh:
    def __init__(self):
        pass
    def get_function(self):
        return lambda x: np.tanh(x)
    def get_derivative(self):
        return lambda x: 1 - np.square(np.tanh(x))
    def get_weights(self, inp, out):
        return xavier_init(inp, out)

class _leaky_relu:
    def __init__(self, a=0.01):
        self.a = a
    def get_function(self):
        return lambda x: np.where(x > 0, x, self.a * x)
    def get_derivative(self):
        return lambda x: np.where(x > 0, 1, self.a)
    def get_weights(self, inp, out):
        return he_init(inp, out)

class _elu:
    def __init__(self, a=1):
        self.a = a
    def get_function(self):
        return lambda x: np.where(x > 0, x, self.a * (np.exp(x) - 1))
    def get_derivative(self):
        return lambda x: np.where(x > 0, 1, self.a * np.exp(x))
    def get_weights(self, inp, out):
        return he_init(inp, out)

class _softmax:
    def __init__(self):
        pass
    def _function(self, x):
        exps = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exps / np.sum(exps, axis=1, keepdims=True)
    def get_function(self):
        return self._function
    def get_derivative(self):
        return lambda y_true, y_pred: y_pred - y_true
    def get_weights(self, inp, out):
        return xavier_init(inp, out)

linear = _linear()
relu = _relu()
sigmoid = _sigmoid()
swish = _swish()
tanh = _tanh()
leaky_relu = lambda a=0.01: _leaky_relu(a)
elu = lambda a=1: _elu(a)
softmax = _softmax()
