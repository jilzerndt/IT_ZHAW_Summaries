import math
import numpy as np
from typing import Union, List, Tuple, Callable
import matplotlib.pyplot as plt
import sympy as sp

# Type aliases
Number = Union[int, float]
Vector = List[Number]
Matrix = List[List[Number]]

def norm_vector(v: Vector, p: int = 2) -> float:
    """
    Calculate p-norm of a vector.
    
    Args:
        v: Input vector
        p: Which p-norm to calculate (1 = Manhattan, 2 = Euclidean, np.inf = Maximum)
    
    Returns:
        float: The calculated norm
    """
    if p == np.inf:
        return max(abs(x) for x in v)
    return sum(abs(x)**p for x in v)**(1/p)

def norm_matrix(A: Matrix, p: int = 2) -> float:
    """
    Calculate matrix norm.
    
    Args:
        A: Input matrix
        p: Which norm to calculate (1 = column sum, 2 = spectral, np.inf = row sum)
    
    Returns:
        float: The calculated norm
    """
    if not A or not A[0]:  # Check for empty matrix
        return 0.0
        
    n, m = len(A), len(A[0])
    
    if p == 1:  # Maximum column sum
        return max(sum(abs(A[i][j]) for i in range(n)) for j in range(m))
    elif p == np.inf:  # Maximum row sum
        return max(sum(abs(x) for x in row) for row in A)
    elif p == 2:  # Spectral norm - this is simplified, actual implementation would need eigenvalues
        # For actual spectral norm we would need to calculate sqrt(largest eigenvalue of A^T A)
        AT = [[A[j][i] for j in range(n)] for i in range(m)]
        ATA = [[sum(AT[i][k] * A[k][j] for k in range(n)) for j in range(n)] for i in range(m)]
        # This is a placeholder - actual implementation would need eigenvalue calculation
        return math.sqrt(max(sum(abs(x) for x in row) for row in ATA))
    
    raise ValueError(f"Norm {p} not implemented")

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
    