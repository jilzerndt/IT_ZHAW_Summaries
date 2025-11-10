"""
Matrix operations for eigenvalue calculations.
Includes determinant, characteristic polynomial, and eigenvalue computation.
"""

import numpy as np
from complex_numbers import Complex
from basics.matrix_vector_basics import matrix_multiply, matrix_subtract

"""Spezielle Matrizen (Special Matrices)"""

def identity_matrix(n):
    """
    Create n×n identity matrix with ones on diagonal and zeros elsewhere.
    
    Args:
        n: Size of the matrix (integer)
        
    Returns:
        2D list representing the identity matrix
        
    Example:
        For n=2, returns [[1.0, 0.0], [0.0, 1.0]]
    """
    # Use list comprehension to create matrix with 1s on diagonal, 0s elsewhere
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def scalar_matrix(n, scalar):
    """
    Create n×n scalar matrix (λI) - scalar multiple of identity matrix.
    Useful for characteristic equation calculations.
    
    Args:
        n: Size of the matrix (integer)
        scalar: Value to put on diagonal (float)
        
    Returns:
        2D list representing the scalar matrix
        
    Example:
        For n=2, scalar=3, returns [[3.0, 0.0], [0.0, 3.0]]
    """
    # Similar to identity_matrix but with scalar value instead of 1
    return [[scalar if i == j else 0.0 for j in range(n)] for i in range(n)]

"""Matrix Properties"""

def is_symmetric(A):
    """
    Check if matrix is symmetric (A = A^T).
    A matrix is symmetric if it equals its transpose.
    
    Args:
        A: Input matrix (2D list of floats)
        
    Returns:
        Boolean indicating if matrix is symmetric
        
    Note:
        Uses small tolerance (1e-10) for floating point comparison
    """
    n = len(A)
    # Check each pair of corresponding elements across diagonal
    return all(abs(A[i][j] - A[j][i]) < 1e-10 for i in range(n) for j in range(n))

def is_positive_definite(A):
    """
    Check if matrix is positive definite using Sylvester's criterion.
    A matrix is positive definite if all its leading principal minors are positive.
    
    Args:
        A: Input matrix (2D list of floats)
        
    Returns:
        Boolean indicating if matrix is positive definite
        
    Note:
        Matrix must be symmetric for this test to be valid
    """
    # First check symmetry as it's required for positive definiteness
    if not is_symmetric(A):
        return False
        
    n = len(A)
    # Check each leading principal minor
    for k in range(1, n+1):
        # Extract submatrix of size k×k from upper-left corner
        submatrix = [[A[i][j] for j in range(k)] for i in range(k)]
        # If any determinant is non-positive, matrix is not positive definite
        if determinant(submatrix) <= 0:
            return False
            
    return True

"""Matrix Properties: Determinant, Trace, Characteristic Polynomial"""

def determinant(A):
    """
    Calculate matrix determinant using recursive expansion by first row.
    Uses Laplace expansion along first row for recursive calculation.
    
    Args:
        A: Input matrix (2D list of floats)
        
    Returns:
        float: Determinant value
        
    Note:
        Efficient for small matrices but not recommended for large ones
    """
    n = len(A)
    # Base cases for recursion
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0]*A[1][1] - A[0][1]*A[1][0]
        
    det = 0
    # Expand along first row
    for j in range(n):
        # Create submatrix by removing first row and current column
        submatrix = [[A[i][k] for k in range(n) if k != j] 
                    for i in range(1, n)]
        # Add term to determinant (with alternating sign)
        det += ((-1)**j) * A[0][j] * determinant(submatrix)
        
    return det

def trace(A):
    """
    Calculate matrix trace (sum of diagonal elements).
    
    Args:
        A: Input matrix (2D list of floats)
        
    Returns:
        float: Sum of diagonal elements
    """
    return sum(A[i][i] for i in range(len(A)))

def characteristic_polynomial(A, lambda_val):
    """
    Evaluate characteristic polynomial det(A - λI) at given λ value.
    This polynomial's roots are the eigenvalues of A.
    
    Args:
        A: Input matrix (2D list of floats)
        lambda_val: Value at which to evaluate polynomial (float)
        
    Returns:
        float: Value of characteristic polynomial at lambda_val
    """
    n = len(A)
    # Create λI matrix
    lambda_matrix = scalar_matrix(n, lambda_val)
    # Compute A - λI
    diff_matrix = matrix_subtract(A, lambda_matrix)
    # Return determinant of A - λI
    return determinant(diff_matrix)

"""Eigenvalue Methods"""

def gerschgorin_circles(A):
    """
    Compute Gerschgorin circles for eigenvalue bounds.
    Each circle is centered at diagonal element with radius equal to
    sum of absolute values of off-diagonal elements in that row.
    
    Args:
        A: Input matrix (2D list of floats)
        
    Returns:
        List of tuples (center, radius) defining each circle
    """
    n = len(A)
    circles = []
    
    for i in range(n):
        # Center is diagonal element
        center = A[i][i]
        # Radius is sum of absolute values of off-diagonal elements
        radius = sum(abs(A[i][j]) for j in range(n) if j != i)
        circles.append((center, radius))
        
    return circles

def estimate_eigenvalue_bounds(A):
    """
    Estimate bounds for eigenvalues using Gerschgorin circles.
    All eigenvalues lie in the union of these circles.
    
    Args:
        A: Input matrix (2D list of floats)
        
    Returns:
        Tuple (lower_bound, upper_bound) for eigenvalues
    """
    circles = gerschgorin_circles(A)
    # Find extremes of all circles
    lower = min(center - radius for center, radius in circles)
    upper = max(center + radius for center, radius in circles)
    return lower, upper

def power_method_step(A, x):
    """
    Perform one iteration of power method for finding largest eigenvalue.
    
    Args:
        A: Input matrix (2D list of floats)
        x: Current approximation of eigenvector (list of floats)
        
    Returns:
        Tuple (new_vector, rayleigh_quotient):
        - new_vector: Normalized next approximation
        - rayleigh_quotient: Estimate of largest eigenvalue
    """
    n = len(A)
    
    # Compute matrix-vector product Ax
    y = [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
    
    # Compute Rayleigh quotient (x^T A x)/(x^T x)
    rayleigh = sum(x[i] * y[i] for i in range(n)) / sum(x[i] * x[i] for i in range(n))
    
    # Normalize the vector
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