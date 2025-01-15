"""
Error estimation for root finding methods.
"""

from typing import Callable, Tuple, Optional
import numpy as np
from libraries import get_machine_epsilon

def verify_bracket(f: Callable[[float], float], 
                  x: float, 
                  epsilon: float) -> bool:
    """
    Verify if a root is bracketed within epsilon of x.
    
    Args:
        f: Function to analyze
        x: Current approximation
        epsilon: Error bound to check
        
    Returns:
        bool: Whether root is verified to be in interval
    """
    f_left = f(x - epsilon)
    f_right = f(x + epsilon)
    
    return f_left * f_right < 0

def estimate_error_bound(f: Callable[[float], float],
                        df: Optional[Callable[[float], float]],
                        x: float,
                        method: str = 'newton') -> float:
    """
    Estimate error bound for root approximation.
    
    Args:
        f: Function to analyze
        df: Derivative function (optional)
        x: Current approximation
        method: Method used ('newton', 'secant', etc.)
        
    Returns:
        float: Estimated error bound
    """
    eps = get_machine_epsilon()
    h = max(abs(x) * eps**(1/3), eps**(1/3))
    
    # Estimate derivative if not provided
    if df is None:
        df_x = (f(x + h) - f(x)) / h
    else:
        df_x = df(x)
        
    # Avoid division by zero
    if abs(df_x) < eps:
        raise ValueError("Derivative too close to zero")
        
    if method == 'newton':
        # For Newton's method, error is approximately f(x)/f'(x)
        return abs(f(x) / df_x)
    elif method == 'secant':
        # For secant method, error bound is less precise
        return abs(f(x) / df_x) * 1.5
    else:
        raise ValueError(f"Unknown method: {method}")

def compute_residual(f: Callable[[float], float],
                    x: float) -> float:
    """
    Compute residual |f(x)| at current approximation.
    
    Args:
        f: Function to analyze
        x: Current approximation
        
    Returns:
        float: Absolute value of residual
    """
    return abs(f(x))

def verify_convergence_conditions(f: Callable[[float], float],
                                df: Callable[[float], float],
                                x: float,
                                interval: Tuple[float, float],
                                method: str = 'newton') -> Tuple[bool, str]:
    """
    Verify conditions for method convergence.
    
    Args:
        f: Function to analyze
        df: Derivative function
        x: Current point
        interval: Interval to check
        method: Method to check conditions for
        
    Returns:
        Tuple containing:
        - Whether conditions are satisfied
        - Description of any violations
    """
    a, b = interval
    h = (b - a) / 1000
    x_test = np.arange(a, b, h)
    
    try:
        # Check if derivative exists and is continuous
        df_values = [df(xi) for xi in x_test]
        if any(np.isnan(df_values)):
            return False, "Derivative not defined in interval"
            
        if method == 'newton':
            # Check if derivative is zero anywhere
            if any(abs(dfx) < get_machine_epsilon() for dfx in df_values):
                return False, "Derivative too close to zero"
                
            # Estimate second derivative
            d2f_values = np.diff(df_values) / h
            
            # Check if f*f''/f'^2 < 1 (sufficient condition for Newton)
            max_ratio = max(abs(f(xi) * d2f_val / df_values[i]**2) 
                          for i, (xi, d2f_val) in enumerate(zip(x_test[:-1], d2f_values)))
            
            if max_ratio >= 1:
                return False, "Newton convergence condition f*f''/f'^2 < 1 not satisfied"
                
        elif method == 'secant':
            # Check if derivative changes sign (could cause issues for secant)
            if any(df1 * df2 < 0 for df1, df2 in zip(df_values[:-1], df_values[1:])):
                return False, "Derivative changes sign (secant method may have issues)"
                
    except Exception as e:
        return False, f"Error checking conditions: {str(e)}"
        
    return True, "All conditions satisfied"

