"""
Implementation of Newton's method and its variants for finding roots.
Includes standard Newton's method, simplified Newton's method, and damped Newton's method.
"""

import numpy as np
import matplotlib.pyplot as plt
from plot_functions import plot_function_1d, plot_convergence

def newton_method(f, df, x0, tol=1e-10, max_iter=100, store_history=False):
    """
    Standard Newton's method for finding roots: x_{n+1} = x_n - f(x_n)/f'(x_n)
    This is the classical implementation with quadratic convergence near roots.
    
    Args:
        f: Function to find root of
        df: Derivative of f
        x0: Initial guess
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
        store_history: Whether to store iteration history
    
    Returns:
        Tuple of (final approximation, iterations performed, history if requested)
    """
    x = x0
    history = [x0] if store_history else None
    
    for i in range(max_iter):
        # Calculate derivative at current point
        df_x = df(x)
        
        # Check for near-zero derivative to avoid division by zero
        if abs(df_x) < tol:
            raise ValueError(f"Derivative too close to zero at x = {x}")
        
        # Newton step: x - f(x)/f'(x)
        x_new = x - f(x)/df_x
        
        # Store iteration if requested
        if store_history:
            history.append(x_new)
        
        # Check for convergence
        if abs(x_new - x) < tol:
            return x_new, i + 1, history
            
        x = x_new
        
    return x, max_iter, history

def simplified_newton(f, df, x0, tol=1e-10, max_iter=100):
    """
    Simplified Newton's method using constant derivative evaluation.
    This variant only evaluates the derivative once at x0, trading convergence speed
    for computational efficiency. Convergence is linear instead of quadratic.
    
    Args:
        f: Function to find root of
        df: Derivative of f
        x0: Initial guess
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
    
    Returns:
        Tuple of (final approximation, iterations performed)
    """
    x = x0
    # Calculate derivative only once at initial point
    df_x0 = df(x0)
    
    if abs(df_x0) < tol:
        raise ValueError(f"Initial derivative too close to zero at x0 = {x0}")
    
    for i in range(max_iter):
        # Simplified Newton step using initial derivative
        x_new = x - f(x)/df_x0
        
        if abs(x_new - x) < tol:
            return x_new, i + 1
            
        x = x_new
        
    return x, max_iter

def damped_newton(f, df, x0, lambda_min=0.1, tol=1e-10, max_iter=100):
    """
    Damped Newton's method with line search.
    This variant uses a damping factor to improve global convergence.
    The damping factor is adjusted by line search to ensure |f(x_{n+1})| < |f(x_n)|.
    
    Args:
        f: Function to find root of
        df: Derivative of f
        x0: Initial guess
        lambda_min: Minimum damping factor
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
    
    Returns:
        Tuple of (final approximation, iterations performed, damping factors used)
    """
    x = x0
    damping_factors = []
    
    for i in range(max_iter):
        # Calculate derivative and check for zero
        df_x = df(x)
        if abs(df_x) < tol:
            raise ValueError(f"Derivative too close to zero at x = {x}")
            
        # Calculate standard Newton step
        dx = -f(x)/df_x
        
        # Line search with damping
        lambda_k = 1.0  # Start with full Newton step
        while lambda_k >= lambda_min:
            x_new = x + lambda_k * dx
            # Check if residual is reduced
            if abs(f(x_new)) < abs(f(x)):
                break
            lambda_k /= 2  # Reduce step size
            
        damping_factors.append(lambda_k)
        
        # Check if line search failed
        if lambda_k < lambda_min:
            raise ValueError(f"No improvement found with damping at x = {x}")
            
        # Check for convergence
        if abs(x_new - x) < tol:
            return x_new, i + 1, damping_factors
            
        x = x_new
        
    return x, max_iter, damping_factors

