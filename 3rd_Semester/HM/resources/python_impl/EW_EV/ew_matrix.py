"""
Matrix operations for eigenvalue calculations.
Includes determinant, characteristic polynomial, and eigenvalue computation.
"""

from typing import List, Tuple, Optional
import numpy as np
from complex_numbers import Complex
from basics.matrix_vector_basics import matrix_multiply, matrix_subtract

"""Spezielle Matrizen"""

def identity_matrix(n: int) -> List[List[float]]:
    """
    Create n×n identity matrix.
    
    Args:
        n: Matrix size
        
    Returns:
        List[List[float]]: Identity matrix
    """
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def scalar_matrix(n: int, scalar: float) -> List[List[float]]:
    """
    Create n×n scalar matrix (λI).
    
    Args:
        n: Matrix size
        scalar: Scalar value
        
    Returns:
        List[List[float]]: Scalar matrix
    """
    return [[scalar if i == j else 0.0 for j in range(n)] for i in range(n)]

"""Eigenschaften prüfen"""

def is_symmetric(A: List[List[float]]) -> bool:
    """
    Check if matrix is symmetric.
    
    Args:
        A: Input matrix
        
    Returns:
        bool: True if matrix is symmetric
    """
    n = len(A)
    return all(abs(A[i][j] - A[j][i]) < 1e-10 for i in range(n) for j in range(n))

def is_positive_definite(A: List[List[float]]) -> bool:
    """
    Check if matrix is positive definite using Sylvester's criterion.
    
    Args:
        A: Input matrix
        
    Returns:
        bool: True if matrix is positive definite
    """
    if not is_symmetric(A):
        return False
        
    n = len(A)
    for k in range(1, n+1):
        submatrix = [[A[i][j] for j in range(k)] for i in range(k)]
        if determinant(submatrix) <= 0:
            return False
            
    return True

"""Determinante, Spur, charakteristisches Polynom"""

def determinant(A: List[List[float]]) -> float:
    """
    Calculate determinant using recursive expansion.
    
    Args:
        A: Input matrix
        
    Returns:
        float: Determinant value
    """
    n = len(A)
    if n == 1:
        return A[0][0]
        
    if n == 2:
        return A[0][0]*A[1][1] - A[0][1]*A[1][0]
        
    det = 0
    for j in range(n):
        # Create submatrix by removing first row and column j
        submatrix = [[A[i][k] for k in range(n) if k != j] 
                    for i in range(1, n)]
        det += ((-1)**j) * A[0][j] * determinant(submatrix)
        
    return det

def trace(A: List[List[float]]) -> float:
    """
    Calculate matrix trace (sum of diagonal elements).
    
    Args:
        A: Input matrix
        
    Returns:
        float: Trace value
    """
    return sum(A[i][i] for i in range(len(A)))

def characteristic_polynomial(A: List[List[float]], lambda_val: float) -> float:
    """
    Evaluate characteristic polynomial det(A - λI).
    
    Args:
        A: Input matrix
        lambda_val: Value at which to evaluate polynomial
        
    Returns:
        float: Value of characteristic polynomial
    """
    n = len(A)
    lambda_matrix = scalar_matrix(n, lambda_val)
    diff_matrix = matrix_subtract(A, lambda_matrix)
    return determinant(diff_matrix)

"""Eigenwerte und Eigenvektoren"""

def gerschgorin_circles(A: List[List[float]]) -> List[Tuple[float, float]]:
    """
    Compute Gerschgorin circles for eigenvalue bounds.
    
    Args:
        A: Input matrix
        
    Returns:
        List[Tuple[float, float]]: List of (center, radius) pairs
    """
    n = len(A)
    circles = []
    
    for i in range(n):
        center = A[i][i]
        radius = sum(abs(A[i][j]) for j in range(n) if j != i)
        circles.append((center, radius))
        
    return circles

def estimate_eigenvalue_bounds(A: List[List[float]]) -> Tuple[float, float]:
    """
    Estimate bounds for eigenvalues using Gerschgorin circles.
    
    Args:
        A: Input matrix
        
    Returns:
        Tuple[float, float]: Lower and upper bounds for eigenvalues
    """
    circles = gerschgorin_circles(A)
    lower = min(center - radius for center, radius in circles)
    upper = max(center + radius for center, radius in circles)
    return lower, upper

def power_method_step(A: List[List[float]], x: List[float]) -> Tuple[List[float], float]:
    """
    Perform one step of power method.
    
    Args:
        A: Input matrix
        x: Current vector
        
    Returns:
        Tuple[List[float], float]: New vector and Rayleigh quotient
    """
    n = len(A)
    
    # Matrix-vector multiplication
    y = [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
    
    # Compute Rayleigh quotient
    rayleigh = sum(x[i] * y[i] for i in range(n)) / sum(x[i] * x[i] for i in range(n))
    
    # Normalize
    norm = np.sqrt(sum(y[i] * y[i] for i in range(n)))
    y = [y[i]/norm for i in range(n)]
    
    return y, rayleigh

# Example usage
if __name__ == "__main__":
    # Example 1: Basic matrix operations
    A1 = [
        [4.0, -1.0, 0.0],
        [-1.0, 4.0, -1.0],
        [0.0, -1.0, 4.0]
    ]
    
    print("Matrix A:")
    for row in A1:
        print([f"{x:6.2f}" for x in row])
        
    print(f"\nDeterminant: {determinant(A1):.4f}")
    print(f"Trace: {trace(A1):.4f}")
    
    # Example 2: Characteristic polynomial
    lambdas = [0.0, 2.0, 4.0, 6.0]
    print("\nCharacteristic polynomial values:")
    for lambda_val in lambdas:
        p_val = characteristic_polynomial(A1, lambda_val)
        print(f"p({lambda_val}) = {p_val:.4f}")
        
    # Example 3: Matrix properties
    print(f"\nSymmetric: {is_symmetric(A1)}")
    print(f"Positive definite: {is_positive_definite(A1)}")
    
    # Example 4: Gerschgorin circles
    circles = gerschgorin_circles(A1)
    print("\nGerschgorin circles (center, radius):")
    for i, (center, radius) in enumerate(circles):
        print(f"Circle {i+1}: ({center:.4f}, {radius:.4f})")
        
    # Eigenvalue bounds
    lower, upper = estimate_eigenvalue_bounds(A1)
    print(f"\nEigenvalue bounds: [{lower:.4f}, {upper:.4f}]")
    
    # Example 5: Power method demonstration
    print("\nPower method iterations:")
    n = len(A1)
    x = [1.0/np.sqrt(n)] * n  # Initial normalized vector
    
    for i in range(5):
        x, rayleigh = power_method_step(A1, x)
        print(f"Iteration {i+1}:")
        print(f"Approximate eigenvalue: {rayleigh:.6f}")
        print("Approximate eigenvector:", [f"{v:.6f}" for v in x])
    
    # Visualize Gerschgorin circles
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(8, 8))
    for center, radius in circles:
        circle = plt.Circle((center, 0), radius, fill=False)
        plt.gca().add_patch(circle)
        
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    plt.grid(True)
    plt.axis('equal')
    plt.title('Gerschgorin Circles')
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    
    # Add some padding to the plot
    plt.xlim(lower - 1, upper + 1)
    plt.ylim(-max(radius for _, radius in circles) - 1,
             max(radius for _, radius in circles) + 1)
    
    plt.show()
