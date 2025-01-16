"""
Implementation of fixed-point iteration methods for finding roots.
Includes convergence analysis and error estimation.
"""

import numpy as np
import matplotlib.pyplot as plt
from basics.rechnerarithmetik import is_close
from basics.plot_functions import plot_function_1d, plot_convergence

def fixed_point_iteration(g, x0, tol=1e-10, max_iter=100, store_history=False):
    """
    Perform fixed-point iteration x_{n+1} = g(x_n).
    
    Args:
        g: Fixed-point function
        x0: Initial guess
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
        store_history: Whether to store iteration history
        
    Returns:
        Tuple of (final approximation, iterations performed, history if requested)
    """
    x_prev = x0
    history = [x0] if store_history else None
    
    for i in range(max_iter):
        x_next = g(x_prev)
        
        if store_history:
            history.append(x_next)
            
        if abs(x_next - x_prev) < tol:
            return x_next, i + 1, history
            
        x_prev = x_next
        
    return x_next, max_iter, history

def estimate_lipschitz_constant(g, x, h=1e-5):
    """
    Estimate Lipschitz constant using numerical differentiation.
    
    Args:
        g: Function to analyze
        x: Point at which to estimate
        h: Step size for differentiation
        
    Returns:
        Estimated Lipschitz constant (absolute value of derivative)
    """
    return abs((g(x + h) - g(x)) / h)

def verify_banach_conditions(g, a, b, num_points=1000):
    """
    Verify Banach fixed-point theorem conditions on interval [a,b].
    
    Args:
        g: Function to analyze
        a, b: Interval endpoints
        num_points: Number of points for checking
        
    Returns:
        Tuple of (conditions satisfied, maximum Lipschitz constant)
    """
    x_test = np.linspace(a, b, num_points)
    y_test = [g(x) for x in x_test]
    maps_to_itself = all(a <= y <= b for y in y_test)
    
    lipschitz_constants = [estimate_lipschitz_constant(g, x) for x in x_test]
    max_lipschitz = max(lipschitz_constants)
    
    conditions_satisfied = maps_to_itself and max_lipschitz < 1
    
    return conditions_satisfied, max_lipschitz

def fixed_point_iteration_with_error(g, x0, alpha, tol=1e-10, max_iter=100):
    """
    Fixed-point iteration with a priori and a posteriori error estimates.
    
    Args:
        g: Fixed-point function
        x0: Initial guess
        alpha: Lipschitz constant
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
        
    Returns:
        Tuple of (final approximation, a priori errors, a posteriori errors)
    """
    x_prev = x0
    x_curr = g(x0)
    
    a_priori_errors = []
    a_posteriori_errors = []
    
    first_step_size = abs(x_curr - x_prev)
    
    for i in range(max_iter):
        # Calculate error estimates
        a_priori = (alpha ** (i+1) / (1 - alpha)) * first_step_size
        a_posteriori = (alpha / (1 - alpha)) * abs(x_curr - x_prev)
        
        a_priori_errors.append(a_priori)
        a_posteriori_errors.append(a_posteriori)
        
        if abs(x_curr - x_prev) < tol:
            break
            
        x_prev = x_curr
        x_curr = g(x_curr)
    
    return x_curr, a_priori_errors, a_posteriori_errors

def analyze_convergence(g, x0, x_star, iterations=20):
    """
    Analyze convergence order of fixed-point iteration.
    
    Args:
        g: Fixed-point function
        x0: Initial guess
        x_star: Known fixed point
        iterations: Number of iterations to analyze
        
    Returns:
        Estimated convergence order
    """
    x_prev = x0
    errors = []
    
    for _ in range(iterations):
        x_curr = g(x_prev)
        errors.append(abs(x_curr - x_star))
        x_prev = x_curr
        
    # Estimate convergence order using consecutive errors
    if len(errors) > 2:
        ratios = []
        for i in range(len(errors)-2):
            if errors[i+1] > 0 and errors[i] > 0:  # Avoid division by zero
                ratio = np.log(errors[i+2]/errors[i+1]) / np.log(errors[i+1]/errors[i])
                ratios.append(ratio)
        
        return np.mean(ratios) if ratios else 0.0
    
    return 0.0

def plot_iteration_process(g, x0, a, b, num_iterations=5):
    """
    Visualize the fixed-point iteration process.
    
    Args:
        g: Fixed-point function
        x0: Initial guess
        a, b: Plot range
        num_iterations: Number of iterations to show
    """
    x = np.linspace(a, b, 1000)
    y_g = [g(xi) for xi in x]
    
    plt.figure(figsize=(10, 10))
    plt.plot(x, y_g, 'b-', label='g(x)')
    plt.plot(x, x, 'k--', label='y=x')
    
    x_curr = x0
    plt.plot([x_curr], [x_curr], 'go', label='Start')
    
    for i in range(num_iterations):
        y_curr = g(x_curr)
        # Plot vertical line to g(x)
        plt.plot([x_curr, x_curr], [x_curr, y_curr], 'r:', alpha=0.5)
        # Plot horizontal line to y=x
        plt.plot([x_curr, y_curr], [y_curr, y_curr], 'r:', alpha=0.5)
        x_curr = y_curr
        plt.plot([x_curr], [x_curr], 'ro')
    
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Fixed-Point Iteration Process')
    plt.legend()
    plt.axis('equal')
    plt.show()

def plot_error_analysis(a_priori_errors, a_posteriori_errors):
    """
    Plot error estimates comparison.
    
    Args:
        a_priori_errors: List of a priori error estimates
        a_posteriori_errors: List of a posteriori error estimates
    """
    plt.figure(figsize=(10, 6))
    plt.semilogy(a_priori_errors, 'b.-', label='A priori')
    plt.semilogy(a_posteriori_errors, 'r.-', label='A posteriori')
    plt.grid(True)
    plt.xlabel('Iteration')
    plt.ylabel('Error estimate')
    plt.title('Error Estimates vs Iteration')
    plt.legend()
    plt.show()

# Example usage
if __name__ == "__main__":
    # Example 1: Simple fixed point iteration
    def g1(x):
        return np.cos(x)  # Fixed point is approximately 0.739
    
    x0 = 0
    x_star, iters, history = fixed_point_iteration(g1, x0, store_history=True)
    print(f"Example 1 - cos(x):")
    print(f"Fixed point: {x_star:.6f}")
    print(f"Iterations needed: {iters}")
    
    plot_iteration_process(g1, x0, 0, 1)
    
    # Example 2: Analysis with Banach conditions
    def g2(x):
        return (x**2 + 1)/3  # Fixed point is approximately 1
        
    conditions_met, lipschitz = verify_banach_conditions(g2, 0.5, 1.5)
    print(f"\nExample 2 - (x^2 + 1)/3:")
    print(f"Banach conditions met: {conditions_met}")
    print(f"Maximum Lipschitz constant: {lipschitz:.6f}")
    
    # Example 3: Error analysis
    if lipschitz < 1:
        x_final, a_priori, a_posteriori = fixed_point_iteration_with_error(
            g2, 1.0, lipschitz
        )
        print(f"Fixed point: {x_final:.6f}")
        plot_error_analysis(a_priori, a_posteriori)
