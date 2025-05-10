import numpy as np
from scipy.stats import gmean, hmean

# These methods are implemented with NumPy and SciPy functions.

def _mean_wrapper(X):
    return np.mean(X, axis = 0)

def _hmean_wrapper(X):
    return hmean(X, axis = 0)

def _gmean_wrapper(X):
    return gmean(X, axis = 0)

def _min_wrapper(X):
    return np.min(X, axis = 0)