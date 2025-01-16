"""
Implementation of Gaussian elimination with and without pivoting.
Includes forward elimination, back substitution, and error analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
import time
from basics.rechnerarithmetik import get_machine_epsilon
from pivotisierung import PivotingManager

def forward_elimination(A, b, use_pivoting=True, strategy='partial'):
    """
    Perform forward elimination phase of Gaussian elimination.
    Converts matrix A to upper triangular form while updating b.
    
    Args:
        A: Input matrix
        b: Right-hand side vector
        use_pivoting: Whether to use pivoting
        strategy: Pivoting strategy if used
        
    Returns:
        Tuple of (upper triangular matrix, modified right-hand side, pivoting manager)
    """
    n = len(A)
    # Create working copies to preserve originals
    U = [[A[i][j] for j in range(n)] for i in range(n)]
    y = [b[i] for i in range(n)]
    
    # Initialize pivoting if requested
    pivoting_manager = PivotingManager(n, strategy) if use_pivoting else None
    if use_pivoting:
        pivoting_manager.set_scaling(U)
    
    for k in range(n-1):
        # Apply pivoting if requested
        if use_pivoting:
            pivot_row, pivot_col = pivoting_manager.find_pivot(U, k)
            pivoting_manager.apply_pivot(U, y, k, pivot_row, pivot_col)
            
        # Check for numerical stability
        if abs(U[k][k]) < get_machine_epsilon():
            raise ValueError(f"Zero pivot encountered at step {k}")
            
        # Eliminate entries below pivot
        for i in range(k+1, n):
            factor = U[i][k] / U[k][k]
            U[i][k] = 0.0  # Exact zero for stability
            
            # Update row
            for j in range(k+1, n):
                U[i][j] -= factor * U[k][j]
            y[i] -= factor * y[k]
    
    return U, y, pivoting_manager

def back_substitution(U, y):
    """
    Perform back substitution phase of Gaussian elimination.
    Solves Ux = y where U is upper triangular.
    
    Args:
        U: Upper triangular matrix
        y: Modified right-hand side
        
    Returns:
        Solution vector x
    """
    n = len(U)
    x = [0.0] * n
    
    # Solve from bottom to top
    for i in range(n-1, -1, -1):
        # Check diagonal element
        if abs(U[i][i]) < get_machine_epsilon():
            raise ValueError(f"Zero diagonal element at index {i}")
            
        # Compute solution component
        x[i] = y[i]
        for j in range(i+1, n):
            x[i] -= U[i][j] * x[j]
        x[i] /= U[i][i]
    
    return x

def gauss_elimination(A, b, use_pivoting=True, strategy='partial'):
    """
    Solve linear system Ax = b using Gaussian elimination.
    Combines forward elimination and back substitution phases.
    
    Args:
        A: Coefficient matrix
        b: Right-hand side vector
        use_pivoting: Whether to use pivoting
        strategy: Pivoting strategy if used
        
    Returns:
        Solution vector x
    """
    # Perform forward elimination
    U, y, pivoting_manager = forward_elimination(A, b, use_pivoting, strategy)
    
    # Solve triangular system
    x = back_substitution(U, y)
    
    # Apply inverse permutation for complete pivoting
    if pivoting_manager and strategy == 'complete':
        x = pivoting_manager.apply_inverse_permutation(x)
    
    return x

def compute_residual(A, x, b):
    """
    Compute residual r = b - Ax.
    Measures how well solution satisfies original system.
    
    Args:
        A: Coefficient matrix
        x: Solution vector
        b: Right-hand side vector
        
    Returns:
        Residual vector
    """
    n = len(A)
    r = [b[i] for i in range(n)]
    
    # Compute matrix-vector product and subtract
    for i in range(n):
        for j in range(n):
            r[i] -= A[i][j] * x[j]
            
    return r

def estimate_error(A, x, b):
    """
    Estimate relative error in solution using residual.
    Uses condition number and residual for error bound.
    
    Args:
        A: Coefficient matrix
        x: Solution vector
        b: Right-hand side vector
        
    Returns:
        Estimated relative error
    """
    residual = compute_residual(A, x, b)
    
    # Compute various norms
    residual_norm = max(abs(r) for r in residual)
    b_norm = max(abs(bi) for bi in b)
    x_norm = max(abs(xi) for xi in x)
    A_norm = max(sum(abs(A[i][j]) for j in range(len(A))) for i in range(len(A)))
    
    # Estimate condition number using 1-norm
    try:
        # Estimate inverse norm (rough approximation)
        A_inv_norm = 1.0 / min(sum(abs(A[i][j]) for j in range(len(A))) 
                              for i in range(len(A)))
        cond_A = A_norm * A_inv_norm
        
        # Compute error estimate
        relative_error = (cond_A * residual_norm) / (x_norm * b_norm)
        return relative_error
    except ZeroDivisionError:
        return float('inf')

def determine_matrix_rank(A, tol=None):
    """
    Determine the rank of a matrix using Gaussian elimination.
    Counts number of non-zero pivots after elimination.
    
    Args:
        A: Input matrix
        tol: Tolerance for zero (if None, use machine epsilon)
        
    Returns:
        Rank of matrix
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
            
        # Check if pivot is significant
        if abs(U[k][k]) > tol:
            rank += 1
            # Eliminate entries below pivot
            for i in range(k+1, n):
                factor = U[i][k] / U[k][k]
                for j in range(k, n):
                    U[i][j] -= factor * U[k][j]
                    
    return rank

