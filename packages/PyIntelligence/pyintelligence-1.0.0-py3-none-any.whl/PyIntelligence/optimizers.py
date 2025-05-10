import numpy as np

class rmsprop:
    def __init__(self, learning_rate, gamma=0.9, epsilon=1e-8):
        self.lr = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.ema = {}
    def update(self, weights, gradients, layer_idx):
        if layer_idx not in self.ema:
            self.ema[layer_idx] = np.zeros_like(gradients)
        g_t = gradients
        ema = self.gamma * self.ema[layer_idx] + (1 - self.gamma) * np.square(g_t)
        self.ema[layer_idx] = ema
        return weights - self.lr / np.sqrt(ema + self.epsilon) * g_t 
           
class adam:
    def __init__(self, learning_rate, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.lr = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = {}
        self.v = {}
        self.t = 0

    def update(self, weights, gradients, layer_idx):
        if layer_idx not in self.m:
            self.m[layer_idx] = np.zeros_like(gradients)
            self.v[layer_idx] = np.zeros_like(gradients)

        self.t += 1
        self.m[layer_idx] = self.beta1 * self.m[layer_idx] + (1 - self.beta1) * gradients
        self.v[layer_idx] = self.beta2 * self.v[layer_idx] + (1 - self.beta2) * (gradients ** 2)

        m_hat = self.m[layer_idx] / (1 - self.beta1 ** self.t)
        v_hat = self.v[layer_idx] / (1 - self.beta2 ** self.t)

        return weights - self.lr * m_hat / (np.sqrt(v_hat) + self.epsilon)
    
class sgd:
    def __init__(self, learning_rate):
        self.lr = learning_rate

    def update(self, weights, gradients, layer_idx):
        return weights - self.lr * gradients

class momentum:
    def __init__(self, learning_rate, momentum=0.9):
        self.lr = learning_rate
        self.momentum = momentum
        self.v = {}

    def update(self, weights, gradients, layer_idx):
        if layer_idx not in self.v:
            self.v[layer_idx] = np.zeros_like(gradients)
        self.v[layer_idx] = self.momentum * self.v[layer_idx] - self.lr * gradients
        return weights + self.v[layer_idx]
