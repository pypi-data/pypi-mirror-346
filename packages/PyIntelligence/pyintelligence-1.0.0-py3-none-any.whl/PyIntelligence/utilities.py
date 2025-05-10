import numpy as np
def _accuracy(y_true, y_pred):
    if y_true.shape[1] == 1: 
        return np.mean(np.round(y_pred) == y_true)
    else:  
        return np.mean(np.argmax(y_pred, axis=1) == np.argmax(y_true, axis=1))
