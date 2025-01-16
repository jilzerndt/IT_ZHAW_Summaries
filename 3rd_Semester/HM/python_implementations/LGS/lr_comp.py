"""
Implementation of LR (LU) decomposition for solving linear systems.
Includes pivoting, determinant calculation, and matrix inversion functionality.
"""

import numpy as np
import matplotlib.pyplot as plt
import time
from basics.rechnerarithmetik import get_machine_epsilon
from pivotisierung import PivotingManager

def lr_decomposition(A, use_pivoting=True):
    """
    Compute LR decomposition of matrix A.
    A = LR where L is lower triangular and R is upper triangular.
    
    Args:
        A: Input matrix (as nested list or numpy array)
        use_pivoting: Whether to use pivoting for numerical stability
        
    Returns:
        Tuple (L, R, pivoting_manager): 
        - L: Lower triangular matrix
        - R: Upper triangular matrix
        - pivoting_manager: Manager tracking row permutations if pivoting used
    """
    # Convert input to numpy array for easier manipulation
    A = np.array(A, dtype=float)
    n = len(A)
    
    # Initialize L and R matrices
    # L starts as identity matrix
    L = np.eye(n)
    # R starts as a copy of A
    R = A.copy()
    
    # Initialize pivoting manager if requested
    pivoting_manager = PivotingManager(n, 'partial') if use_pivoting else None
    
    # Perform elimination column by column
    for k in range(n-1):
        # Apply pivoting if requested
        if use_pivoting:
            pivot_row, _ = pivoting_manager.find_pivot(R, k)
            if pivot_row != k:
                # Swap rows in R
                R[k], R[pivot_row] = R[pivot_row].copy(), R[k].copy()
                # Swap corresponding rows in L up to column k
                L[k, :k], L[pivot_row, :k] = L[pivot_row, :k].copy(), L[k, :k].copy()
                
        # Check for zero pivot
        if abs(R[k,k]) < get_machine_epsilon():
            raise ValueError(f"Zero pivot encountered at step {k}")
            
        # Compute multipliers and eliminate below diagonal
        for i in range(k+1, n):
            # Compute and store multiplier in L
            L[i,k] = R[i,k] / R[k,k]
            # Update row of R using multiplier
            R[i,k:] -= L[i,k] * R[k,k:]
            
    return L.tolist(), R.tolist(), pivoting_manager

def forward_substitution(L, b):
    """
    Solve Ly = b using forward substitution.
    Used for systems where L is lower triangular.
    
    Args:
        L: Lower triangular matrix
        b: Right-hand side vector
        
    Returns:
        Solution vector y
    """
    L = np.array(L)
    b = np.array(b)
    n = len(b)
    y = np.zeros(n)
    
    # Solve system row by row
    for i in range(n):
        # Compute sum of known terms
        known_sum = np.dot(L[i,:i], y[:i])
        # Solve for current variable
        y[i] = (b[i] - known_sum) / L[i,i]
        
    return y.tolist()

def back_substitution(R, y):
    """
    Solve Rx = y using back substitution.
    Used for systems where R is upper triangular.
    
    Args:
        R: Upper triangular matrix
        y: Right-hand side vector
        
    Returns:
        Solution vector x
    """
    R = np.array(R)
    y = np.array(y)
    n = len(y)
    x = np.zeros(n)
    
    # Solve system from bottom to top
    for i in range(n-1, -1, -1):
        # Check for zero diagonal element
        if abs(R[i,i]) < get_machine_epsilon():
            raise ValueError(f"Zero diagonal element at index {i}")
            
        # Compute sum of known terms
        known_sum = np.dot(R[i,i+1:], x[i+1:])
        # Solve for current variable
        x[i] = (y[i] - known_sum) / R[i,i]
        
    return x.tolist()

def solve_lr(L, R, b, pivoting_manager=None):
    """
    Solve system LRx = b using forward and back substitution.
    
    Args:
        L: Lower triangular matrix from LR decomposition
        R: Upper triangular matrix from LR decomposition
        b: Right-hand side vector
        pivoting_manager: Manager tracking row permutations
        
    Returns:
        Solution vector x
    """
    # Apply row permutation to b if pivoting was used
    if pivoting_manager:
        row_perm, _ = pivoting_manager.get_permutations()
        b = [b[row_perm[i]] for i in range(len(b))]
    
    # First solve Ly = b (forward substitution)
    y = forward_substitution(L, b)
    
    # Then solve Rx = y (back substitution)
    x = back_substitution(R, y)
    
    return x

def compute_determinant(R):
    """
    Compute determinant from LR decomposition.
    For a triangular matrix, determinant is product of diagonal elements.
    
    Args:
        R: Upper triangular matrix from LR decomposition
        
    Returns:
        Determinant value
    """
    R = np.array(R)
    return np.prod(np.diag(R))

def invert_matrix(A, use_pivoting=True):
    """
    Compute matrix inverse using LR decomposition.
    Solves AX = I column by column.
    
    Args:
        A: Input matrix
        use_pivoting: Whether to use pivoting
        
    Returns:
        Inverse matrix
    """
    n = len(A)
    
    # Compute LR decomposition once (reuse for all columns)
    L, R, pivoting_manager = lr_decomposition(A, use_pivoting)
    
    # Create identity matrix for right-hand sides
    I = np.eye(n)
    
    # Solve for each column of inverse
    A_inv = []
    for j in range(n):
        # Solve for jth column using jth column of identity matrix
        col = solve_lr(L, R, I[j].tolist(), pivoting_manager)
        A_inv.append(col)
    
    # Convert to proper matrix format (transpose result)
    return np.array(A_inv).T.tolist()

# Example usage and testing
if __name__ == "__main__":
    # Test matrix - tridiagonal system
    A = np.array([
        [4.0, -1.0, 0.0, -1.0],
        [-1.0, 4.0, -1.0, 0.0],
        [0.0, -1.0, 4.0, -1.0],
        [-1.0, 0.0, -1.0, 4.0]
    ])
    b = np.array([1.0, 5.0, 0.0, 2.0])
    
    try:
        # Compute and display LR decomposition
        L, R, piv = lr_decomposition(A, use_pivoting=True)
        print("Lower triangular matrix L:")
        print(np.array(L))
        print("\nUpper triangular matrix R:")
        print(np.array(R))
        
        # Solve system and display solution
        x = solve_lr(L, R, b.tolist(), piv)
        print("\nSolution x:")
        print(x)
        
        # Compute and verify determinant
        det = compute_determinant(R)
        print(f"\nDeterminant: {det}")
        
        # Compute and verify inverse
        A_inv = invert_matrix(A.tolist())
        print("\nInverse matrix:")
        print(np.array(A_inv))
        
        # Verify solution
        residual = np.linalg.norm(A @ np.array(x) - b)
        print(f"\nResidual norm: {residual}")
        
    except ValueError as e:
        print(f"Error: {e}")
