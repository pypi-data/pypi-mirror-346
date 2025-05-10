import numpy as np

class dense:
    def __init__(self, units, activation):
        self.units = units
        self.activation = activation
        self.activation_fn = activation.get_function()
        self.activation_derivative = activation.get_derivative()
        self.weights = None
        self.biases = None

    def build(self, input_dim):
        self.weights = self.activation.get_weights(input_dim, self.units)
        self.biases = np.zeros((1, self.units))

    def forward(self, X):
        self.input = X
        self.z = np.dot(X, self.weights) + self.biases
        self.output = self.activation_fn(self.z)
        return self.output

    def backward(self, grad_output):
        grad_z = grad_output * self.activation_derivative(self.output)
        grad_w = np.dot(self.input.T, grad_z)
        grad_b = np.sum(grad_z, axis=0, keepdims=True)
        grad_input = np.dot(grad_z, self.weights.T)
        return grad_input, grad_w, grad_b
    
