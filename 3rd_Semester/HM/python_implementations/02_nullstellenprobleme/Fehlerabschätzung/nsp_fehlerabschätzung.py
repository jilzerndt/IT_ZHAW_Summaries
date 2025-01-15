import numpy as np

def error_estimate(f, x, eps=1e-5):
    fx_left = f(x - eps)
    fx_right = f(x + eps)
    
    if np.sign(fx_left) != np.sign(fx_right):
        return eps  # Nullstelle liegt in (x-eps, x+eps)
    return None