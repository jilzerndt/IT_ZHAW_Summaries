"""
Implementation of Gaussian elimination with and without pivoting.
"""

from typing import List, Tuple, Optional
import numpy as np
from basics.rechnerarithmetik import get_machine_epsilon
from pivotisierung import PivotingManager

def forward_elimination(A: List[List[float]],
                      b: List[float],
                      use_pivoting: bool = True,
                      strategy: str = 'partial') -> Tuple[List[List[float]], List[float], Optional[PivotingManager]]:
    """
    Perform forward elimination phase of Gaussian elimination.
    
    Args:
        A: Input matrix
        b: Right-hand side vector
        use_pivoting: Whether to use pivoting
        strategy: Pivoting strategy if used
        
    Returns:
        Tuple containing:
        - Upper triangular matrix
        - Modified right-hand side
        - Pivoting manager (if pivoting used)
    """
    n = len(A)
    # Create working copies
    U = [[A[i][j] for j in range(n)] for i in range(n)]
    y = [b[i] for i in range(n)]
    
    pivoting_manager = PivotingManager(n, strategy) if use_pivoting else None
    if use_pivoting:
        pivoting_manager.set_scaling(U)
    
    for k in range(n-1):
        # Apply pivoting if requested
        if use_pivoting:
            pivot_row, pivot_col = pivoting_manager.find_pivot(U, k)
            pivoting_manager.apply_pivot(U, y, k, pivot_row, pivot_col)
            
        # Check for effective zero pivot
        if abs(U[k][k]) < get_machine_epsilon():
            raise ValueError(f"Zero pivot encountered at step {k}")
            
        # Eliminate entries below pivot
        for i in range(k+1, n):
            factor = U[i][k] / U[k][k]
            U[i][k] = 0.0  # Fill with exact zero
            
            for j in range(k+1, n):
                U[i][j] -= factor * U[k][j]
            y[i] -= factor * y[k]
    
    return U, y, pivoting_manager

def back_substitution(U: List[List[float]], 
                     y: List[float]) -> List[float]:
    """
    Perform back substitution phase of Gaussian elimination.
    
    Args:
        U: Upper triangular matrix
        y: Modified right-hand side
        
    Returns:
        List[float]: Solution vector
    """
    n = len(U)
    x = [0.0] * n
    
    for i in range(n-1, -1, -1):
        if abs(U[i][i]) < get_machine_epsilon():
            raise ValueError(f"Zero diagonal element at index {i}")
            
        x[i] = y[i]
        for j in range(i+1, n):
            x[i] -= U[i][j] * x[j]
        x[i] /= U[i][i]
    
    return x

def gauss_elimination(A: List[List[float]], 
                     b: List[float],
                     use_pivoting: bool = True,
                     strategy: str = 'partial') -> List[float]:
    """
    Solve linear system Ax = b using Gaussian elimination.
    
    Args:
        A: Coefficient matrix
        b: Right-hand side vector
        use_pivoting: Whether to use pivoting
        strategy: Pivoting strategy if used
        
    Returns:
        List[float]: Solution vector
    """
    # Forward elimination
    U, y, pivoting_manager = forward_elimination(A, b, use_pivoting, strategy)
    
    # Back substitution
    x = back_substitution(U, y)
    
    # Apply inverse permutation if needed
    if pivoting_manager and strategy == 'complete':
        x = pivoting_manager.apply_inverse_permutation(x)
    
    return x

def compute_residual(A: List[List[float]], 
                    x: List[float], 
                    b: List[float]) -> List[float]:
    """
    Compute residual r = b - Ax.
    
    Args:
        A: Coefficient matrix
        x: Solution vector
        b: Right-hand side vector
        
    Returns:
        List[float]: Residual vector
    """
    n = len(A)
    r = [b[i] for i in range(n)]
    
    for i in range(n):
        for j in range(n):
            r[i] -= A[i][j] * x[j]
            
    return r

def estimate_error(A: List[List[float]], 
                  x: List[float], 
                  b: List[float]) -> float:
    """
    Estimate relative error in solution using residual.
    
    Args:
        A: Coefficient matrix
        x: Solution vector
        b: Right-hand side vector
        
    Returns:
        float: Estimated relative error
    """
    residual = compute_residual(A, x, b)
    
    # Compute norms
    residual_norm = max(abs(r) for r in residual)
    b_norm = max(abs(bi) for bi in b)
    x_norm = max(abs(xi) for xi in x)
    A_norm = max(sum(abs(A[i][j]) for j in range(len(A))) for i in range(len(A)))
    
    # Estimate condition number using 1-norm
    try:
        A_inv_norm = 1.0 / min(sum(abs(A[i][j]) for j in range(len(A))) for i in range(len(A)))
        cond_A = A_norm * A_inv_norm
        
        # Compute error estimate
        relative_error = (cond_A * residual_norm) / (x_norm * b_norm)
        return relative_error
    except ZeroDivisionError:
        return float('inf')

