"""
Implementation of iterative methods for solving linear systems.
Includes Jacobi, Gauss-Seidel, and SOR methods with convergence analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from basics.rechnerarithmetik import get_machine_epsilon

def decompose_matrix(A):
    """
    Decompose matrix A into diagonal (D), strictly lower (L), and strictly upper (U) parts.
    For iterative methods, we often need the decomposition A = D + L + U.
    """
    A = np.array(A)
    n = len(A)
    
    # Extract diagonal matrix
    D = np.diag(np.diag(A))
    # Extract strictly lower triangular part
    L = np.tril(A, -1)
    # Extract strictly upper triangular part
    U = np.triu(A, 1)
    
    return D, L, U

def jacobi_iteration(A, b, x0, max_iter=1000, tol=1e-10):
    """
    Solve linear system using Jacobi iteration.
    x_{k+1} = D^{-1}(b - (L+U)x_k) where A = D + L + U
    """
    A = np.array(A)
    b = np.array(b)
    x = np.array(x0)
    n = len(b)
    residual_norms = []
    
    for iteration in range(max_iter):
        # Save previous iteration
        x_old = x.copy()
        
        # Compute new iteration: x = D^{-1}(b - (L+U)x)
        for i in range(n):
            x[i] = (b[i] - np.dot(A[i,:i], x_old[:i]) - 
                    np.dot(A[i,i+1:], x_old[i+1:])) / A[i,i]
        
        # Check convergence using max norm
        if np.max(np.abs(x - x_old)) < tol:
            return x, iteration + 1, residual_norms
        
        # Compute residual norm
        residual = np.linalg.norm(b - np.dot(A, x))
        residual_norms.append(residual)
    
    return x, max_iter, residual_norms

def gauss_seidel_iteration(A, b, x0, max_iter=1000, tol=1e-10):
    """
    Solve linear system using Gauss-Seidel iteration.
    x_{k+1} = (D+L)^{-1}(b - Ux_k) where A = D + L + U
    """
    A = np.array(A)
    b = np.array(b)
    x = np.array(x0)
    n = len(b)
    residual_norms = []
    
    for iteration in range(max_iter):
        x_old = x.copy()
        
        # Update each component using the latest values
        for i in range(n):
            x[i] = (b[i] - np.dot(A[i,:i], x[:i]) - 
                    np.dot(A[i,i+1:], x_old[i+1:])) / A[i,i]
        
        # Check convergence
        if np.max(np.abs(x - x_old)) < tol:
            return x, iteration + 1, residual_norms
            
        # Compute residual norm
        residual = np.linalg.norm(b - np.dot(A, x))
        residual_norms.append(residual)
    
    return x, max_iter, residual_norms

def sor_iteration(A, b, x0, omega, max_iter=1000, tol=1e-10):
    """
    Solve linear system using Successive Over-Relaxation (SOR).
    x_new = omega * x_gs + (1-omega) * x_old
    where x_gs is the Gauss-Seidel update
    """
    if not 0 < omega < 2:
        raise ValueError("Relaxation parameter must be between 0 and 2")
        
    A = np.array(A)
    b = np.array(b)
    x = np.array(x0)
    n = len(b)
    residual_norms = []
    
    for iteration in range(max_iter):
        x_old = x.copy()
        
        # Compute new values with relaxation
        for i in range(n):
            x_gs = (b[i] - np.dot(A[i,:i], x[:i]) - 
                   np.dot(A[i,i+1:], x_old[i+1:])) / A[i,i]
            x[i] = x_old[i] + omega * (x_gs - x_old[i])
        
        if np.max(np.abs(x - x_old)) < tol:
            return x, iteration + 1, residual_norms
            
        residual = np.linalg.norm(b - np.dot(A, x))
        residual_norms.append(residual)
    
    return x, max_iter, residual_norms

def estimate_spectral_radius(A, max_iter=100):
    """
    Estimate spectral radius using power iteration.
    The spectral radius determines convergence of iterative methods.
    """
    A = np.array(A)
    n = len(A)
    x = np.ones(n) / np.sqrt(n)
    lambda_old = 0
    
    for _ in range(max_iter):
        # Power iteration step
        y = np.dot(A, x)
        lambda_new = abs(np.dot(x, y))
        
        if abs(lambda_new - lambda_old) < get_machine_epsilon():
            return lambda_new
            
        x = y / np.linalg.norm(y)
        lambda_old = lambda_new
    
    return lambda_new

def check_convergence_conditions(A):
    """
    Check convergence conditions for iterative methods.
    Returns dict with analysis of diagonal dominance, spectral radius,
    and matrix properties.
    """
    A = np.array(A)
    n = len(A)
    results = {}
    
    # Check diagonal dominance
    diag = np.abs(np.diag(A))
    row_sums = np.sum(np.abs(A), axis=1) - diag
    results['diagonally_dominant'] = np.all(diag > row_sums)
    
    # Get matrix decomposition
    D, L, U = decompose_matrix(A)
    D_inv = np.linalg.inv(D)
    
    # Check Jacobi convergence
    B_j = -np.dot(D_inv, (L + U))
    results['jacobi_spectral_radius'] = estimate_spectral_radius(B_j)
    results['jacobi_converges'] = results['jacobi_spectral_radius'] < 1
    
    # Check symmetry and positive definiteness
    results['symmetric'] = np.allclose(A, A.T)
    if results['symmetric']:
        eigenvals = np.linalg.eigvals(A)
        results['positive_definite'] = np.all(np.real(eigenvals) > 0)
    else:
        results['positive_definite'] = None
    
    return results

def analyze_methods(A, b, x0, show_plots=True):
    """
    Run and analyze all iterative methods on given system.
    """
    methods = [
        ('Jacobi', lambda A, b, x0: jacobi_iteration(A, b, x0)),
        ('Gauss-Seidel', lambda A, b, x0: gauss_seidel_iteration(A, b, x0)),
        ('SOR (ω=1.2)', lambda A, b, x0: sor_iteration(A, b, x0, omega=1.2))
    ]
    
    if show_plots:
        plt.figure(figsize=(10, 6))
    
    print("\nMethod Comparison:")
    print(f"{'Method':<15} {'Iterations':>10} {'Final Residual':>15}")
    print("-" * 45)
    
    results = {}
    for name, method in methods:
        try:
            x, iters, residuals = method(A, b, x0)
            print(f"{name:<15} {iters:>10} {residuals[-1]:>15.2e}")
            
            if show_plots:
                plt.semilogy(residuals, label=name)
                
            results[name] = {'solution': x, 'iterations': iters, 'residuals': residuals}
            
        except ValueError as e:
            print(f"{name:<15} Failed: {str(e)}")
    
    if show_plots:
        plt.grid(True)
        plt.xlabel('Iteration')
        plt.ylabel('Residual Norm (log scale)')
        plt.title('Convergence Comparison of Iterative Methods')
        plt.legend()
        plt.show()
        
    return results

# Example usage
if __name__ == "__main__":
    # Test matrix - tridiagonal system
    A = np.array([
        [4.0, -1.0, 0.0, -1.0],
        [-1.0, 4.0, -1.0, 0.0],
        [0.0, -1.0, 4.0, -1.0],
        [-1.0, 0.0, -1.0, 4.0]
    ])
    b = np.array([1.0, 5.0, 0.0, 2.0])
    x0 = np.zeros_like(b)
    
    # Analyze convergence conditions
    print("Convergence Analysis:")
    conditions = check_convergence_conditions(A)
    for key, value in conditions.items():
        print(f"{key}: {value}")
    
    # Run analysis of methods
    results = analyze_methods(A, b, x0)
    
    # Test effect of SOR parameter
    omegas = [0.5, 1.0, 1.2, 1.5]
    plt.figure(figsize=(10, 6))
    
    for omega in omegas:
        try:
            _, _, residuals = sor_iteration(A, b, x0, omega)
            plt.semilogy(residuals, label=f'ω={omega:.1f}')
        except ValueError:
            continue
    
    plt.grid(True)
    plt.xlabel('Iteration')
    plt.ylabel('Residual Norm (log scale)')
    plt.title('Effect of Relaxation Parameter in SOR Method')
    plt.legend()
    plt.show()
