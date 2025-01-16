"""
Functions for analyzing and working with computer arithmetic.
"""

import numpy as np
import math
import sympy as sp
import matplotlib.pyplot as plt

def is_close(a, b, rel_tol=1e-9, abs_tol=0.0):
    """
    Check if two floating point numbers are approximately equal.
    Uses both relative and absolute tolerance for comparison.
    
    Args:
        a, b: Numbers to compare
        rel_tol: Relative tolerance
        abs_tol: Absolute tolerance
    
    Returns:
        bool: True if numbers are approximately equal
    """
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def get_machine_epsilon():
    """
    Calculate machine epsilon - smallest number ε where 1 + ε ≠ 1
    
    Returns:
        float: Machine epsilon for current system
    """
    eps = 1.0
    while 1.0 + eps/2.0 > 1.0:
        eps = eps/2.0
    return eps

def relative_error(true_val, approx_val):
    """
    Calculate relative error between true and approximate value.
    
    Args:
        true_val: True value
        approx_val: Approximate value
    
    Returns:
        float: Relative error
    """
    if true_val == 0:
        raise ValueError("True value cannot be zero when calculating relative error")
    return abs((true_val - approx_val) / true_val)

def absolute_error(true_val, approx_val):
    """
    Calculate absolute error between true and approximate value.
    
    Args:
        true_val: True value
        approx_val: Approximate value
    
    Returns:
        float: Absolute error
    """
    return abs(true_val - approx_val)

def analyze_float_representation(x):
    """
    Analyze the floating point representation of a number.
    
    Args:
        x: Number to analyze
    
    Returns:
        dict: Information about the floating point representation
    """
    # Get binary representation
    bits = np.binary_repr(np.float64(x).view(np.int64), width=64)
    
    # Extract components
    sign = int(bits[0])
    exponent = int(bits[1:12], 2) - 1023  # Remove bias
    fraction = bits[12:]
    
    # Calculate normalized value
    real_value = (-1)**sign * 2**exponent * (1 + sum([int(b) * 2**(-i-1) 
                                                      for i, b in enumerate(fraction)]))
    
    return {
        'sign': sign,
        'exponent': exponent,
        'fraction': fraction,
        'binary': bits,
        'real_value': real_value
    }

def plot_rounding_errors(f, x_range, points=1000):
    """
    Plot function values and their rounding errors.
    
    Args:
        f: Function to analyze
        x_range: Tuple of (min_x, max_x)
        points: Number of points to evaluate
    """
    x = np.linspace(x_range[0], x_range[1], points)
    y_exact = [f(xi) for xi in x]
    y_float = [float(f(float(xi))) for xi in x]
    errors = [abs(ye - yf) for ye, yf in zip(y_exact, y_float)]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Plot function
    ax1.plot(x, y_exact, 'b-', label='Exact')
    ax1.plot(x, y_float, 'r--', label='Float')
    ax1.set_title('Function Values')
    ax1.legend()
    ax1.grid(True)
    
    # Plot errors
    ax2.semilogy(x, errors, 'g-', label='Rounding Error')
    ax2.set_title('Rounding Errors')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    # Demonstrate machine epsilon
    eps = get_machine_epsilon()
    print(f"Machine epsilon: {eps}")
    
    # Demonstrate error calculations
    true_val = math.pi
    approx_val = 22/7
    print(f"\nApproximating π:")
    print(f"Absolute error: {absolute_error(true_val, approx_val)}")
    print(f"Relative error: {relative_error(true_val, approx_val)}")
    
    # Analyze floating point representation
    x = 0.1
    analysis = analyze_float_representation(x)
    print(f"\nAnalysis of {x}:")
    for key, value in analysis.items():
        print(f"{key}: {value}")
    
    # Plot rounding errors for a function
    def f(x):
        return x**2 - 2*x + 1
    
    plot_rounding_errors(f, (-1, 2))