def determine_matrix_rank(A: List[List[float]], tol: float = None) -> int:
    """
    Determine the rank of a matrix using Gaussian elimination.
    
    Args:
        A: Input matrix
        tol: Tolerance for zero (if None, use machine epsilon)
        
    Returns:
        int: Rank of matrix
    """
    if tol is None:
        tol = get_machine_epsilon()
        
    n = len(A)
    # Create working copy
    U = [[A[i][j] for j in range(n)] for i in range(n)]
    
    # Convert to upper triangular form
    rank = 0
    for k in range(n):
        # Find pivot in current column
        max_val = 0.0
        pivot_row = k
        for i in range(k, n):
            if abs(U[i][k]) > max_val:
                max_val = abs(U[i][k])
                pivot_row = i
                
        # Swap rows if needed
        if pivot_row != k:
            U[k], U[pivot_row] = U[pivot_row], U[k]
            
        # Check if pivot is effectively zero
        if abs(U[k][k]) > tol:
            rank += 1
            # Eliminate entries below pivot
            for i in range(k+1, n):
                factor = U[i][k] / U[k][k]
                for j in range(k, n):
                    U[i][j] -= factor * U[k][j]
                    
    return rank

# Example usage
if __name__ == "__main__":
    # Example 1: Well-conditioned system
    A1 = [
        [4.0, 1.0, -1.0],
        [1.0, 4.0, -1.0],
        [-1.0, -1.0, 4.0]
    ]
    b1 = [6.0, 7.0, 1.0]
    
    try:
        # Solve without pivoting
        x1_no_pivot = gauss_elimination(A1, b1, use_pivoting=False)
        print("\nSolution without pivoting:")
        print(x1_no_pivot)
        
        # Compute and print residual
        r1 = compute_residual(A1, x1_no_pivot, b1)
        print("Residual:")
        print(r1)
        
        # Estimate error
        err1 = estimate_error(A1, x1_no_pivot, b1)
        print(f"Estimated relative error: {err1:.2e}")
        
        # Solve with partial pivoting
        x1_pivot = gauss_elimination(A1, b1, use_pivoting=True, strategy='partial')
        print("\nSolution with partial pivoting:")
        print(x1_pivot)
        
    except ValueError as e:
        print(f"Error: {e}")
    
    # Example 2: Ill-conditioned system (Hilbert matrix)
    n = 5
    A2 = [[1.0/(i + j + 1) for j in range(n)] for i in range(n)]
    b2 = [sum(row) for row in A2]  # Makes x = [1,1,...,1] the exact solution
    
    try:
        # Solve with complete pivoting
        x2 = gauss_elimination(A2, b2, use_pivoting=True, strategy='complete')
        print("\nSolution for Hilbert matrix:")
        print(x2)
        
        # Compute error compared to exact solution
        exact_x2 = [1.0] * n
        err2 = max(abs(x2[i] - exact_x2[i]) for i in range(n))
        print(f"Maximum absolute error: {err2:.2e}")
        
        # Check rank
        rank = determine_matrix_rank(A2)
        print(f"Matrix rank: {rank}")
        
    except ValueError as e:
        print(f"Error: {e}")
    
    # Example 3: Compare pivoting strategies
    import time
    import matplotlib.pyplot as plt
    
    # Function to generate random test matrix
    def generate_test_matrix(n: int) -> Tuple[List[List[float]], List[float]]:
        A = [[np.random.random() for _ in range(n)] for _ in range(n)]
        x_exact = [np.random.random() for _ in range(n)]
        b = [sum(A[i][j] * x_exact[j] for j in range(n)) for i in range(n)]
        return A, b, x_exact
    
    # Test different sizes
    sizes = [10, 20, 50, 100]
    times_no_pivot = []
    times_partial = []
    times_complete = []
    errors_no_pivot = []
    errors_partial = []
    errors_complete = []
    
    for n in sizes:
        A, b, x_exact = generate_test_matrix(n)
        
        # No pivoting
        start = time.time()
        x_no_pivot = gauss_elimination(A, b, use_pivoting=False)
        times_no_pivot.append(time.time() - start)
        errors_no_pivot.append(max(abs(x_no_pivot[i] - x_exact[i]) for i in range(n)))
        
        # Partial pivoting
        start = time.time()
        x_partial = gauss_elimination(A, b, use_pivoting=True, strategy='partial')
        times_partial.append(time.time() - start)
        errors_partial.append(max(abs(x_partial[i] - x_exact[i]) for i in range(n)))
        
        # Complete pivoting
        start = time.time()
        x_complete = gauss_elimination(A, b, use_pivoting=True, strategy='complete')
        times_complete.append(time.time() - start)
        errors_complete.append(max(abs(x_complete[i] - x_exact[i]) for i in range(n)))
    
    # Plot results
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot computation times
    ax1.plot(sizes, times_no_pivot, 'b.-', label='No pivoting')
    ax1.plot(sizes, times_partial, 'r.-', label='Partial pivoting')
    ax1.plot(sizes, times_complete, 'g.-', label='Complete pivoting')
    ax1.set_xlabel('Matrix size')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('Computation Time vs Matrix Size')
    ax1.grid(True)
    ax1.legend()
    
    # Plot errors
    ax2.semilogy(sizes, errors_no_pivot, 'b.-', label='No pivoting')
    ax2.semilogy(sizes, errors_partial, 'r.-', label='Partial pivoting')
    ax2.semilogy(sizes, errors_complete, 'g.-', label='Complete pivoting')
    ax2.set_xlabel('Matrix size')
    ax2.set_ylabel('Maximum absolute error')
    ax2.set_title('Error vs Matrix Size')
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    plt.show()