"""
Implementation of iterative methods for solving linear systems.
Includes Jacobi and Gauss-Seidel methods.
"""

from typing import List, Tuple, Optional, Callable
import numpy as np
from basics.rechnerarithmetik import get_machine_epsilon

def decompose_matrix(A: List[List[float]]) -> Tuple[List[List[float]], 
                                                   List[List[float]], 
                                                   List[List[float]]]:
    """
    Decompose matrix A into diagonal, strictly lower, and strictly upper parts.
    
    Args:
        A: Input matrix
        
    Returns:
        Tuple containing:
        - Diagonal matrix D
        - Strictly lower triangular matrix L
        - Strictly upper triangular matrix U
    """
    n = len(A)
    D = [[A[i][j] if i == j else 0.0 for j in range(n)] for i in range(n)]
    L = [[A[i][j] if i > j else 0.0 for j in range(n)] for i in range(n)]
    U = [[A[i][j] if i < j else 0.0 for j in range(n)] for i in range(n)]
    
    return D, L, U

def jacobi_iteration(A: List[List[float]], 
                    b: List[float], 
                    x0: List[float], 
                    max_iter: int = 1000, 
                    tol: float = 1e-10) -> Tuple[List[float], int, List[float]]:
    """
    Solve linear system using Jacobi iteration.
    
    Args:
        A: Coefficient matrix
        b: Right-hand side vector
        x0: Initial guess
        max_iter: Maximum number of iterations
        tol: Convergence tolerance
        
    Returns:
        Tuple containing:
        - Solution vector
        - Number of iterations performed
        - List of residual norms
    """
    n = len(A)
    x = x0.copy()
    x_new = [0.0] * n
    residual_norms = []
    
    for iteration in range(max_iter):
        # Compute new approximation
        for i in range(n):
            sum_others = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - sum_others) / A[i][i]
            
        # Check convergence
        max_diff = max(abs(x_new[i] - x[i]) for i in range(n))
        
        # Compute residual
        residual = [b[i] - sum(A[i][j] * x_new[j] for j in range(n)) 
                   for i in range(n)]
        residual_norm = np.sqrt(sum(r*r for r in residual))
        residual_norms.append(residual_norm)
        
        if max_diff < tol:
            return x_new, iteration + 1, residual_norms
            
        # Update solution
        x = x_new.copy()
        
    return x, max_iter, residual_norms

def gauss_seidel_iteration(A: List[List[float]], 
                          b: List[float], 
                          x0: List[float], 
                          max_iter: int = 1000, 
                          tol: float = 1e-10) -> Tuple[List[float], int, List[float]]:
    """
    Solve linear system using Gauss-Seidel iteration.
    
    Args:
        A: Coefficient matrix
        b: Right-hand side vector
        x0: Initial guess
        max_iter: Maximum number of iterations
        tol: Convergence tolerance
        
    Returns:
        Tuple containing:
        - Solution vector
        - Number of iterations performed
        - List of residual norms
    """
    n = len(A)
    x = x0.copy()
    residual_norms = []
    
    for iteration in range(max_iter):
        x_old = x.copy()
        
        # Compute new approximation
        for i in range(n):
            sum_lower = sum(A[i][j] * x[j] for j in range(i))
            sum_upper = sum(A[i][j] * x_old[j] for j in range(i+1, n))
            x[i] = (b[i] - sum_lower - sum_upper) / A[i][i]
            
        # Check convergence
        max_diff = max(abs(x[i] - x_old[i]) for i in range(n))
        
        # Compute residual
        residual = [b[i] - sum(A[i][j] * x[j] for j in range(n)) 
                   for i in range(n)]
        residual_norm = np.sqrt(sum(r*r for r in residual))
        residual_norms.append(residual_norm)
        
        if max_diff < tol:
            return x, iteration + 1, residual_norms
            
    return x, max_iter, residual_norms

