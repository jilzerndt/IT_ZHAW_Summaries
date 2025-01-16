"""
Error estimation for root finding methods.
Provides tools for verifying and estimating errors in numerical root finding.
"""

import numpy as np
import matplotlib.pyplot as plt
from libraries import get_machine_epsilon

def verify_bracket(f, x, epsilon):
    """
    Verify if a root is bracketed within epsilon of x by checking for sign change.
    Uses Bolzano's theorem: if f(a)f(b) < 0, then f has a root in [a,b].
    
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

def estimate_error_bound(f, df, x, method='newton'):
    """
    Estimate error bound for root approximation using different methods.
    For Newton's method: |x - α| ≈ |f(x)/f'(x)|
    For Secant method: adds safety factor due to approximated derivative
    
    Args:
        f: Function to analyze
        df: Derivative function (optional)
        x: Current approximation
        method: Method used ('newton', 'secant', etc.)
        
    Returns:
        Estimated error bound
    """
    eps = get_machine_epsilon()
    # Choose step size for numerical differentiation using h ≈ eps^(1/3)
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
        # Classical Newton error estimate
        return abs(f(x) / df_x)
    elif method == 'secant':
        # Add safety factor for secant method
        return abs(f(x) / df_x) * 1.5
    else:
        raise ValueError(f"Unknown method: {method}")

def compute_residual(f, x):
    """
    Compute residual |f(x)| at current approximation.
    This measures how well x satisfies f(x) = 0.
    
    Args:
        f: Function to analyze
        x: Current approximation
        
    Returns:
        Absolute value of residual
    """
    return abs(f(x))

def verify_convergence_conditions(f, df, x, interval, method='newton'):
    """
    Verify conditions for method convergence in an interval.
    For Newton: checks if f*f''/f'^2 < 1 (sufficient for quadratic convergence)
    For Secant: checks if f' maintains sign (for reliable convergence)
    
    Args:
        f: Function to analyze
        df: Derivative function
        x: Current point
        interval: Interval to check
        method: Method to check conditions for
        
    Returns:
        Tuple of (conditions satisfied, description message)
    """
    a, b = interval
    h = (b - a) / 1000
    x_test = np.arange(a, b, h)
    
    try:
        # Check derivative existence and continuity
        df_values = [df(xi) for xi in x_test]
        if any(np.isnan(df_values)):
            return False, "Derivative not defined in interval"
            
        if method == 'newton':
            # Check for zero derivative
            if any(abs(dfx) < get_machine_epsilon() for dfx in df_values):
                return False, "Derivative too close to zero"
                
            # Estimate second derivative using finite differences
            d2f_values = np.diff(df_values) / h
            
            # Check Newton convergence condition
            max_ratio = max(abs(f(xi) * d2f_val / df_values[i]**2) 
                          for i, (xi, d2f_val) in enumerate(zip(x_test[:-1], d2f_values)))
            
            if max_ratio >= 1:
                return False, "Newton convergence condition f*f''/f'^2 < 1 not satisfied"
                
        elif method == 'secant':
            # Check for derivative sign changes
            if any(df1 * df2 < 0 for df1, df2 in zip(df_values[:-1], df_values[1:])):
                return False, "Derivative changes sign (secant method may have issues)"
                
    except Exception as e:
        return False, f"Error checking conditions: {str(e)}"
        
    return True, "All conditions satisfied"

def estimate_working_precision(f, x):
    """
    Estimate working precision at current approximation.
    Considers both roundoff error and truncation error in the computation.
    
    Args:
        f: Function to analyze
        x: Current approximation
        
    Returns:
        Estimated working precision
    """
    eps = get_machine_epsilon()
    h = max(abs(x) * eps**(1/3), eps**(1/3))
    
    # Evaluate function at three points for error estimation
    f_x = f(x)
    f_xph = f(x + h)
    f_xmh = f(x - h)
    
    # Estimate local roundoff error using machine epsilon
    roundoff = eps * abs(f_x) / h
    
    # Estimate truncation error using second derivative approximation
    trunc = abs(f_xph - 2*f_x + f_xmh) / (h * h)
    
    return max(roundoff, trunc)

def plot_error_bounds(f, x_approx, error_bound, title="Error Bound Visualization"):
    """
    Plot function with error bounds around approximate root.
    Shows the interval where the true root is expected to lie.
    
    Args:
        f: Function to plot
        x_approx: Approximate root
        error_bound: Estimated error bound
        title: Plot title
    """
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

def track_error_convergence(f, df, x0, tol=1e-10, max_iter=100):
    """
    Track various error estimates during Newton iteration.
    Shows how different error measures evolve during the iteration process.
    
    Args:
        f: Function to analyze
        df: Derivative function
        x0: Initial guess
        tol: Convergence tolerance
        max_iter: Maximum iterations
    """
    x = x0
    residuals = []
    error_bounds = []
    working_precision = []
    
    for i in range(max_iter):
        # Collect error measures
        residuals.append(compute_residual(f, x))
        error_bounds.append(estimate_error_bound(f, df, x, 'newton'))
        working_precision.append(estimate_working_precision(f, x))
        
        # Newton step
        dx = -f(x)/df(x)
        x += dx
        
        if abs(dx) < tol:
            break
    
    # Plot convergence of all error measures
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

# Example usage
if __name__ == "__main__":
    # Example function: x³ - 2x - 5
    def f(x):
        return x**3 - 2*x - 5
        
    def df(x):
        return 3*x**2 - 2
        
    # Test point near the root ≈ 2.0946
    x_test = 2.0946
    
    # Verify root bracketing
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
    
    # Compute and display residual
    res = compute_residual(f, x_test)
    print(f"Residual |f(x)|: {res:.2e}")
    
    # Check convergence conditions
    interval = (1.5, 2.5)
    newton_ok, newton_msg = verify_convergence_conditions(f, df, x_test, interval, 'newton')
    print(f"\nNewton convergence check: {newton_msg}")
    
    secant_ok, secant_msg = verify_convergence_conditions(f, df, x_test, interval, 'secant')
    print(f"Secant convergence check: {secant_msg}")
    
    # Show error bounds visually
    plot_error_bounds(f, x_test, newton_error, "Newton Method Error Bound")
    
    # Demonstrate error tracking during iteration
    track_error_convergence(f, df, 1.5)
