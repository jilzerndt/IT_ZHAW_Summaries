"""
Implementation of QR decomposition using Householder transformations.
Includes functionality for solving linear systems and least squares problems.
"""

import numpy as np
import matplotlib.pyplot as plt
from basics.rechnerarithmetik import get_machine_epsilon

def householder_vector(x):
    """
    Compute Householder vector v and beta for given vector x.
    The Householder vector is used to create a reflection that zeros out
    all elements below the diagonal in one column.
    
    Args:
        x: Input vector (as numpy array)
        
    Returns:
        Tuple (v, beta) where:
        - v is the Householder vector
        - beta is the scaling factor
    """
    x = np.array(x, dtype=float)
    n = len(x)
    
    # Compute norm of x excluding first element
    sigma = np.sum(x[1:] ** 2)
    
    # Handle special case where vector is already zero below first element
    if sigma == 0 and x[0] >= 0:
        return x, 0
        
    # Compute vector norm including first element
    mu = np.sqrt(x[0]**2 + sigma)
    
    # Choose sign to minimize cancellation error
    if x[0] <= 0:
        v = x.copy()
        v[0] = x[0] - mu
    else:
        v = x.copy()
        v[0] = -sigma / (x[0] + mu)
        
    # Compute beta
    beta = 2 * v[0]**2 / (sigma + v[0]**2)
    
    # Normalize v
    if v[0] != 0:
        v = v / v[0]
        
    return v, beta

def apply_householder(A, v, beta, i):
    """
    Apply Householder transformation in place to matrix A.
    The transformation is I - beta*v*v^T.
    
    Args:
        A: Matrix to transform (modified in place)
        v: Householder vector
        beta: Scaling factor
        i: Starting row/column index
    """
    A = np.array(A)
    n, m = A.shape
    
    for j in range(i, m):
        # Compute v^T * A_j where A_j is column j
        s = np.dot(v, A[i:n, j])
        
        # Update column j: A_j = A_j - beta * v * (v^T * A_j)
        A[i:n, j] -= beta * v * s
        
    return A.tolist()

def qr_decomposition(A, compute_q=True):
    """
    Compute QR decomposition using Householder transformations.
    A = QR where Q is orthogonal and R is upper triangular.
    
    Args:
        A: Input matrix
        compute_q: Whether to explicitly compute Q matrix
        
    Returns:
        Tuple (Q, R):
        - Q: Orthogonal matrix (if compute_q is True, else None)
        - R: Upper triangular matrix
    """
    A = np.array(A, dtype=float)
    n, m = A.shape
    
    # Initialize R as copy of A
    R = A.copy()
    
    # Initialize Q as identity if needed
    Q = np.eye(n) if compute_q else None
    
    # Store Householder vectors and betas
    vs = []
    betas = []
    
    # Main decomposition loop
    for i in range(min(n-1, m)):
        # Extract column vector to be zeroed below diagonal
        x = R[i:, i].copy()
        
        # Compute Householder vector and beta
        v, beta = householder_vector(x)
        
        # Store for later Q computation
        vs.append(v)
        betas.append(beta)
        
        # Apply transformation to R
        R = apply_householder(R, v, beta, i)
        
        # Ensure strict zeros below diagonal
        R[i+1:, i] = 0.0
    
    # Compute Q if requested by accumulating transformations
    if compute_q:
        for i in range(min(n-1, m)-1, -1, -1):
            Q = apply_householder(Q, vs[i], betas[i], i)
        Q = Q.T  # Transpose because we accumulated in reverse
        Q = Q.tolist()
        
    return Q, R.tolist()

def solve_qr(A, b):
    """
    Solve linear system Ax = b using QR decomposition.
    
    Args:
        A: Coefficient matrix
        b: Right-hand side vector
        
    Returns:
        Solution vector x
    """
    A = np.array(A)
    b = np.array(b)
    n = len(b)
    
    # Compute QR decomposition
    Q, R = qr_decomposition(A)
    
    # Compute Q^T * b
    y = np.dot(np.array(Q).T, b)
    
    # Back substitution with R
    x = np.zeros(n)
    R = np.array(R)
    
    for i in range(n-1, -1, -1):
        if abs(R[i,i]) < get_machine_epsilon():
            raise ValueError(f"Zero diagonal element at index {i}")
        
        x[i] = (y[i] - np.dot(R[i,i+1:], x[i+1:])) / R[i,i]
        
    return x.tolist()

def least_squares_qr(A, b):
    """
    Solve least squares problem min ||Ax - b||_2 using QR decomposition.
    
    Args:
        A: Coefficient matrix (m x n, m >= n)
        b: Right-hand side vector (length m)
        
    Returns:
        Solution vector x minimizing ||Ax - b||_2
    """
    A = np.array(A)
    b = np.array(b)
    m, n = A.shape
    
    # Compute QR decomposition
    Q, R = qr_decomposition(A)
    Q = np.array(Q)
    R = np.array(R)
    
    # Compute Q^T * b
    y = np.dot(Q.T, b)
    
    # Solve R1*x = y1 where R1 is the upper n×n block
    x = np.zeros(n)
    
    for i in range(n-1, -1, -1):
        if abs(R[i,i]) < get_machine_epsilon():
            raise ValueError("Rank deficient least squares problem")
            
        x[i] = (y[i] - np.dot(R[i,i+1:], x[i+1:])) / R[i,i]
        
    return x.tolist()

# Example usage and testing
if __name__ == "__main__":
    # Test case 1: Square matrix
    A = np.array([
        [1.0, -2.0, 3.0],
        [2.0, -5.0, 12.0],
        [0.0, 2.0, -10.0]
    ])
    b = np.array([7.0, 17.0, -24.0])
    
    try:
        # Compute and verify QR decomposition
        Q, R = qr_decomposition(A)
        
        print("Q matrix:")
        print(np.array(Q))
        print("\nR matrix:")
        print(np.array(R))
        
        # Verify orthogonality of Q
        Q = np.array(Q)
        QTQ = np.dot(Q.T, Q)
        print("\nVerify Q^T Q = I:")
        print(QTQ)
        
        # Solve system and verify solution
        x = solve_qr(A, b)
        print("\nSolution x:")
        print(x)
        
        residual = np.linalg.norm(np.dot(A, x) - b)
        print(f"\nResidual norm: {residual}")
        
    except ValueError as e:
        print(f"Error: {e}")
    
    # Test case 2: Least squares problem
    # Generate data with noise
    x_data = np.linspace(0, 5, 20)
    y_true = 2.0 * x_data - 1.0
    y_noisy = y_true + np.random.normal(0, 0.5, size=len(x_data))
    
    # Set up least squares problem
    A_ls = np.column_stack([np.ones_like(x_data), x_data])
    b_ls = y_noisy
    
    try:
        # Solve and plot
        coeffs = least_squares_qr(A_ls, b_ls)
        y_fit = coeffs[0] + coeffs[1] * x_data
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_data, y_noisy, 'bo', label='Noisy data')
        plt.plot(x_data, y_true, 'g-', label='True line')
        plt.plot(x_data, y_fit, 'r--', label='QR fit')
        plt.grid(True)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Least Squares Fit using QR Decomposition')
        plt.legend()
        plt.show()
        
        print("\nFitted equation:")
        print(f"y = {coeffs[0]:.4f} + {coeffs[1]:.4f}x")
        print("True equation: y = -1.0000 + 2.0000x")
        
    except ValueError as e:
        print(f"Error: {e}")
