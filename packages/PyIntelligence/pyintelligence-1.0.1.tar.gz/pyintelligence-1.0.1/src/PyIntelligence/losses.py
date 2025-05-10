import numpy as np

class binary_crossentropy:
    def _function(self, y_true, y_pred):
        y_pred = np.clip(y_pred, 1e-15, 1 - 1e-15)
        return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
    def _derivative(self, y_true, y_pred):
        y_pred = np.clip(y_pred, 1e-15, 1 - 1e-15)
        return (y_pred - y_true) / (y_pred * (1 - y_pred) * y_true.shape[0])
    def get_function(self):
        return self._function
    def get_derivative(self):
        return self._derivative

class categorical_crossentropy:
    def get_function(self):
        return lambda y_true, y_pred: -np.mean(np.sum(y_true * np.log(y_pred + 1e-8), axis=1))
    def get_derivative(self):
        return lambda y_true, y_pred: y_pred - y_true

class mean_squared_error:
    def get_function(self):
        return lambda y_true, y_pred: np.mean((y_true - y_pred)**2)
    def get_derivative(self):
        return lambda y_true, y_pred: 2 * (y_pred - y_true) / y_true.size

binary_crossentropy = binary_crossentropy()
categorical_crossentropy = categorical_crossentropy()
mean_squared_error = mean_squared_error()
