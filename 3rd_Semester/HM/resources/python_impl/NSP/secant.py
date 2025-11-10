"""
Implementation of the secant method for finding roots.
Includes variants and convergence analysis.
"""

from typing import Callable, Tuple, List, Optional
import numpy as np
import matplotlib.pyplot as plt

from basics.plot_functions import plot_function_1d, plot_convergence

def secant_method(f: Callable[[float], float],
                 x0: float,
                 x1: float,
                 tol: float = 1e-10,
                 max_iter: int = 100,
                 store_history: bool = False) -> Tuple[float, int, Optional[List[float]]]:
    """
    Standard secant method for finding roots.
    
    Args:
        f: Function to find root of
        x0, x1: Initial guesses
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
        store_history: Whether to store iteration history
    
    Returns:
        Tuple containing:
        - Final approximation
        - Number of iterations performed
        - List of iterations if store_history=True, else None
    """
    if abs(f(x1) - f(x0)) < tol:
        raise ValueError("Initial points too close together")
        
    history = [x0, x1] if store_history else None
    
    for i in range(max_iter):
        f_x0, f_x1 = f(x0), f(x1)
        
        # Secant step
        x_new = x1 - f_x1 * (x1 - x0)/(f_x1 - f_x0)
        
        if store_history:
            history.append(x_new)
            
        if abs(x_new - x1) < tol:
            return x_new, i + 1, history
            
        # Update points
        x0, x1 = x1, x_new
        
    return x1, max_iter, history

def regula_falsi(f: Callable[[float], float],
                a: float,
                b: float,
                tol: float = 1e-10,
                max_iter: int = 100) -> Tuple[float, int]:
    """
    Regula falsi (false position) method.
    Requires initial bracket containing the root.
    
    Args:
        f: Function to find root of
        a, b: Initial bracket endpoints with f(a)*f(b) < 0
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
    
    Returns:
        Tuple containing:
        - Final approximation
        - Number of iterations performed
    """
    f_a, f_b = f(a), f(b)
    
    if f_a * f_b >= 0:
        raise ValueError("Initial points must bracket the root")
        
    for i in range(max_iter):
        # False position step
        c = (a * f_b - b * f_a)/(f_b - f_a)
        f_c = f(c)
        
        if abs(f_c) < tol:
            return c, i + 1
            
        # Update bracket
        if f_c * f_a < 0:
            b, f_b = c, f_c
        else:
            a, f_a = c, f_c
            
    return c, max_iter

def modified_secant(f: Callable[[float], float],
                   x0: float,
                   h: float = 1e-4,
                   tol: float = 1e-10,
                   max_iter: int = 100) -> Tuple[float, int]:
    """
    Modified secant method using finite difference approximation.
    
    Args:
        f: Function to find root of
        x0: Initial guess
        h: Finite difference step size
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
    
    Returns:
        Tuple containing:
        - Final approximation
        - Number of iterations performed
    """
    x = x0
    
    for i in range(max_iter):
        f_x = f(x)
        f_xh = f(x + h)
        
        if abs(f_xh - f_x) < tol:
            raise ValueError("Function values too close")
            
        # Modified secant step
        x_new = x - f_x * h/(f_xh - f_x)
        
        if abs(x_new - x) < tol:
            return x_new, i + 1
            
        x = x_new
        
    return x, max_iter

def visualize_secant_steps(f: Callable[[float], float],
                         x0: float,
                         x1: float,
                         x_range: Tuple[float, float],
                         num_steps: int = 5) -> None:
    """
    Visualize secant method iterations.
    
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
    
    x_prev, x_curr = x0, x1
    plt.plot([x_prev, x_curr], [f(x_prev), f(x_curr)], 'go', label='Initial points')
    
    for i in range(num_steps):
        f_prev, f_curr = f(x_prev), f(x_curr)
        
        # Calculate next point
        x_new = x_curr - f_curr * (x_curr - x_prev)/(f_curr - f_prev)
        f_new = f(x_new)
        
        # Plot secant line
        plt.plot([x_prev, x_curr], [f_prev, f_curr], 'r--', alpha=0.5)
        plt.plot(x_new, f_new, 'ro')
        
        # Update points
        x_prev, x_curr = x_curr, x_new
        
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Secant Method Iterations')
    plt.legend()
    plt.show()

def analyze_convergence(x_hist: List[float], x_star: float) -> float:
    """
    Analyze convergence rate of secant method.
    Theoretical order is (1 + √5)/2 ≈ 1.618 (golden ratio).
    
    Args:
        x_hist: List of iterations
        x_star: Known root
    
    Returns:
        float: Estimated convergence order
    """
    errors = [abs(x - x_star) for x in x_hist]
    orders = []
    
    for i in range(len(errors)-2):
        if errors[i+1] > 0 and errors[i] > 0:
            order = np.log(errors[i+2]/errors[i+1]) / np.log(errors[i+1]/errors[i])
            if not np.isnan(order) and not np.isinf(order):
                orders.append(order)
                
    return np.mean(orders) if orders else 0.0

# Example usage
if __name__ == "__main__":
    # Example 1: Find root of cos(x) - x = 0 using secant method
    def f1(x: float) -> float:
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
        
        # Plot convergence
        errors = [abs(x - root) for x in history]
        plot_convergence(errors, title="Secant Method Convergence")
    
    # Example 2: Compare with regula falsi
    try:
        root_rf, iters_rf = regula_falsi(f1, 0.0, 1.0)
        print(f"\nRegula falsi root: {root_rf:.10f}")
        print(f"Regula falsi iterations: {iters_rf}")
    except ValueError as e:
        print(f"Regula falsi failed: {e}")
    
    # Example 3: Modified secant method
    try:
        root_mod, iters_mod = modified_secant(f1, 1.0)
        print(f"\nModified secant root: {root_mod:.10f}")
        print(f"Modified secant iterations: {iters_mod}")
    except ValueError as e:
        print(f"Modified secant failed: {e}")