def analyze_convergence_order(x_hist, x_star):
    """
    Analyze convergence order from iteration history.
    Uses the formula: p ≈ ln(|e_{n+2}|/|e_{n+1}|) / ln(|e_{n+1}|/|e_n|)
    where e_n is the error at iteration n.
    
    Args:
        x_hist: List of iterations
        x_star: Known root
        
    Returns:
        Estimated convergence order
    """
    # Calculate absolute errors
    errors = [abs(x - x_star) for x in x_hist]
    orders = []
    
    # Estimate convergence order using three consecutive iterations
    for i in range(len(errors)-2):
        if errors[i+1] > 0 and errors[i] > 0:
            order = np.log(errors[i+2]/errors[i+1]) / np.log(errors[i+1]/errors[i])
            if not np.isnan(order) and not np.isinf(order):
                orders.append(order)
                
    return np.mean(orders) if orders else 0.0

def visualize_newton_steps(f, df, x0, x_range, num_steps=5):
    """
    Visualize Newton iteration steps graphically.
    Shows the function, tangent lines at each iteration, and convergence path.
    
    Args:
        f: Function to find root of
        df: Derivative of f
        x0: Initial guess
        x_range: Plot range (xmin, xmax)
        num_steps: Number of steps to visualize
    """
    # Create x points for plotting
    x = np.linspace(x_range[0], x_range[1], 1000)
    y = [f(xi) for xi in x]
    
    plt.figure(figsize=(12, 8))
    # Plot function and x-axis
    plt.plot(x, y, 'b-', label='f(x)')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    
    # Plot iterations
    x_curr = x0
    plt.plot(x_curr, f(x_curr), 'go', label='Start')
    
    for i in range(num_steps):
        # Calculate derivative and new point
        df_x = df(x_curr)
        x_new = x_curr - f(x_curr)/df_x
        
        # Plot tangent line
        x_tang = np.array([x_curr - 1, x_curr + 1])
        y_tang = f(x_curr) + df_x * (x_tang - x_curr)
        
        plt.plot(x_tang, y_tang, 'r--', alpha=0.5)
        plt.plot(x_new, f(x_new), 'ro')
        
        x_curr = x_new
        
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title("Newton's Method Iterations")
    plt.legend()
    plt.show()

def plot_basins_of_attraction(f, df, x_range, y_range, n_points=100, max_iter=50):
    """
    Plot basins of attraction for complex Newton's method.
    Different colors indicate convergence to different roots.
    
    Args:
        f: Complex function
        df: Derivative of f
        x_range, y_range: Plot ranges for real and imaginary parts
        n_points: Number of points in each dimension
        max_iter: Maximum iterations per point
    """
    x = np.linspace(x_range[0], x_range[1], n_points)
    y = np.linspace(y_range[0], y_range[1], n_points)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X, dtype=complex)
    
    # Try Newton's method from each starting point
    for i in range(n_points):
        for j in range(n_points):
            z = complex(X[i,j], Y[i,j])
            for k in range(max_iter):
                z_new = z - f(z)/df(z)
                if abs(z_new - z) < 1e-10:
                    break
                z = z_new
            Z[i,j] = z
    
    # Plot the results
    plt.figure(figsize=(10, 10))
    plt.imshow(np.angle(Z), extent=[x_range[0], x_range[1], y_range[0], y_range[1]], 
               cmap='hsv')
    plt.colorbar(label='Argument of final value')
    plt.title('Basins of Attraction')
    plt.xlabel('Re(z)')
    plt.ylabel('Im(z)')
    plt.show()

# Example usage
if __name__ == "__main__":
    # Example 1: Find root of cos(x) - x = 0
    def f1(x):
        return np.cos(x) - x
    
    def df1(x):
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
    
    # Example 2: Complex polynomial z³ - 1
    def f2(z):
        return z**3 - 1
    
    def df2(z):
        return 3*z**2
    
    # Plot basins of attraction
    plot_basins_of_attraction(f2, df2, (-2, 2), (-2, 2))
