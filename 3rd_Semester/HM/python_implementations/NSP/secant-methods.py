"""
Implementation of the secant method and its variants for finding roots.
Includes standard secant method, regula falsi, and modified secant method.
"""

import numpy as np
import matplotlib.pyplot as plt
from basics.plot_functions import plot_function_1d, plot_convergence

def secant_method(f, x0, x1, tol=1e-10, max_iter=100, store_history=False):
    """
    Standard secant method for finding roots: x_{n+1} = x_n - f(x_n)(x_n - x_{n-1})/(f(x_n) - f(x_{n-1}))
    Uses linear interpolation between two points to approximate derivative.
    
    Args:
        f: Function to find root of
        x0, x1: Initial guesses
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
        store_history: Whether to store iteration history
    
    Returns:
        Tuple of (final approximation, iterations performed, history if requested)
    """
    # Check initial points aren't too close together
    if abs(f(x1) - f(x0)) < tol:
        raise ValueError("Initial points too close together")
        
    history = [x0, x1] if store_history else None
    
    for i in range(max_iter):
        f_x0, f_x1 = f(x0), f(x1)
        
        # Secant step using linear interpolation
        x_new = x1 - f_x1 * (x1 - x0)/(f_x1 - f_x0)
        
        if store_history:
            history.append(x_new)
            
        # Check for convergence
        if abs(x_new - x1) < tol:
            return x_new, i + 1, history
            
        # Update points for next iteration
        x0, x1 = x1, x_new
        
    return x1, max_iter, history

def regula_falsi(f, a, b, tol=1e-10, max_iter=100):
    """
    Regula falsi (false position) method.
    Similar to secant method but maintains bracketing interval.
    Converges more slowly but more reliably than secant method.
    
    Args:
        f: Function to find root of
        a, b: Initial bracket endpoints with f(a)*f(b) < 0
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
    
    Returns:
        Tuple of (final approximation, iterations performed)
    """
    # Evaluate function at endpoints
    f_a, f_b = f(a), f(b)
    
    # Verify bracketing interval
    if f_a * f_b >= 0:
        raise ValueError("Initial points must bracket the root")
        
    for i in range(max_iter):
        # False position step - weighted average based on function values
        c = (a * f_b - b * f_a)/(f_b - f_a)
        f_c = f(c)
        
        # Check for convergence using residual
        if abs(f_c) < tol:
            return c, i + 1
            
        # Update bracket while maintaining opposite signs
        if f_c * f_a < 0:
            b, f_b = c, f_c  # Root in left half
        else:
            a, f_a = c, f_c  # Root in right half
            
    return c, max_iter

def modified_secant(f, x0, h=1e-4, tol=1e-10, max_iter=100):
    """
    Modified secant method using finite difference approximation.
    Approximates derivative using single point and small perturbation.
    
    Args:
        f: Function to find root of
        x0: Initial guess
        h: Finite difference step size
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
    
    Returns:
        Tuple of (final approximation, iterations performed)
    """
    x = x0
    
    for i in range(max_iter):
        # Evaluate function at current point and perturbed point
        f_x = f(x)
        f_xh = f(x + h)
        
        # Check if function difference is too small
        if abs(f_xh - f_x) < tol:
            raise ValueError("Function values too close")
            
        # Modified secant step using finite difference
        x_new = x - f_x * h/(f_xh - f_x)
        
        if abs(x_new - x) < tol:
            return x_new, i + 1
            
        x = x_new
        
    return x, max_iter

