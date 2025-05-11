import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def train_logistic_model(X_train, X_test, y_train, y_test, epochs=1000, learning_rate=0.1, show_logs=True):
    weights = np.zeros(X_train.shape[1])
    bias = 0

    for epoch in range(epochs):
        linear_output = np.dot(X_train, weights) + bias
        predictions = sigmoid(linear_output)

        loss = -np.mean(y_train * np.log(predictions + 1e-8) + (1 - y_train) * np.log(1 - predictions + 1e-8))

        dw = np.dot(X_train.T, (predictions - y_train)) / len(X_train)
        db = np.mean(predictions - y_train)

        weights -= learning_rate * dw
        bias -= learning_rate * db

        if show_logs and epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {loss:.4f}")

    test_preds = sigmoid(np.dot(X_test, weights) + bias)
    test_preds = (test_preds >= 0.5).astype(int)

    accuracy = np.mean(test_preds == y_test)
    print(f"\nTest Accuracy: {accuracy:.2f}")

    return {
        "weights": weights,
        "bias": bias,
        "accuracy": accuracy
    }
