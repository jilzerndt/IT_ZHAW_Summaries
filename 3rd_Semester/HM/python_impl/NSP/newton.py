"""
Implementation of Newton's method and its variants for finding roots.
Includes standard Newton's method, simplified Newton's method, and damped Newton's method.
"""

from typing import Callable, Tuple, List, Optional
import numpy as np
from plot_functions import plot_function_1d, plot_convergence

def newton_method(f: Callable[[float], float],
                 df: Callable[[float], float],
                 x0: float,
                 tol: float = 1e-10,
                 max_iter: int = 100,
                 store_history: bool = False) -> Tuple[float, int, Optional[List[float]]]:
    """
    Standard Newton's method for finding roots.
    
    Args:
        f: Function to find root of
        df: Derivative of f
        x0: Initial guess
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
        store_history: Whether to store iteration history
    
    Returns:
        Tuple containing:
        - Final approximation
        - Number of iterations performed
        - List of iterations if store_history=True, else None
    """
    x = x0
    history = [x0] if store_history else None
    
    for i in range(max_iter):
        df_x = df(x)
        if abs(df_x) < tol:  # Avoid division by zero
            raise ValueError(f"Derivative too close to zero at x = {x}")
            
        x_new = x - f(x)/df_x
        
        if store_history:
            history.append(x_new)
            
        if abs(x_new - x) < tol:
            return x_new, i + 1, history
            
        x = x_new
        
    return x, max_iter, history

def simplified_newton(f: Callable[[float], float],
                     df: Callable[[float], float],
                     x0: float,
                     tol: float = 1e-10,
                     max_iter: int = 100) -> Tuple[float, int]:
    """
    Simplified Newton's method using constant derivative evaluation.
    
    Args:
        f: Function to find root of
        df: Derivative of f
        x0: Initial guess
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
    
    Returns:
        Tuple containing:
        - Final approximation
        - Number of iterations performed
    """
    x = x0
    df_x0 = df(x0)  # Calculate derivative only once
    
    if abs(df_x0) < tol:
        raise ValueError(f"Initial derivative too close to zero at x0 = {x0}")
    
    for i in range(max_iter):
        x_new = x - f(x)/df_x0
        
        if abs(x_new - x) < tol:
            return x_new, i + 1
            
        x = x_new
        
    return x, max_iter

def damped_newton(f: Callable[[float], float],
                 df: Callable[[float], float],
                 x0: float,
                 lambda_min: float = 0.1,
                 tol: float = 1e-10,
                 max_iter: int = 100) -> Tuple[float, int, List[float]]:
    """
    Damped Newton's method with line search.
    
    Args:
        f: Function to find root of
        df: Derivative of f
        x0: Initial guess
        lambda_min: Minimum damping factor
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
    
    Returns:
        Tuple containing:
        - Final approximation
        - Number of iterations performed
        - List of damping factors used
    """
    x = x0
    damping_factors = []
    
    for i in range(max_iter):
        df_x = df(x)
        if abs(df_x) < tol:
            raise ValueError(f"Derivative too close to zero at x = {x}")
            
        # Standard Newton step
        dx = -f(x)/df_x
        
        # Line search with damping
        lambda_k = 1.0
        while lambda_k >= lambda_min:
            x_new = x + lambda_k * dx
            if abs(f(x_new)) < abs(f(x)):  # Improvement found
                break
            lambda_k /= 2
            
        damping_factors.append(lambda_k)
        
        if lambda_k < lambda_min:
            raise ValueError(f"No improvement found with damping at x = {x}")
            
        if abs(x_new - x) < tol:
            return x_new, i + 1, damping_factors
            
        x = x_new
        
    return x, max_iter, damping_factors

def analyze_convergence_order(x_hist: List[float], x_star: float) -> float:
    """
    Analyze convergence order from iteration history.
    
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

def visualize_newton_steps(f: Callable[[float], float],
                         df: Callable[[float], float],
                         x0: float,
                         x_range: Tuple[float, float],
                         num_steps: int = 5) -> None:
    """
    Visualize Newton iteration steps.
    
    Args:
        f: Function to find root of
        df: Derivative of f
        x0: Initial guess
        x_range: Plot range (xmin, xmax)
        num_steps: Number of steps to visualize
    """
    x = np.linspace(x_range[0], x_range[1], 1000)
    y = [f(xi) for xi in x]
    
    plt.figure(figsize=(12, 8))
    plt.plot(x, y, 'b-', label='f(x)')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    
    x_curr = x0
    plt.plot(x_curr, f(x_curr), 'go', label='Start')
    
    for i in range(num_steps):
        # Plot tangent line
        df_x = df(x_curr)
        x_new = x_curr - f(x_curr)/df_x
        
        # Tangent line points
        x_tang = np.array([x_curr - 1, x_curr + 1])
        y_tang = f(x_curr) + df_x * (x_tang - x_curr)
        
        plt.plot(x_tang, y_tang, 'r--', alpha=0.5)
        plt.plot(x_new, f(x_new), 'ro')
        
        # Update for next iteration
        x_curr = x_new
        
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title("Newton's Method Iterations")
    plt.legend()
    plt.show()

# Example usage
if __name__ == "__main__":
    # Example 1: Find root of cos(x) - x = 0
    def f1(x: float) -> float:
        return np.cos(x) - x
    
    def df1(x: float) -> float:
        return -np.sin(x) - 1
    
    x0 = 1.0
    root, iters, history = newton_method(f1, df1, x0, store_history=True)
    print(f"Root found: {root:.10f}")
    print(f"Iterations: {iters}")
    
    # Visualize steps
    visualize_newton_steps(f1, df1, x0, (0, 2))
    
    # Analyze convergence
    if history:
        order = analyze_convergence_order(history, root)
        print(f"Estimated convergence order: {order:.2f}")
        
        # Plot convergence
        errors = [abs(x - root) for x in history]
        plot_convergence(errors, title="Newton's Method Convergence")
    
    # Example 2: Compare with simplified Newton
    root_simple, iters_simple = simplified_newton(f1, df1, x0)
    print(f"\nSimplified Newton root: {root_simple:.10f}")
    print(f"Simplified Newton iterations: {iters_simple}")
    
    # Example 3: Damped Newton for more difficult function
    def f2(x: float) -> float:
        return x**3 - 2*x + 2
    
    def df2(x: float) -> float:
        return 3*x**2 - 2
    
    try:
        root_damped, iters_damped, lambdas = damped_newton(f2, df2, x0)
        print(f"\nDamped Newton root: {root_damped:.10f}")
        print(f"Damped Newton iterations: {iters_damped}")
        print(f"Average damping factor: {np.mean(lambdas):.4f}")
    except ValueError as e:
        print(f"Damped Newton failed: {e}")