def visualize_secant_steps(f, x0, x1, x_range, num_steps=5):
    """
    Visualize secant method iterations graphically.
    Shows function, secant lines, and convergence path.
    
    Args:
        f: Function to find root of
        x0, x1: Initial points
        x_range: Plot range (xmin, xmax)
        num_steps: Number of steps to visualize
    """
    x = np.linspace(x_range[0], x_range[1], 1000)
    y = [f(xi) for xi in x]
    
    plt.figure(figsize=(12, 8))
    plt.plot(x, y, 'b-', label='f(x)')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    
    # Plot initial points
    x_prev, x_curr = x0, x1
    plt.plot([x_prev, x_curr], [f(x_prev), f(x_curr)], 'go', label='Initial points')
    
    # Show iterations
    for i in range(num_steps):
        f_prev, f_curr = f(x_prev), f(x_curr)
        
        # Calculate next iteration point
        x_new = x_curr - f_curr * (x_curr - x_prev)/(f_curr - f_prev)
        f_new = f(x_new)
        
        # Plot secant line and new point
        plt.plot([x_prev, x_curr], [f_prev, f_curr], 'r--', alpha=0.5)
        plt.plot(x_new, f_new, 'ro')
        
        x_prev, x_curr = x_curr, x_new
        
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Secant Method Iterations')
    plt.legend()
    plt.show()

def analyze_convergence(x_hist, x_star):
    """
    Analyze convergence rate of secant method.
    Theoretical order is golden ratio φ = (1 + √5)/2 ≈ 1.618.
    Uses ratios of consecutive errors to estimate convergence order.
    
    Args:
        x_hist: List of iterations
        x_star: Known root
    
    Returns:
        Estimated convergence order
    """
    errors = [abs(x - x_star) for x in x_hist]
    orders = []
    
    for i in range(len(errors)-2):
        if errors[i+1] > 0 and errors[i] > 0:
            # Estimate order using consecutive error ratios
            order = np.log(errors[i+2]/errors[i+1]) / np.log(errors[i+1]/errors[i])
            if not np.isnan(order) and not np.isinf(order):
                orders.append(order)
                
    return np.mean(orders) if orders else 0.0

def plot_convergence_comparison(f, x0, x1, max_iter=20):
    """
    Compare convergence of different secant variants.
    Shows error vs iteration for each method.
    
    Args:
        f: Function to find root of
        x0, x1: Initial points
        max_iter: Maximum iterations to compare
    """
    # Get reference solution using many iterations
    root_ref, _, _ = secant_method(f, x0, x1, tol=1e-14, max_iter=100)
    
    # Compare methods
    methods = {
        'Secant': lambda: secant_method(f, x0, x1, store_history=True)[2],
        'Regula Falsi': lambda: [x for i in range(max_iter)],
        'Modified': lambda: [modified_secant(f, x0, max_iter=i)[0] 
                           for i in range(1, max_iter+1)]
    }
    
    plt.figure(figsize=(10, 6))
    for name, method in methods.items():
        try:
            history = method()
            errors = [abs(x - root_ref) for x in history]
            plt.semilogy(errors, '.-', label=name)
        except ValueError:
            print(f"{name} method failed")
    
    plt.grid(True)
    plt.xlabel('Iteration')
    plt.ylabel('Error (log scale)')
    plt.title('Convergence Comparison')
    plt.legend()
    plt.show()

# Example usage
if __name__ == "__main__":
    # Example 1: Find root of cos(x) - x = 0
    def f1(x):
        return np.cos(x) - x
    
    x0, x1 = 0.0, 1.0
    root, iters, history = secant_method(f1, x0, x1, store_history=True)
    print(f"Secant method root: {root:.10f}")
    print(f"Iterations: {iters}")
    
    # Visualize steps
    visualize_secant_steps(f1, x0, x1, (0, 2))
    
    # Analyze convergence
    if history:
        order = analyze_convergence(history, root)
        print(f"Estimated convergence order: {order:.2f}")
        print(f"Theoretical order: {(1 + np.sqrt(5))/2:.2f}")
        
        # Compare methods
        plot_convergence_comparison(f1, x0, x1)
        
        # Plot convergence
        errors = [abs(x - root) for x in history]
        plot_convergence(errors, title="Secant Method Convergence")
    
    # Example 2: More challenging function x³ - 2x - 5
    def f2(x):
        return x**3 - 2*x - 5
        
    try:
        root2, iters2, _ = secant_method(f2, 1.0, 2.0)
        print(f"\nRoot of x³ - 2x - 5: {root2:.10f}")
        print(f"Iterations: {iters2}")
    except ValueError as e:
        print(f"Method failed: {e}")
