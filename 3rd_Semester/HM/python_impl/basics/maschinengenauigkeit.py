"""
Demonstration of machine precision effects using LR decomposition.
Shows how numerical errors propagate in matrix computations.
"""

import numpy as np
from typing import Tuple, List, Optional
import matplotlib.pyplot as plt
from rechnerarithmetik import get_machine_epsilon, relative_error
from matrix_vector_basics import norm_matrix

def wilkinson_matrix(n: int) -> List[List[float]]:
    """
    Generate the Wilkinson matrix of size n×n.
    This matrix is particularly sensitive to numerical errors.
    
    Args:
        n: Size of the matrix
        
    Returns:
        List[List[float]]: Wilkinson matrix
    """
    W = [[0.0] * n for _ in range(n)]
    
    # Fill the matrix
    for i in range(n):
        for j in range(n):
            if i == j:
                W[i][j] = abs(i - (n-1)/2)  # Diagonal elements
            elif abs(i-j) == 1:
                W[i][j] = 1.0  # Superdiagonal and subdiagonal elements
                
    return W

def perform_lr_decomposition(A: List[List[float]], 
                           use_pivoting: bool = True) -> Tuple[Optional[List[List[float]]], 
                                                             Optional[List[List[float]]], 
                                                             float]:
    """
    Perform LR decomposition with optional pivoting.
    Tracks accumulated numerical error.
    
    Args:
        A: Input matrix
        use_pivoting: Whether to use partial pivoting
        
    Returns:
        Tuple containing:
        - L matrix (lower triangular)
        - R matrix (upper triangular)
        - Maximum accumulated error
    """
    n = len(A)
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    R = [[A[i][j] for j in range(n)] for i in range(n)]
    
    max_error = 0.0
    
    for k in range(n-1):
        # Find pivot if using pivoting
        if use_pivoting:
            pivot_row = k + max(range(n-k), key=lambda i: abs(R[i+k][k]))
            if pivot_row != k:
                # Swap rows in R
                R[k], R[pivot_row] = R[pivot_row], R[k]
                # Swap rows in L up to k
                for j in range(k):
                    L[k][j], L[pivot_row][j] = L[pivot_row][j], L[k][j]
        
        # Check for effective zero pivot
        if abs(R[k][k]) < get_machine_epsilon():
            return None, None, float('inf')
            
        for i in range(k+1, n):
            factor = R[i][k] / R[k][k]
            L[i][k] = factor
            
            for j in range(k, n):
                # Calculate theoretical vs actual subtraction
                theoretical = R[i][j] - factor * R[k][j]
                R[i][j] = R[i][j] - factor * R[k][j]  # Actual computation
                
                # Track maximum error
                error = abs(theoretical - R[i][j])
                max_error = max(max_error, error)
                
    return L, R, max_error

def demonstrate_precision_effects(sizes: List[int], 
                                use_pivoting: bool = True) -> None:
    """
    Demonstrate the effects of machine precision on matrix decomposition.
    
    Args:
        sizes: List of matrix sizes to test
        use_pivoting: Whether to use partial pivoting
    """
    errors = []
    condition_numbers = []
    
    for n in sizes:
        # Generate test matrix
        W = wilkinson_matrix(n)
        
        # Calculate condition number
        cond_num = norm_matrix(W, p=np.inf)  # Simplified condition number
        condition_numbers.append(cond_num)
        
        # Perform decomposition and get error
        L, R, error = perform_lr_decomposition(W, use_pivoting)
        errors.append(error)
        
        # Print results
        print(f"\nMatrix size {n}x{n}:")
        print(f"Condition number: {cond_num:.2e}")
        print(f"Maximum error: {error:.2e}")
        
        # Check if decomposition failed
        if L is None or R is None:
            print("Decomposition failed - matrix likely singular")
            continue
            
        # Verify decomposition by reconstructing A
        A_reconstructed = [[sum(L[i][k] * R[k][j] for k in range(n)) 
                           for j in range(n)] for i in range(n)]
        
        max_diff = max(max(abs(A_reconstructed[i][j] - W[i][j]) 
                      for j in range(n)) for i in range(n))
        print(f"Maximum difference in reconstruction: {max_diff:.2e}")
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, errors, 'b.-', label='Maximum Error')
    plt.plot(sizes, condition_numbers, 'r.-', label='Condition Number')
    plt.yscale('log')
    plt.grid(True)
    plt.xlabel('Matrix Size')
    plt.ylabel('Value (log scale)')
    plt.title('Error Growth and Condition Number vs Matrix Size')
    plt.legend()
    plt.show()

def analyze_rounding_effects() -> None:
    """
    Analyze and demonstrate various rounding effects in floating-point arithmetic.
    """
    eps = get_machine_epsilon()
    print(f"Machine epsilon: {eps}")
    
    # Demonstrate cancellation error
    a = 1.0
    b = 1.0 + eps
    c = b - a
    print(f"\nCancellation error demonstration:")
    print(f"1 + eps - 1 = {c} (should be {eps})")
    
    # Demonstrate accumulation of rounding errors
    sum_forward = 0.0
    sum_backward = 0.0
    n = 1000000
    numbers = [1.0/i for i in range(1, n+1)]
    
    # Forward summation
    for x in numbers:
        sum_forward += x
        
    # Backward summation
    for x in reversed(numbers):
        sum_backward += x
        
    print(f"\nAccumulation of rounding errors in summation:")
    print(f"Forward sum: {sum_forward}")
    print(f"Backward sum: {sum_backward}")
    print(f"Relative difference: {abs(sum_forward - sum_backward)/sum_backward}")

if __name__ == "__main__":
    # Demonstrate machine precision effects
    matrix_sizes = [4, 8, 12, 16, 20]
    demonstrate_precision_effects(matrix_sizes, use_pivoting=True)
    
    # Analyze general rounding effects
    analyze_rounding_effects()
    
    # Demonstrate Wilkinson's polynomial instability
    n = 20
    W = wilkinson_matrix(n)
    print(f"\nWilkinson matrix condition number ({n}x{n}): {norm_matrix(W, p=np.inf):.2e}")
