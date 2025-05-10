import numpy as np
from .utilities import _accuracy
from .losses import mean_squared_error
from .optimizers import adam, sgd

class fnn:
    """
    Feedforward Neural Network (FNN)

    A simple fully-connected neural network with customizable layers,
    activations, loss functions, optimizers, and training features.
    """
    
    def __init__(self, input_size:int):
        """
        Initialize the network with an input size.

        Args:
            input_size (int): Number of input features.
        """
        
        self.input_size = input_size
        self.layers = []
        self.activation = []
        np.random.seed(42)

    def add_layer(self, layer:dense):
        """
        Add a hidden or output layer to the model.

        Args:
            size (int): Number of neurons in the layer.
            activation (object): Activation function class instance.
        """
        
        self.layers.append(layer)

    def build(self):
        """
        Initialize weights, biases, and activation functions
        after all layers have been added.
        """
        
        input_dim = self.input_size
        for layer in self.layers:
            layer.build(input_dim)
            input_dim = layer.units
            
    def _forward(self, X:np.ndarray):
        """
        Perform a forward pass through the network.

        Args:
            X (np.ndarray): Input data.

        Returns:
            np.ndarray: Output of the final layer.
        """
        
        for layer in self.layers:
            X = layer.forward(X)
        return X
    
    def _backward(self, X:np.ndarray, Y:np.ndarray):
        """
        Perform backward pass and compute gradients.

        Args:
            X (np.ndarray): Input batch.
            Y (np.ndarray): True labels.
        """
        
        output = self._forward(X)
        if isinstance(self.layers[-1].activation, _softmax) and isinstance(self.loss, categorical_crossentropy):
            grad = output - Y
        else:
            grad = self.loss_derivative(Y, output) * self.layers[-1].activation_derivative(output)

        grads_w, grads_b = [], []

        for layer in reversed(self.layers):
            grad, dw, db = layer.backward(grad)
            grads_w.insert(0, dw)
            grads_b.insert(0, db)

        self._update_parameters(grads_w, grads_b)

    def _update_parameters(self, grads_w:list, grads_b:list):
        """
        Apply parameter updates using the optimizer.

        Args:
            gradients_w (list): Weight gradients.
            gradients_b (list): Bias gradients.
        """
        
        for i, layer in enumerate(self.layers):
            layer.weights = self.optimizer.update(layer.weights, grads_w[i], f"w{i}")
            layer.biases = self.optimizer.update(layer.biases, grads_b[i], f"b{i}")
            
    def train(
        self, X_train:np.ndarray, Y_train:np.ndarray,
        X_val=None, Y_val=None,
        loss=mean_squared_error, epochs=100, batch_size=64,
        learning_rate=0.001, optimizer=sgd, patience=float('inf'),
        verbose=True, plot=False,
        save_best=True, val_split=0.0):
        """
        Train the model on the given data.

        Args:
            X_train (np.ndarray): Training input.
            Y_train (np.ndarray): Training labels.
            X_val (np.ndarray): Validation input.
            Y_val (np.ndarray): Validation labels.
            loss (object): Loss function class.
            epochs (int): Maximum training epochs.
            batch_size (int): Size of training batches.
            learning_rate (float): Learning rate.
            optimizer (class): Optimizer class.
            patience (int): Early stopping patience.
            verbose (bool): Whether to print progress.
            plot (bool): Whether to plot training progress.
            save_best (bool): Save best model weights.
            val_split (float): % of train data to use as validation if val not provided.
        """
        
        if X_val is None and val_split > 0:
            split_index = int(len(X_train) * (1 - val_split))
            X_train, X_val = X_train[:split_index], X_train[split_index:]
            Y_train, Y_val = Y_train[:split_index], Y_train[split_index:]

        self.loss_history = []
        self.accuracy_history = []
        self.val_loss_history = []
        self.val_accuracy_history = []

        self.loss = loss
        self.loss_fn = self.loss.get_function()
        self.loss_derivative = self.loss.get_derivative()
        self.optimizer = optimizer(learning_rate=learning_rate)
        self.batch_size = batch_size
        num_samples = len(X_train)
        wait = 0

        best_val_loss = float('inf')
        self.best_weights = None

        if plot:
            import matplotlib.pyplot as plt
            plt.ion()
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
            fig.suptitle("Training Progress")
            ax1.set_ylabel("Loss")
            ax2.set_ylabel("Accuracy")
            ax2.set_xlabel("Epochs")
            loss_line, = ax1.plot([], [], 'r-', label="Train Loss")
            val_loss_line, = ax1.plot([], [], 'g--', label="Val Loss")
            acc_line, = ax2.plot([], [], 'b-', label="Train Acc")
            val_acc_line, = ax2.plot([], [], 'k--', label="Val Acc")
            ax1.legend(); ax2.legend()

            def update_plot():
                x_range = range(len(self.loss_history))
                loss_line.set_data(x_range, self.loss_history)
                val_loss_line.set_data(x_range, self.val_loss_history)
                acc_line.set_data(x_range, self.accuracy_history)
                val_acc_line.set_data(x_range, self.val_accuracy_history)
                ax1.relim(); ax1.autoscale_view()
                ax2.relim(); ax2.autoscale_view()
                plt.draw(); plt.pause(0.001)

        for epoch in range(epochs):
            indices = np.random.permutation(num_samples)
            X_shuffled = X_train[indices]
            Y_shuffled = Y_train[indices]

            epoch_losses = []
            epoch_accuracies = []

            for start in range(0, num_samples, batch_size):
                end = start + batch_size
                xb, yb = X_shuffled[start:end], Y_shuffled[start:end]

                y_pred = self._forward(xb)
                self._backward(xb, yb)

                loss = self.loss_fn(yb, y_pred)
                acc = _accuracy(yb, y_pred)

                epoch_losses.append(loss)
                epoch_accuracies.append(acc)

            train_loss = np.mean(epoch_losses)
            train_acc = np.mean(epoch_accuracies)
            self.loss_history.append(train_loss)
            self.accuracy_history.append(train_acc)

            if X_val is not None and Y_val is not None:
                val_pred = self._forward(X_val)
                val_loss = self.loss_fn(Y_val, val_pred)
                val_acc = _accuracy(Y_val, val_pred)
            else:
                val_loss = train_loss
                val_acc = train_acc

            self.val_loss_history.append(val_loss)
            self.val_accuracy_history.append(val_acc)

            if verbose and (epoch + 1) % 100 == 0:
                print(f"[Epoch {epoch+1}] "
                      f"Train Loss: {train_loss:.4f}, Acc: {train_acc:.4f} | "
                      f"Val Loss: {val_loss:.4f}, Acc: {val_acc:.4f}")

            if plot and (epoch + 1) % 10 == 0:
                update_plot()

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                wait = 0
                if save_best:
                    self.best_weights = self.get_weights()
            else:
                wait += 1
                if wait >= patience:
                    if verbose:
                        print(f"Early stopping at epoch {epoch+1}")
                    break

        if save_best and self.best_weights is not None:
            self.set_weights(self.best_weights)

        if plot:
            plt.ioff()
            plt.show()
            
    def get_weights(self):
        """
        Return a copy of current weights and biases.

        Returns:
            dict: Containing 'weights' and 'biases'.
        """
        
        return {
            'weights': [layer.weights.copy() for layer in self.layers],
            'biases': [layer.biases.copy() for layer in self.layers]
            }
    
    def set_weights(self, weights_dict):
        """
        Load a saved weight dictionary into the model.

        Args:
            weights_dict (dict): Dictionary of weights and biases.
        """
        
        for layer, w, b in zip(self.layers, weights_dict['weights'], weights_dict['biases']):
            layer.weights = w.copy()
            layer.biases = b.copy()
        
    def evaluate(self, X:np.ndarray, Y:np.ndarray):
        """
        Evaluate the model on given data.

        Args:
            X (np.ndarray): Input data.
            Y (np.ndarray): Ground truth labels.

        Returns:
            tuple: Loss and accuracy.
        """
        
        y_pred = self._forward(X)
        loss = self.loss_fn(Y, y_pred)
        acc = _accuracy(Y, y_pred)
        print(f"Eval Loss: {loss:.4f} - Accuracy: {acc:.4f}")
        return loss, acc

    def predict(self, X:np.ndarray, round_output=True):
        """
        Predict outputs for new input data.

        Args:
            X (np.ndarray): Input data.
            round_output (bool): Round predictions for classification.

        Returns:
            np.ndarray: Predictions.
        """
        
        pred = self._forward(X)
        return np.round(pred) if round_output else pred

    def summary(self):
        """
        Print a summary of the model's architecture.
        """
        
        print("Model Summary:")
        print(f" Input size: {self.input_size}")
        for i, layer in enumerate(self.layers):
            print(f" Layer {i+1}: {layer.weights.shape[0]} → {layer.weights.shape[1]}  | Activation: {layer.activation.__class__.__name__}")
        print(f" Output size: {self.layers[-1].weights.shape[1]}")
