import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

def xor_neural_network_basic(X, y, epochs=10000, learning_rate=0.1, seed=42):
    """
    Trains a basic XOR neural network with 1 hidden layer.

    Parameters:
        X (ndarray): Input features of shape (n_samples, 2)
        y (ndarray): Target output of shape (n_samples, 1)
        epochs (int): Number of training iterations
        learning_rate (float): Learning rate for weight updates
        seed (int): Random seed for reproducibility

    Returns:
        output (ndarray): Final predictions after training
        (wh, bh, wo, bo): Tuple of trained weights and biases
    """
    np.random.seed(seed)

    # Define network structure
    input_layer_neurons = X.shape[1]
    hidden_layer_neurons = 2
    output_neurons = 1

    # Initialize weights and biases
    wh = np.random.uniform(size=(input_layer_neurons, hidden_layer_neurons))
    bh = np.random.uniform(size=(1, hidden_layer_neurons))
    wo = np.random.uniform(size=(hidden_layer_neurons, output_neurons))
    bo = np.random.uniform(size=(1, output_neurons))

    for epoch in range(epochs):
        # Forward propagation
        hidden_input = np.dot(X, wh) + bh
        hidden_output = sigmoid(hidden_input)

        output_input = np.dot(hidden_output, wo) + bo
        output = sigmoid(output_input)

        # Backpropagation
        error = y - output
        d_output = error * sigmoid_derivative(output)

        error_hidden = d_output.dot(wo.T)
        d_hidden = error_hidden * sigmoid_derivative(hidden_output)

        # Update weights and biases
        wo += hidden_output.T.dot(d_output) * learning_rate
        bo += np.sum(d_output, axis=0, keepdims=True) * learning_rate
        wh += X.T.dot(d_hidden) * learning_rate
        bh += np.sum(d_hidden, axis=0, keepdims=True) * learning_rate

        # Optional: Print loss
        if epoch % 1000 == 0:
            loss = np.mean(np.square(error))
            print(f"Epoch {epoch} — Loss: {loss:.4f}")

    # Return the final prediction and learned weights
    return np.round(output, 2), (wh, bh, wo, bo)