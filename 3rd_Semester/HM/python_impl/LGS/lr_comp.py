"""
Implementation of LR (LU) decomposition for solving linear systems.
"""

from typing import List, Tuple, Optional
import numpy as np
from basics.rechnerarithmetik import get_machine_epsilon
from pivotisierung import PivotingManager

def lr_decomposition(A: List[List[float]], 
                    use_pivoting: bool = True) -> Tuple[List[List[float]], 
                                                      List[List[float]], 
                                                      Optional[PivotingManager]]:
    """
    Compute LR decomposition of matrix A.
    
    Args:
        A: Input matrix
        use_pivoting: Whether to use pivoting
        
    Returns:
        Tuple containing:
        - Lower triangular matrix L
        - Upper triangular matrix R
        - Pivoting manager if pivoting used
    """
    n = len(A)
    # Initialize L and R
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    R = [[A[i][j] for j in range(n)] for i in range(n)]
    
    pivoting_manager = PivotingManager(n, 'partial') if use_pivoting else None
    
    for k in range(n-1):
        # Apply pivoting if requested
        if use_pivoting:
            pivot_row, _ = pivoting_manager.find_pivot(R, k)
            if pivot_row != k:
                # Swap rows in R
                R[k], R[pivot_row] = R[pivot_row], R[k]
                # Swap rows in L up to k
                for j in range(k):
                    L[k][j], L[pivot_row][j] = L[pivot_row][j], L[k][j]
                    
        # Check for effectively zero pivot
        if abs(R[k][k]) < get_machine_epsilon():
            raise ValueError(f"Zero pivot encountered at step {k}")
            
        # Compute multipliers and eliminate
        for i in range(k+1, n):
            L[i][k] = R[i][k] / R[k][k]
            R[i][k] = 0.0
            for j in range(k+1, n):
                R[i][j] -= L[i][k] * R[k][j]
                
    return L, R, pivoting_manager

def forward_substitution(L: List[List[float]], 
                        b: List[float]) -> List[float]:
    """
    Solve Ly = b using forward substitution.
    
    Args:
        L: Lower triangular matrix
        b: Right-hand side vector
        
    Returns:
        List[float]: Solution vector y
    """
    n = len(L)
    y = [0.0] * n
    
    for i in range(n):
        y[i] = b[i]
        for j in range(i):
            y[i] -= L[i][j] * y[j]
            
    return y

def back_substitution(R: List[List[float]], 
                     y: List[float]) -> List[float]:
    """
    Solve Rx = y using back substitution.
    
    Args:
        R: Upper triangular matrix
        y: Right-hand side vector
        
    Returns:
        List[float]: Solution vector x
    """
    n = len(R)
    x = [0.0] * n
    
    for i in range(n-1, -1, -1):
        if abs(R[i][i]) < get_machine_epsilon():
            raise ValueError(f"Zero diagonal element at index {i}")
            
        x[i] = y[i]
        for j in range(i+1, n):
            x[i] -= R[i][j] * x[j]
        x[i] /= R[i][i]
        
    return x

def solve_lr(L: List[List[float]], 
             R: List[List[float]], 
             b: List[float],
             pivoting_manager: Optional[PivotingManager] = None) -> List[float]:
    """
    Solve system LRx = b using forward and back substitution.
    
    Args:
        L: Lower triangular matrix
        R: Upper triangular matrix
        b: Right-hand side vector
        pivoting_manager: Pivoting manager if pivoting was used
        
    Returns:
        List[float]: Solution vector x
    """
    # Apply row permutation to b if needed
    if pivoting_manager:
        row_perm, _ = pivoting_manager.get_permutations()
        b = [b[row_perm[i]] for i in range(len(b))]
    
    # Solve Ly = b
    y = forward_substitution(L, b)
    
    # Solve Rx = y
    x = back_substitution(R, y)
    
    return x

def lr_solve(A: List[List[float]], 
             b: List[float],
             use_pivoting: bool = True) -> List[float]:
    """
    Solve linear system Ax = b using LR decomposition.
    
    Args:
        A: Coefficient matrix
        b: Right-hand side vector
        use_pivoting: Whether to use pivoting
        
    Returns:
        List[float]: Solution vector x
    """
    # Compute LR decomposition
    L, R, pivoting_manager = lr_decomposition(A, use_pivoting)
    
    # Solve system
    return solve_lr(L, R, b, pivoting_manager)

def compute_determinant(R: List[List[float]]) -> float:
    """
    Compute determinant from LR decomposition.
    
    Args:
        R: Upper triangular matrix from LR decomposition
        
    Returns:
        float: Determinant of original matrix
    """
    return np.prod([R[i][i] for i in range(len(R))])

