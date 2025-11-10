"""
Implementation of pivoting strategies for linear system solvers.
Includes column pivoting and complete pivoting with permutation tracking.
"""

from typing import List, Tuple, Optional
import numpy as np
from basics.rechnerarithmetik import get_machine_epsilon

def find_pivot_element(A: List[List[float]], 
                      k: int, 
                      n: int,
                      strategy: str = 'partial') -> Tuple[int, int]:
    """
    Find pivot element for given elimination step.
    
    Args:
        A: Matrix to analyze
        k: Current elimination step
        n: Matrix dimension
        strategy: Pivoting strategy ('partial' or 'complete')
    
    Returns:
        Tuple containing:
        - Row index of pivot
        - Column index of pivot (only for complete pivoting)
    """
    if strategy == 'partial':
        # Find largest element in current column k
        pivot_row = k + max(range(n-k), key=lambda i: abs(A[i+k][k]))
        return pivot_row, k
    
    elif strategy == 'complete':
        # Find largest element in remaining submatrix
        max_val = 0.0
        pivot_row = k
        pivot_col = k
        
        for i in range(k, n):
            for j in range(k, n):
                if abs(A[i][j]) > max_val:
                    max_val = abs(A[i][j])
                    pivot_row = i
                    pivot_col = j
                    
        return pivot_row, pivot_col
    
    else:
        raise ValueError(f"Unknown pivoting strategy: {strategy}")

def swap_rows(A: List[List[float]], 
              b: List[float], 
              i: int, 
              j: int) -> None:
    """
    Swap rows i and j in matrix A and vector b in-place.
    
    Args:
        A: Matrix to modify
        b: Right-hand side vector to modify
        i, j: Row indices to swap
    """
    if i != j:
        A[i], A[j] = A[j], A[i]
        b[i], b[j] = b[j], b[i]

def swap_columns(A: List[List[float]], 
                i: int, 
                j: int,
                col_perm: List[int]) -> None:
    """
    Swap columns i and j in matrix A in-place and track permutation.
    
    Args:
        A: Matrix to modify
        i, j: Column indices to swap
        col_perm: List tracking column permutations
    """
    if i != j:
        for row in A:
            row[i], row[j] = row[j], row[i]
        col_perm[i], col_perm[j] = col_perm[j], col_perm[i]

class PivotingManager:
    """Class to manage pivoting operations and permutation tracking."""
    
    def __init__(self, n: int, strategy: str = 'partial'):
        """
        Initialize pivoting manager.
        
        Args:
            n: Matrix dimension
            strategy: Pivoting strategy ('partial' or 'complete')
        """
        self.n = n
        self.strategy = strategy
        self.row_perm = list(range(n))  # Track row permutations
        self.col_perm = list(range(n))  # Track column permutations (for complete pivoting)
        self.scaling_factors = None  # For scaled pivoting
        
    def set_scaling(self, A: List[List[float]]) -> None:
        """
        Compute scaling factors for scaled pivoting.
        
        Args:
            A: Input matrix
        """
        self.scaling_factors = [max(abs(A[i][j]) for j in range(self.n)) 
                              for i in range(self.n)]
    
    def find_pivot(self, 
                  A: List[List[float]], 
                  k: int,
                  use_scaling: bool = False) -> Tuple[int, int]:
        """
        Find pivot element considering scaling if requested.
        
        Args:
            A: Matrix to analyze
            k: Current elimination step
            use_scaling: Whether to use scaled pivoting
            
        Returns:
            Tuple containing pivot indices
        """
        if not use_scaling:
            return find_pivot_element(A, k, self.n, self.strategy)
            
        # For scaled pivoting, compare elements divided by scaling factors
        if self.strategy == 'partial':
            pivot_row = k + max(range(self.n-k),
                              key=lambda i: abs(A[i+k][k])/self.scaling_factors[i+k])
            return pivot_row, k
        else:
            max_val = 0.0
            pivot_row = k
            pivot_col = k
            
            for i in range(k, self.n):
                for j in range(k, self.n):
                    scaled_val = abs(A[i][j])/self.scaling_factors[i]
                    if scaled_val > max_val:
                        max_val = scaled_val
                        pivot_row = i
                        pivot_col = j
                        
            return pivot_row, pivot_col
    
    def apply_pivot(self, 
                   A: List[List[float]], 
                   b: Optional[List[float]], 
                   k: int,
                   pivot_row: int,
                   pivot_col: int) -> None:
        """
        Apply pivoting operations and update permutation tracking.
        
        Args:
            A: Matrix to modify
            b: Right-hand side vector (optional)
            k: Current elimination step
            pivot_row, pivot_col: Pivot indices
        """
        # Swap rows if needed
        if pivot_row != k:
            swap_rows(A, b, k, pivot_row) if b is not None else swap_rows(A, [], k, pivot_row)
            self.row_perm[k], self.row_perm[pivot_row] = \
                self.row_perm[pivot_row], self.row_perm[k]
        
        # Swap columns if needed (complete pivoting)
        if self.strategy == 'complete' and pivot_col != k:
            swap_columns(A, k, pivot_col, self.col_perm)
    
    def get_permutations(self) -> Tuple[List[int], List[int]]:
        """
        Get current permutation vectors.
        
        Returns:
            Tuple containing:
            - Row permutation vector
            - Column permutation vector
        """
        return self.row_perm, self.col_perm
    
    def apply_inverse_permutation(self, x: List[float]) -> List[float]:
        """
        Apply inverse permutation to solution vector (for complete pivoting).
        
        Args:
            x: Solution vector
            
        Returns:
            List[float]: Permuted solution vector
        """
        if self.strategy != 'complete':
            return x
            
        # Create inverse permutation
        n = len(x)
        inv_perm = [0] * n
        for i in range(n):
            inv_perm[self.col_perm[i]] = i
            
        # Apply inverse permutation
        return [x[inv_perm[i]] for i in range(n)]

# Example usage
if __name__ == "__main__":
    # Example matrix and right-hand side
    A = [
        [0.0, 2.0, 1.0],
        [1.0, 0.0, 3.0],
        [4.0, 2.0, 1.0]
    ]
    b = [1.0, 2.0, 3.0]
    n = len(A)
    
    # Create pivoting manager
    manager = PivotingManager(n, strategy='complete')
    
    # Optional: Set scaling
    manager.set_scaling(A)
    
    # Simulate elimination steps
    for k in range(n-1):
        # Find and apply pivot
        pivot_row, pivot_col = manager.find_pivot(A, k, use_scaling=True)
        manager.apply_pivot(A, b, k, pivot_row, pivot_col)
        
        print(f"\nStep {k+1}:")
        print(f"Pivot position: ({pivot_row}, {pivot_col})")
        print("Matrix A:")
        for row in A:
            print(row)
        print("Vector b:", b)
    
    # Get final permutations
    row_perm, col_perm = manager.get_permutations()
    print("\nFinal permutations:")
    print("Row permutation:", row_perm)
    print("Column permutation:", col_perm)
