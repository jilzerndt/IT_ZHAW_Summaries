"""
Implementation of pivoting strategies for linear system solvers.
Includes column pivoting and complete pivoting with permutation tracking.
"""

import numpy as np
from basics.rechnerarithmetik import get_machine_epsilon

def find_pivot_element(A, k, n, strategy='partial'):
    """
    Find pivot element for given elimination step.
    For partial pivoting, searches only current column.
    For complete pivoting, searches entire remaining submatrix.
    
    Args:
        A: Matrix to analyze
        k: Current elimination step
        n: Matrix dimension
        strategy: Pivoting strategy ('partial' or 'complete')
    
    Returns:
        Tuple of pivot indices (row, column)
    """
    if strategy == 'partial':
        # Find largest absolute value in current column k
        pivot_row = k + max(range(n-k), key=lambda i: abs(A[i+k][k]))
        return pivot_row, k
    
    elif strategy == 'complete':
        # Find largest absolute value in remaining submatrix
        max_val = 0.0
        pivot_row = k
        pivot_col = k
        
        # Search entire submatrix k:n × k:n
        for i in range(k, n):
            for j in range(k, n):
                if abs(A[i][j]) > max_val:
                    max_val = abs(A[i][j])
                    pivot_row = i
                    pivot_col = j
                    
        return pivot_row, pivot_col
    
    else:
        raise ValueError(f"Unknown pivoting strategy: {strategy}")

def swap_rows(A, b, i, j):
    """
    Swap rows i and j in matrix A and vector b in-place.
    Used for row permutations during pivoting.
    
    Args:
        A: Matrix to modify
        b: Right-hand side vector to modify
        i, j: Row indices to swap
    """
    if i != j:  # Only swap if indices are different
        A[i], A[j] = A[j], A[i]
        if b:  # Only swap b if it exists
            b[i], b[j] = b[j], b[i]

def swap_columns(A, i, j, col_perm):
    """
    Swap columns i and j in matrix A and track permutation.
    Used for column permutations in complete pivoting.
    
    Args:
        A: Matrix to modify
        i, j: Column indices to swap
        col_perm: List tracking column permutations
    """
    if i != j:
        # Swap columns element by element
        for row in A:
            row[i], row[j] = row[j], row[i]
        # Update permutation tracking
        col_perm[i], col_perm[j] = col_perm[j], col_perm[i]

class PivotingManager:
    """
    Class to manage pivoting operations and permutation tracking.
    Supports partial and complete pivoting with optional scaling.
    """
    
    def __init__(self, n, strategy='partial'):
        """
        Initialize pivoting manager.
        Sets up permutation tracking and optional scaling.
        
        Args:
            n: Matrix dimension
            strategy: Pivoting strategy ('partial' or 'complete')
        """
        self.n = n
        self.strategy = strategy
        # Initialize permutation trackers
        self.row_perm = list(range(n))  # Track row swaps
        self.col_perm = list(range(n))  # Track column swaps
        self.scaling_factors = None      # For scaled pivoting
        
    def set_scaling(self, A):
        """
        Compute scaling factors for scaled pivoting.
        Uses maximum absolute value in each row as scaling factor.
        
        Args:
            A: Input matrix
        """
        # For each row, find largest absolute value
        self.scaling_factors = [max(abs(A[i][j]) for j in range(self.n)) 
                              for i in range(self.n)]
    
    def find_pivot(self, A, k, use_scaling=False):
        """
        Find pivot element considering scaling if requested.
        Scaling helps prevent issues with widely varying matrix elements.
        
        Args:
            A: Matrix to analyze
            k: Current elimination step
            use_scaling: Whether to use scaled pivoting
            
        Returns:
            Tuple of pivot indices (row, column)
        """
        if not use_scaling:
            return find_pivot_element(A, k, self.n, self.strategy)
            
        # For scaled pivoting, compare elements divided by scaling factors
        if self.strategy == 'partial':
            # Find largest scaled element in column k
            pivot_row = k + max(range(self.n-k),
                              key=lambda i: abs(A[i+k][k])/self.scaling_factors[i+k])
            return pivot_row, k
        else:
            # Find largest scaled element in submatrix
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
    
    def apply_pivot(self, A, b, k, pivot_row, pivot_col):
        """
        Apply pivoting operations and update permutation tracking.
        Performs necessary row and column swaps.
        
        Args:
            A: Matrix to modify
            b: Right-hand side vector (can be None)
            k: Current elimination step
            pivot_row, pivot_col: Pivot indices
        """
        # Swap rows if needed
        if pivot_row != k:
            swap_rows(A, b, k, pivot_row)
            self.row_perm[k], self.row_perm[pivot_row] = \
                self.row_perm[pivot_row], self.row_perm[k]
        
        # Swap columns if using complete pivoting
        if self.strategy == 'complete' and pivot_col != k:
            swap_columns(A, k, pivot_col, self.col_perm)
    
    def get_permutations(self):
        """
        Get current permutation vectors.
        Used to track all row and column swaps.
        
        Returns:
            Tuple of (row permutation, column permutation)
        """
        return self.row_perm, self.col_perm
    
    def apply_inverse_permutation(self, x):
        """
        Apply inverse permutation to solution vector.
        Necessary for complete pivoting to get correct solution order.
        
        Args:
            x: Solution vector
            
        Returns:
            Permuted solution vector
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

def display_matrix(A, b=None, title="Matrix"):
    """
    Helper function to display matrix and vector in readable format.
    
    Args:
        A: Matrix to display
        b: Optional right-hand side vector
        title: Title for display
    """
    print(f"\n{title}:")
    for i, row in enumerate(A):
        if b is not None:
            print(f"{row} | {b[i]}")
        else:
            print(row)

# Example usage
if __name__ == "__main__":
    # Test matrix with poor pivots on diagonal
    A = [
        [0.0, 2.0, 1.0],
        [1.0, 0.0, 3.0],
        [4.0, 2.0, 1.0]
    ]
    b = [1.0, 2.0, 3.0]
    n = len(A)
    
    # Test both pivoting strategies
    for strategy in ['partial', 'complete']:
        print(f"\nTesting {strategy} pivoting:")
        
        # Create fresh copies of test data
        A_test = [row[:] for row in A]
        b_test = b[:]
        
        # Create pivoting manager
        manager = PivotingManager(n, strategy=strategy)
        manager.set_scaling(A_test)  # Optional scaling
        
        # Simulate elimination steps
        for k in range(n-1):
            # Find and apply pivot
            pivot_row, pivot_col = manager.find_pivot(A_test, k, use_scaling=True)
            manager.apply_pivot(A_test, b_test, k, pivot_row, pivot_col)
            
            print(f"\nStep {k+1}:")
            print(f"Pivot position: ({pivot_row}, {pivot_col})")
            display_matrix(A_test, b_test, "Current state")
        
        # Show final permutations
        row_perm, col_perm = manager.get_permutations()
        print("\nFinal permutations:")
        print(f"Row permutation: {row_perm}")
        print(f"Column permutation: {col_perm}")