def estimate_working_precision(f: Callable[[float], float],
                             x: float) -> float:
    """
    Estimate working precision at current approximation.
    
    Args:
        f: Function to analyze
        x: Current approximation
        
    Returns:
        float: Estimated working precision
    """
    eps = get_machine_epsilon()
    h = max(abs(x) * eps**(1/3), eps**(1/3))
    
    # Compute function at nearby points
    f_x = f(x)
    f_xph = f(x + h)
    f_xmh = f(x - h)
    
    # Estimate local roundoff error
    roundoff = eps * abs(f_x) / h
    
    # Estimate truncation error using central difference
    trunc = abs(f_xph - 2*f_x + f_xmh) / (h * h)
    
    return max(roundoff, trunc)

# Example usage
if __name__ == "__main__":
    # Example function and its derivative
    def f(x: float) -> float:
        return x**3 - 2*x - 5
        
    def df(x: float) -> float:
        return 3*x**2 - 2
        
    # Test point near a root
    x_test = 2.0946
    
    # Verify if we're near a root
    eps = 1e-6
    is_bracketed = verify_bracket(f, x_test, eps)
    print(f"Root bracketed within {eps} of x = {x_test}: {is_bracketed}")
    
    # Estimate error bounds
    try:
        newton_error = estimate_error_bound(f, df, x_test, 'newton')
        print(f"Estimated Newton error bound: {newton_error:.2e}")
        
        secant_error = estimate_error_bound(f, df, x_test, 'secant')
        print(f"Estimated Secant error bound: {secant_error:.2e}")
    except ValueError as e:
        print(f"Error estimation failed: {e}")
    
    # Compute residual
    res = compute_residual(f, x_test)
    print(f"Residual |f(x)|: {res:.2e}")
    
    # Check convergence conditions
    interval = (1.5, 2.5)
    newton_ok, newton_msg = verify_convergence_conditions(f, df, x_test, interval, 'newton')
    print(f"\nNewton convergence check: {newton_msg}")
    
    secant_ok, secant_msg = verify_convergence_conditions(f, df, x_test, interval, 'secant')
    print(f"Secant convergence check: {secant_msg}")
    
    # Estimate working precision
    prec = estimate_working_precision(f, x_test)
    print(f"\nEstimated working precision: {prec:.2e}")
    
    # Visual demonstration of error bounds
    import matplotlib.pyplot as plt
    
    def plot_error_bounds(f: Callable[[float], float],
                         x_approx: float,
                         error_bound: float,
                         title: str = "Error Bound Visualization"):
        """Plot function with error bounds around approximate root."""
        x = np.linspace(x_approx - 2*error_bound, x_approx + 2*error_bound, 1000)
        y = [f(xi) for xi in x]
        
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, 'b-', label='f(x)')
        plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        plt.axvline(x=x_approx, color='r', linestyle='--', label='Approximation')
        plt.axvspan(x_approx - error_bound, x_approx + error_bound, 
                   color='g', alpha=0.2, label='Error bound')
        
        plt.grid(True)
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title(title)
        plt.legend()
        plt.show()
    
    # Plot error bounds for Newton method
    plot_error_bounds(f, x_test, newton_error, "Newton Method Error Bound")
    
    # Example of tracking error estimates during iteration
    def track_error_convergence(f: Callable[[float], float],
                              df: Callable[[float], float],
                              x0: float,
                              tol: float = 1e-10,
                              max_iter: int = 100) -> None:
        """Track various error estimates during Newton iteration."""
        x = x0
        residuals = []
        error_bounds = []
        working_precision = []
        
        for i in range(max_iter):
            # Store error measures
            residuals.append(compute_residual(f, x))
            error_bounds.append(estimate_error_bound(f, df, x, 'newton'))
            working_precision.append(estimate_working_precision(f, x))
            
            # Newton step
            dx = -f(x)/df(x)
            x += dx
            
            if abs(dx) < tol:
                break
        
        # Plot convergence of different error measures
        plt.figure(figsize=(10, 6))
        plt.semilogy(residuals, 'b.-', label='Residual')
        plt.semilogy(error_bounds, 'r.-', label='Error bound')
        plt.semilogy(working_precision, 'g.-', label='Working precision')
        plt.grid(True)
        plt.xlabel('Iteration')
        plt.ylabel('Error measure (log scale)')
        plt.title('Convergence of Error Measures')
        plt.legend()
        plt.show()
    
    # Demonstrate error tracking
    track_error_convergence(f, df, 1.5)