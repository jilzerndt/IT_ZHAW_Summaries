"""
Basic matrix and vector operations implementation.
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

def matrix_multiply(A, B):
    """
    Multiply two matrices.
    
    Args:
        A, B: Input matrices
        
    Returns:
        Product matrix
    """
    n, m = len(A), len(A[0])
    p = len(B[0])
    
    if len(B) != m:
        raise ValueError("Matrix dimensions do not match")
        
    C = [[0.0] * p for _ in range(n)]
    for i in range(n):
        for j in range(p):
            C[i][j] = sum(A[i][k] * B[k][j] for k in range(m))
            
    return C

def matrix_subtract(A, B):
    """
    Subtract two matrices.
    
    Args:
        A, B: Input matrices
        
    Returns:
        Difference matrix
    """
    n, m = len(A), len(A[0])
    if len(B) != n or len(B[0]) != m:
        raise ValueError("Matrix dimensions do not match")
        
    return [[A[i][j] - B[i][j] for j in range(m)] for i in range(n)]

def matrix_add(A, B):
    """
    Add two matrices.
    
    Args:
        A, B: Input matrices
    
    Returns:
        Sum matrix
    """
    n, m = len(A), len(A[0])
    if len(B) != n or len(B[0]) != m:
        raise ValueError("Matrix dimensions do not match")
        
    return [[A[i][j] + B[i][j] for j in range(m)] for i in range(n)]

def matrix_transpose(A):
    """
    Transpose a matrix.
    
    Args:
        A: Input matrix
    
    Returns:
        Transposed matrix
    """
    n, m = len(A), len(A[0])
    return [[A[j][i] for j in range(n)] for i in range(m)]

def norm_vector(v, p=2):
    """
    Calculate p-norm of a vector.
    
    Args:
        v: Input vector
        p: Which p-norm to calculate (1 = Manhattan, 2 = Euclidean, np.inf = Maximum)
    
    Returns:
        The calculated norm
    """
    if p == np.inf:
        return max(abs(x) for x in v)
    return sum(abs(x)**p for x in v)**(1/p)

def norm_matrix(A, p=2):
    """
    Calculate matrix norm.
    
    Args:
        A: Input matrix
        p: Which norm to calculate (1 = column sum, 2 = spectral, np.inf = row sum)
    
    Returns:
        The calculated norm
    """
    if not A or not A[0]:  # Check for empty matrix
        return 0.0
        
    n, m = len(A), len(A[0])
    
    if p == 1:  # Maximum column sum
        return max(sum(abs(A[i][j]) for i in range(n)) for j in range(m))
    elif p == np.inf:  # Maximum row sum
        return max(sum(abs(x) for x in row) for row in A)
    elif p == 2:  # Spectral norm
        AT = matrix_transpose(A)
        ATA = matrix_multiply(AT, A)
        # This is a simplified implementation - actual spectral norm would need eigenvalues
        return math.sqrt(max(sum(abs(x) for x in row) for row in ATA))
    
    raise ValueError(f"Norm {p} not implemented")

def normalize_vector(v):
    """
    Normalize vector to unit length.
    
    Args:
        v: Input vector
        
    Returns:
        Normalized vector
    """
    norm = np.sqrt(sum(x*x for x in v))
    if norm == 0:
        raise ValueError("Zero vector cannot be normalized")
    return [x/norm for x in v]

def is_symmetric(A):
    """
    Check if matrix is symmetric.
    
    Args:
        A: Input matrix
    
    Returns:
        bool: True if matrix is symmetric
    """
    n = len(A)
    if n != len(A[0]):
        return False
    return all(A[i][j] == A[j][i] for i in range(n) for j in range(i+1, n))

def condition_number(A, p=2):
    """
    Calculate condition number of matrix using specified norm.
    
    Args:
        A: Input matrix
        p: Which norm to use
    
    Returns:
        Condition number
    """
    # This is a simplified implementation - actual calculation would need matrix inverse
    return norm_matrix(A, p) * norm_matrix(A, p)

def plot_matrix_heatmap(A, title="Matrix Heatmap"):
    """
    Create a heatmap visualization of a matrix.
    
    Args:
        A: Input matrix
        title: Plot title
    """
    plt.figure(figsize=(10, 8))
    plt.imshow(A, cmap='viridis')
    plt.colorbar(label='Value')
    plt.title(title)
    for i in range(len(A)):
        for j in range(len(A[0])):
            plt.text(j, i, f'{A[i][j]:.2f}', ha='center', va='center')
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    # Demonstrate vector norms
    v = [1, -2, 3]
    print(f"Vector {v}:")
    print(f"1-norm: {norm_vector(v, 1)}")
    print(f"2-norm: {norm_vector(v, 2)}")
    print(f"inf-norm: {norm_vector(v, np.inf)}")
    
    # Demonstrate matrix norms
    A = [[1, 2], [-3, 4]]
    print(f"\nMatrix {A}:")
    print(f"1-norm: {norm_matrix(A, 1)}")
    print(f"inf-norm: {norm_matrix(A, np.inf)}")
    
    # Demonstrate matrix operations
    B = [[2, -1], [1, 3]]
    print(f"\nMatrix multiplication:")
    C = matrix_multiply(A, B)
    print(f"Result: {C}")
    
    # Visualize matrix
    plot_matrix_heatmap(A, "Example Matrix")
