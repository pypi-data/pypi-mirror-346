# from sklearn.datasets import load_iris
try:
    from sklearn.datasets import load_iris
except ImportError:
    raise ImportError("scikit-learn is required. Please install it with `pip install scikit-learn`.")

from sklearn.model_selection import train_test_split

def get_sample_binary_iris(test_size=0.3):
    iris = load_iris()
    X = iris.data
    y = iris.target

    # Filter Setosa (0) vs Versicolor (1) only
    X = X[y != 2]
    y = y[y != 2]

    # Train-test split
    return train_test_split(X, y, test_size=test_size)
