import numpy as np

def simple_linear_regression(X, y):
    n = len(X)
    sum_x = sum(X)
    sum_y = sum(y)
    sum_xy = sum(X[i] * y[i] for i in range(n))
    sum_x_squared = sum(X[i]**2 for i in range(n))

    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x**2)
    b = (sum_y - m * sum_x) / n

    x_array = np.array(X)
    y_pred = m * x_array + b

    return {
        "slope": m,
        "intercept": b,
        "equation": f"y = {m:.2f}x + {b:.2f}",
        "x": x_array,
        "y_pred": y_pred
    }
