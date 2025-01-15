import numpy as np
import math
import sympy as sp
from typing import Union, List, Tuple, Callable
import matplotlib.pyplot as plt

# Type aliases
Number = Union[int, float]
Vector = List[Number]
Matrix = List[List[Number]]

def is_close(a: float, b: float, rel_tol: float = 1e-9, abs_tol: float = 0.0) -> bool:
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

def get_machine_epsilon() -> float:
    """
    Calculate machine epsilon - smallest number ε where 1 + ε ≠ 1
    
    Returns:
        float: Machine epsilon for current system
    """
    eps = 1.0
    while 1.0 + eps/2.0 > 1.0:
        eps = eps/2.0
    return eps

def relative_error(true_val: Number, approx_val: Number) -> float:
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

def absolute_error(true_val: Number, approx_val: Number) -> float:
    """
    Calculate absolute error between true and approximate value.
    
    Args:
        true_val: True value
        approx_val: Approximate value
    
    Returns:
        float: Absolute error
    """
    return abs(true_val - approx_val)

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