def invert_matrix(A: List[List[float]], 
                 use_pivoting: bool = True) -> List[List[float]]:
    """
    Compute matrix inverse using LR decomposition.
    
    Args:
        A: Input matrix
        use_pivoting: Whether to use pivoting
        
    Returns:
        List[List[float]]: Inverse matrix
    """
    n = len(A)
    # Compute LR decomposition once
    L, R, pivoting_manager = lr_decomposition(A, use_pivoting)
    
    # Create identity matrix
    I = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    
    # Solve for each column of inverse
    A_inv = []
    for j in range(n):
        # Solve for jth column
        col = solve_lr(L, R, I[j], pivoting_manager)
        A_inv.append(col)
        
    # Transpose to get correct format
    return [[A_inv[j][i] for j in range(n)] for i in range(n)]

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
    
    try:
        # Compute LR decomposition
        L1, R1, piv1 = lr_decomposition(A1, use_pivoting=True)
        
        print("Matrix L:")
        for row in L1:
            print([f"{x:8.4f}" for x in row])
            
        print("\nMatrix R:")
        for row in R1:
            print([f"{x:8.4f}" for x in row])
            
        # Solve system
        x1 = solve_lr(L1, R1, b1, piv1)
        print("\nSolution:")
        print([f"{x:8.4f}" for x in x1])
        
        # Compute determinant
        det1 = compute_determinant(R1)
        print(f"\nDeterminant: {det1:.4f}")
        
        # Compute inverse
        A1_inv = invert_matrix(A1)
        print("\nInverse matrix:")
        for row in A1_inv:
            print([f"{x:8.4f}" for x in row])
            
        # Verify inverse
        print("\nVerification (A * A^-1 should be identity):")
        identity = [[sum(A1[i][k] * A1_inv[k][j] for k in range(len(A1)))
                    for j in range(len(A1))] for i in range(len(A1))]
        for row in identity:
            print([f"{x:8.4f}" for x in row])
            
    except ValueError as e:
        print(f"Error: {e}")
        
    # Example 2: Compare with and without pivoting
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
    
    # Test matrices of different sizes and condition numbers
    sizes = [5, 10, 20]
    conditions = [1.0, 1e3, 1e6]
    
    print("\nComparison of pivoting strategies:")
    print("=" * 60)
    print(f"{'Size':>5} {'Condition':>12} {'Strategy':>12} {'Error':>12}")
    print("-" * 60)
    
    for n in sizes:
        for cond in conditions:
            A = generate_test_matrix(n, cond)
            x_exact = [1.0] * n  # Use [1,1,...,1] as exact solution
            b = [sum(A[i][j] * x_exact[j] for j in range(n)) for i in range(n)]
            
            try:
                # Without pivoting
                x_no_pivot = lr_solve(A, b, use_pivoting=False)
                err_no_pivot = max(abs(x_no_pivot[i] - x_exact[i]) 
                                 for i in range(n))
                print(f"{n:5d} {cond:12.1e} {'No pivot':>12} {err_no_pivot:12.2e}")
                
                # With pivoting
                x_pivot = lr_solve(A, b, use_pivoting=True)
                err_pivot = max(abs(x_pivot[i] - x_exact[i]) 
                              for i in range(n))
                print(f"{n:5d} {cond:12.1e} {'Pivot':>12} {err_pivot:12.2e}")
                
            except ValueError as e:
                print(f"{n:5d} {cond:12.1e} {'Failed':>12} {str(e)}")
                
    # Example 3: Solve multiple right-hand sides efficiently
    n = 100
    A3 = generate_test_matrix(n, 10.0)
    num_rhs = 5
    B3 = [[np.random.random() for _ in range(num_rhs)] for _ in range(n)]
    
    print("\nSolving multiple right-hand sides:")
    print(f"Matrix size: {n}x{n}")
    print(f"Number of right-hand sides: {num_rhs}")
    
    # Compute LR decomposition once
    import time
    start_time = time.time()
    L3, R3, piv3 = lr_decomposition(A3, use_pivoting=True)
    decomp_time = time.time() - start_time
    
    print(f"LR decomposition time: {decomp_time:.4f} seconds")
    
    # Solve for each right-hand side
    start_time = time.time()
    X3 = []
    for j in range(num_rhs):
        b = [B3[i][j] for i in range(n)]
        x = solve_lr(L3, R3, b, piv3)
        X3.append(x)
    solve_time = time.time() - start_time
    
    print(f"Average solve time per right-hand side: {solve_time/num_rhs:.4f} seconds")

        
    