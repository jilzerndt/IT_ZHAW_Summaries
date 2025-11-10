"""
Plotting utilities for numerical methods visualization.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, List, Tuple, Optional
from mpl_toolkits.mplot3d import Axes3D

def plot_function_1d(f: Callable[[float], float], 
                    x_range: Tuple[float, float],
                    title: str = "Function Plot",
                    num_points: int = 1000,
                    roots: List[float] = None,
                    iterations: List[float] = None) -> None:
    """
    Plot a 1D function with optional roots and iteration points.
    
    Args:
        f: Function to plot
        x_range: Tuple of (min_x, max_x)
        title: Plot title
        num_points: Number of points for plotting
        roots: List of known roots to mark
        iterations: List of iteration points to mark
    """
    x = np.linspace(x_range[0], x_range[1], num_points)
    y = [f(xi) for xi in x]
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', label='f(x)')
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    
    if roots:
        plt.plot(roots, [f(r) for r in roots], 'ro', label='Roots')
        
    if iterations:
        plt.plot(iterations, [f(x) for x in iterations], 'g.', label='Iterations')
        
    plt.grid(True, alpha=0.3)
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.show()

def plot_convergence(errors: List[float], 
                    title: str = "Convergence Plot",
                    log_scale: bool = True) -> None:
    """
    Plot convergence of numerical method using error values.
    
    Args:
        errors: List of error values
        title: Plot title
        log_scale: Whether to use logarithmic scale
    """
    plt.figure(figsize=(10, 6))
    iterations = range(len(errors))
    
    plt.plot(iterations, errors, 'b.-')
    plt.grid(True, alpha=0.3)
    
    if log_scale:
        plt.yscale('log')
        
    plt.title(title)
    plt.xlabel('Iteration')
    plt.ylabel('Error (log scale)' if log_scale else 'Error')
    plt.show()

def plot_function_2d(f: Callable[[float, float], float],
                    x_range: Tuple[float, float],
                    y_range: Tuple[float, float],
                    title: str = "2D Function Plot",
                    num_points: int = 100,
                    view_angle: Tuple[float, float] = (30, 45)) -> None:
    """
    Create 3D surface plot of 2D function.
    
    Args:
        f: Function f(x,y) to plot
        x_range: Tuple of (min_x, max_x)
        y_range: Tuple of (min_y, max_y)
        title: Plot title
        num_points: Number of points in each dimension
        view_angle: Tuple of (elevation, azimuth) for 3D view
    """
    x = np.linspace(x_range[0], x_range[1], num_points)
    y = np.linspace(y_range[0], y_range[1], num_points)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)
    
    for i in range(num_points):
        for j in range(num_points):
            Z[i,j] = f(X[i,j], Y[i,j])
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(X, Y, Z, cmap='viridis')
    fig.colorbar(surf)
    
    ax.view_init(view_angle[0], view_angle[1])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('f(x,y)')
    plt.title(title)
    plt.show()

def plot_contour(f: Callable[[float, float], float],
                x_range: Tuple[float, float],
                y_range: Tuple[float, float],
                title: str = "Contour Plot",
                num_points: int = 100,
                levels: int = 20,
                show_minimum: bool = False) -> None:
    """
    Create contour plot of 2D function.
    
    Args:
        f: Function f(x,y) to plot
        x_range: Tuple of (min_x, max_x)
        y_range: Tuple of (min_y, max_y)
        title: Plot title
        num_points: Number of points in each dimension
        levels: Number of contour levels
        show_minimum: Whether to mark the minimum point
    """
    x = np.linspace(x_range[0], x_range[1], num_points)
    y = np.linspace(y_range[0], y_range[1], num_points)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)
    
    for i in range(num_points):
        for j in range(num_points):
            Z[i,j] = f(X[i,j], Y[i,j])
    
    plt.figure(figsize=(10, 8))
    plt.contour(X, Y, Z, levels=levels)
    plt.colorbar(label='f(x,y)')
    
    if show_minimum:
        min_idx = np.unravel_index(np.argmin(Z), Z.shape)
        plt.plot(X[min_idx], Y[min_idx], 'r*', label='Minimum')
        plt.legend()
    
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(title)
    plt.show()

# Example usage
if __name__ == "__main__":
    # Example 1D function plot
    def f1(x: float) -> float:
        return x**2 - 4
    
    plot_function_1d(f1, (-3, 3), "f(x) = x² - 4", 
                     roots=[-2, 2], 
                     iterations=[-2.5, -2.2, -2.1, -2.01])
    
    # Example convergence plot
    errors = [1, 0.1, 0.01, 0.001, 0.0001]
    plot_convergence(errors, "Example Convergence")
    
    # Example 2D function plot
    def f2(x: float, y: float) -> float:
        return x**2 + y**2
    
    plot_function_2d(f2, (-2, 2), (-2, 2), "f(x,y) = x² + y²")
    plot_contour(f2, (-2, 2), (-2, 2), "Contour: f(x,y) = x² + y²", 
                show_minimum=True)