def sor_iteration(A: List[List[float]], 
                 b: List[float], 
                 x0: List[float], 
                 omega: float,
                 max_iter: int = 1000, 
                 tol: float = 1e-10) -> Tuple[List[float], int, List[float]]:
    """
    Solve linear system using Successive Over-Relaxation (SOR).
    
    Args:
        A: Coefficient matrix
        b: Right-hand side vector
        x0: Initial guess
        omega: Relaxation parameter (0 < omega < 2)
        max_iter: Maximum number of iterations
        tol: Convergence tolerance
        
    Returns:
        Tuple containing:
        - Solution vector
        - Number of iterations performed
        - List of residual norms
    """
    if not 0 < omega < 2:
        raise ValueError("Relaxation parameter omega must be between 0 and 2")
        
    n = len(A)
    x = x0.copy()
    residual_norms = []
    
    for iteration in range(max_iter):
        x_old = x.copy()
        
        # Compute new approximation
        for i in range(n):
            sum_lower = sum(A[i][j] * x[j] for j in range(i))
            sum_upper = sum(A[i][j] * x_old[j] for j in range(i+1, n))
            x_gs = (b[i] - sum_lower - sum_upper) / A[i][i]
            x[i] = x_old[i] + omega * (x_gs - x_old[i])
            
        # Check convergence
        max_diff = max(abs(x[i] - x_old[i]) for i in range(n))
        
        # Compute residual
        residual = [b[i] - sum(A[i][j] * x[j] for j in range(n)) 
                   for i in range(n)]
        residual_norm = np.sqrt(sum(r*r for r in residual))
        residual_norms.append(residual_norm)
        
        if max_diff < tol:
            return x, iteration + 1, residual_norms
            
    return x, max_iter, residual_norms

