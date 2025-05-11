import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def advanced_linear_regression(X, y, plot=True):
    """
    Performs simple linear regression using scipy.stats.linregress
    and optionally plots the result.

    Args:
        X (list or np.array): Independent variable values
        y (list or np.array): Dependent variable values
        plot (bool): Whether to display a regression plot (default: True)

    Returns:
        dict: A dictionary containing slope, intercept, r_value, p_value, std_err, and y_pred
    """
    X = np.array(X)
    y = np.array(y)

    slope, intercept, r_value, p_value, std_err = stats.linregress(X, y)
    y_pred = slope * X + intercept

    if plot:
        plt.scatter(X, y, color='blue', label='Original Data')
        plt.plot(X, y_pred, color='red', label='Fitted Line')
        plt.xlabel('Hours of Study')
        plt.ylabel('Exam Scores')
        plt.title('Linear Regression: Hours of Study vs Exam Scores')
        plt.legend()
        plt.show()

    return {
        "slope": slope,
        "intercept": intercept,
        "equation": f"y = {slope:.2f}x + {intercept:.2f}",
        "r_squared": r_value**2,
        "r_value": r_value,
        "p_value": p_value,
        "std_error": std_err,
        "y_pred": y_pred
    }