def analyze_pivoting_strategies(sizes=[10, 20, 50, 100], plot_results=True):
    """
    Compare different pivoting strategies for various matrix sizes.
    Analyzes computation time and solution accuracy.
    
    Args:
        sizes: List of matrix sizes to test
        plot_results: Whether to plot comparison results
    """
    # Initialize result storage
    times_no_pivot = []
    times_partial = []
    times_complete = []
    errors_no_pivot = []
    errors_partial = []
    errors_complete = []
    
    for n in sizes:
        # Generate random test matrix
        A = np.random.rand(n, n).tolist()
        x_exact = np.random.rand(n).tolist()
        b = [sum(A[i][j] * x_exact[j] for j in range(n)) for i in range(n)]
        
        # Test each pivoting strategy
        # No pivoting
        start = time.time()
        try:
            x_no_pivot = gauss_elimination(A, b, use_pivoting=False)
            error = max(abs(x_no_pivot[i] - x_exact[i]) for i in range(n))
        except ValueError:
            error = float('inf')
        times_no_pivot.append(time.time() - start)
        errors_no_pivot.append(error)
        
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
    
    if plot_results:
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
        
    return {
        'times': {
            'no_pivot': times_no_pivot,
            'partial': times_partial,
            'complete': times_complete
        },
        'errors': {
            'no_pivot': errors_no_pivot,
            'partial': errors_partial,
            'complete': errors_complete
        }
    }

# Example usage
if __name__ == "__main__":
    # Example 1: Well-conditioned system
    A1 = [
        [4.0, 1.0, -1.0],
        [1.0, 4.0, -1.0],
        [-1.0, -1.0, 4.0]
    ]
    b1 = [6.0, 7.0, 1.0]
    
    print("Example 1: Well-conditioned system")
    try:
        # Solve without pivoting
        x1_no_pivot = gauss_elimination(A1, b1, use_pivoting=False)
        print("\nSolution without pivoting:", x1_no_pivot)
        r1 = compute_residual(A1, x1_no_pivot, b1)
        print("Residual:", r1)
        err1 = estimate_error(A1, x1_no_pivot, b1)
        print(f"Estimated relative error: {err1:.2e}")
        
        # Solve with partial pivoting
        x1_pivot = gauss_elimination(A1, b1, use_pivoting=True, strategy='partial')
        print("\nSolution with partial pivoting:", x1_pivot)
        
    except ValueError as e:
        print(f"Error: {e}")
    
    # Example 2: Ill-conditioned Hilbert matrix
    print("\nExample 2: Hilbert matrix")
    n = 5
    A2 = [[1.0/(i + j + 1) for j in range(n)] for i in range(n)]
    b2 = [sum(row) for row in A2]  # Makes x = [1,1,...,1] the solution
    
    try:
        # Solve with complete pivoting
        x2 = gauss_elimination(A2, b2, use_pivoting=True, strategy='complete')
        print("\nSolution:", x2)
        exact_x2 = [1.0] * n
        err2 = max(abs(x2[i] - exact_x2[i]) for i in range(n))
        print(f"Maximum absolute error: {err2:.2e}")
        rank = determine_matrix_rank(A2)
        print(f"Matrix rank: {rank}")
        
    except ValueError as e:
        print(f"Error: {e}")
    
    # Example 3: Compare pivoting strategies
    print("\nExample 3: Comparing pivoting strategies")
    results = analyze_pivoting_strategies()