def estimate_spectral_radius(A: List[List[float]], 
                           method: str = 'power',
                           max_iter: int = 100) -> float:
    """
    Estimate spectral radius using power iteration.
    
    Args:
        A: Input matrix
        method: Method to use ('power' or 'inverse')
        max_iter: Maximum number of iterations
        
    Returns:
        float: Estimated spectral radius
    """
    n = len(A)
    x = [1.0/np.sqrt(n)] * n
    old_lambda = 0.0
    
    for _ in range(max_iter):
        # Matrix-vector multiplication
        y = [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
        
        # Compute Rayleigh quotient
        new_lambda = abs(sum(x[i] * y[i] for i in range(n)))
        
        # Check convergence
        if abs(new_lambda - old_lambda) < get_machine_epsilon():
            return new_lambda
            
        # Normalize vector
        norm = np.sqrt(sum(y[i]**2 for i in range(n)))
        x = [y[i]/norm for i in range(n)]
        old_lambda = new_lambda
        
    return new_lambda

def check_convergence_conditions(A: List[List[float]]) -> dict:
    """
    Check various convergence conditions for iterative methods.
    
    Args:
        A: Input matrix
        
    Returns:
        dict: Dictionary containing convergence information
    """
    n = len(A)
    results = {}
    
    # Check diagonal dominance
    is_diag_dom = True
    for i in range(n):
        diag = abs(A[i][i])
        row_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
        if diag <= row_sum:
            is_diag_dom = False
            break
    results['diagonally_dominant'] = is_diag_dom
    
    # Decompose matrix
    D, L, U = decompose_matrix(A)
    
    # Check Jacobi convergence
    D_inv = [[1.0/D[i][i] if i == j else 0.0 for j in range(n)] for i in range(n)]
    B_j = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                B_j[i][j] -= D_inv[i][k] * (L[k][j] + U[k][j])
                
    spec_radius_j = estimate_spectral_radius(B_j)
    results['jacobi_spectral_radius'] = spec_radius_j
    results['jacobi_converges'] = spec_radius_j < 1
    
    # Check Gauss-Seidel convergence
    # For simplicity, we'll just use the sufficient condition that A is symmetric positive definite
    is_symmetric = all(A[i][j] == A[j][i] for i in range(n) for j in range(n))
    results['symmetric'] = is_symmetric
    
    if is_symmetric:
        # Check positive definiteness using eigenvalues
        eigenvals = []
        for i in range(n):
            x = [1.0 if j == i else 0.0 for j in range(n)]
            Ax = [sum(A[k][j] * x[j] for j in range(n)) for k in range(n)]
            eigenvals.append(sum(x[j] * Ax[j] for j in range(n)))
        results['positive_definite'] = all(ev > 0 for ev in eigenvals)
    else:
        results['positive_definite'] = None
    
    return results

# Example usage
if __name__ == "__main__":
    # Example 1: Well-conditioned system
    A1 = [
        [4.0, -1.0, 0.0, -1.0],
        [-1.0, 4.0, -1.0, 0.0],
        [0.0, -1.0, 4.0, -1.0],
        [-1.0, 0.0, -1.0, 4.0]
    ]
    b1 = [1.0, 5.0, 0.0, 2.0]
    x0 = [0.0] * len(b1)
    
    # Check convergence conditions
    print("Convergence analysis:")
    conditions = check_convergence_conditions(A1)
    for key, value in conditions.items():
        print(f"{key}: {value}")
        
    # Compare methods
    methods = [
        ('Jacobi', lambda A, b, x0: jacobi_iteration(A, b, x0)),
        ('Gauss-Seidel', lambda A, b, x0: gauss_seidel_iteration(A, b, x0)),
        ('SOR (ω=1.2)', lambda A, b, x0: sor_iteration(A, b, x0, omega=1.2))
    ]
    
    print("\nComparison of methods:")
    print(f"{'Method':<15} {'Iterations':>10} {'Final residual':>15}")
    print("-" * 40)
    
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    
    for method_name, method_func in methods:
        try:
            x, iters, residuals = method_func(A1, b1, x0)
            print(f"{method_name:<15} {iters:>10d} {residuals[-1]:>15.2e}")
            
            # Plot convergence
            plt.semilogy(residuals, label=method_name)
            
        except ValueError as e:
            print(f"{method_name:<15} Failed: {str(e)}")
            
    plt.grid(True)
    plt.xlabel('Iteration')
    plt.ylabel('Residual norm (log scale)')
    plt.title('Convergence Comparison')
    plt.legend()
    plt.show()
    
    # Example 2: Effect of matrix condition number
    def generate_test_matrix(n: int, condition: float = 1000.0) -> List[List[float]]:
        """Generate test matrix with given condition number."""
        # Create random orthogonal matrix
        Q = np.random.randn(n, n)
        Q, _ = np.linalg.qr(Q)
        Q = Q.tolist()
        
        # Create diagonal matrix with desired condition number
        D = [[0.0] * n for _ in range(n)]
        for i in range(n):
            D[i][i] = condition ** (i/(n-1)) if n > 1 else 1.0
            
        # Form final matrix A = QDQ^T
        temp = [[sum(Q[i][k] * D[k][j] for k in range(n))
                for j in range(n)] for i in range(n)]
        A = [[sum(temp[i][k] * Q[j][k] for k in range(n))
              for j in range(n)] for i in range(n)]
        
        return A
    
    # Test different condition numbers
    n = 20
    conditions = [1.0, 10.0, 100.0, 1000.0]
    
    print("\nEffect of condition number:")
    print(f"{'Condition':>10} {'Method':>15} {'Iterations':>10}")
    print("-" * 40)
    
    for cond in conditions:
        A = generate_test_matrix(n, cond)
        b = [1.0] * n
        x0 = [0.0] * n
        
        for method_name, method_func in methods:
            try:
                x, iters, residuals = method_func(A, b, x0)
                print(f"{cond:10.1f} {method_name:>15} {iters:>10d}")
                
            except ValueError as e:
                print(f"{cond:10.1f} {method_name:>15} Failed")
                
    # Example 3: Optimal SOR parameter
    def find_optimal_omega(A: List[List[float]], 
                         b: List[float],
                         x0: List[float],
                         omega_range: List[float] = None) -> float:
        """Find optimal relaxation parameter for SOR."""
        if omega_range is None:
            omega_range = np.linspace(0.1, 1.9, 19)
            
        best_omega = 1.0
        min_iters = float('inf')
        
        for omega in omega_range:
            try:
                _, iters, _ = sor_iteration(A, b, x0.copy(), omega)
                if iters < min_iters:
                    min_iters = iters
                    best_omega = omega
            except ValueError:
                continue
                
        return best_omega
    
    # Find optimal omega for example matrix
    best_omega = find_optimal_omega(A1, b1, x0)
    print(f"\nOptimal SOR parameter: {best_omega:.2f}")
    
    # Compare with standard omega values
    omegas = [0.5, 1.0, best_omega, 1.5]
    plt.figure(figsize=(10, 6))
    
    for omega in omegas:
        try:
            _, _, residuals = sor_iteration(A1, b1, x0, omega)
            plt.semilogy(residuals, label=f'ω={omega:.2f}')
        except ValueError:
            continue
            
    plt.grid(True)
    plt.xlabel('Iteration')
    plt.ylabel('Residual norm (log scale)')
    plt.title('SOR Convergence for Different ω')
    plt.legend()
    plt.show()