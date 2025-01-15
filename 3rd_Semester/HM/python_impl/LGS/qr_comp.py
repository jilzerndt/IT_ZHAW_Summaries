"""
Implementation of QR decomposition using Householder transformations.
"""

from typing import List, Tuple, Optional
import numpy as np
from basics.rechnerarithmetik import get_machine_epsilon

def householder_vector(x: List[float]) -> Tuple[List[float], float]:
    """
    Compute Householder vector v and beta for given vector x.
    
    Args:
        x: Input vector
        
    Returns:
        Tuple containing:
        - Householder vector v
        - Scalar beta
    """
    n = len(x)
    v = [x[i] for i in range(n)]
    
    # Compute norm of x
    sigma = sum(v[i]**2 for i in range(1, n))
    
    if sigma == 0 and v[0] >= 0:
        beta = 0
    else:
        mu = np.sqrt(v[0]**2 + sigma)
        if v[0] <= 0:
            v[0] = v[0] - mu
        else:
            v[0] = -sigma / (v[0] + mu)
            
        beta = 2 * v[0]**2 / (sigma + v[0]**2)
        
    # Normalize v
    if v[0] != 0:
        for i in range(n):
            v[i] /= v[0]
            
    return v, beta

def apply_householder(A: List[List[float]], 
                     v: List[float], 
                     beta: float, 
                     i: int) -> None:
    """
    Apply Householder transformation in place.
    
    Args:
        A: Matrix to transform
        v: Householder vector
        beta: Scalar beta
        i: Starting row/column index
    """
    n = len(A)
    m = len(A[0])
    
    # Apply transformation A = A - beta*v*(v^T*A)
    for j in range(i, m):
        # Compute v^T*A_j
        s = sum(v[k-i] * A[k][j] for k in range(i, n))
        
        # Update column j
        for k in range(i, n):
            A[k][j] -= beta * v[k-i] * s

def qr_decomposition(A: List[List[float]], 
                    compute_q: bool = True) -> Tuple[Optional[List[List[float]]], 
                                                   List[List[float]]]:
    """
    Compute QR decomposition using Householder transformations.
    
    Args:
        A: Input matrix
        compute_q: Whether to explicitly compute Q matrix
        
    Returns:
        Tuple containing:
        - Q matrix (if compute_q is True, else None)
        - R matrix
    """
    n = len(A)
    m = len(A[0])
    
    # Create working copy for R
    R = [[A[i][j] for j in range(m)] for i in range(n)]
    
    # Initialize Q if needed
    Q = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)] if compute_q else None
    
    # Store Householder vectors and betas for later Q computation
    vs = []
    betas = []
    
    # Perform decomposition
    for i in range(min(n-1, m)):
        # Get column vector
        x = [R[j][i] for j in range(i, n)]
        
        # Compute Householder vector and beta
        v, beta = householder_vector(x)
        
        # Store for Q computation
        vs.append(v)
        betas.append(beta)
        
        # Apply transformation to R
        apply_householder(R, v, beta, i)
        
        # Zero out elements below diagonal (for numerical stability)
        for j in range(i+1, n):
            R[j][i] = 0.0
    
    # Compute Q if requested
    if compute_q:
        for i in range(min(n-1, m)-1, -1, -1):
            apply_householder(Q, vs[i], betas[i], i)
            
        # Transpose Q (since we accumulated transformations in reverse)
        Q = [[Q[j][i] for j in range(n)] for i in range(n)]
    
    return Q, R

def solve_qr(A: List[List[float]], 
             b: List[float]) -> List[float]:
    """
    Solve linear system Ax = b using QR decomposition.
    
    Args:
        A: Coefficient matrix
        b: Right-hand side vector
        
    Returns:
        List[float]: Solution vector
    """
    n = len(A)
    Q, R = qr_decomposition(A)
    
    # Compute Q^T * b
    y = [sum(Q[j][i] * b[j] for j in range(n)) for i in range(n)]
    
    # Back substitution
    x = [0.0] * n
    for i in range(n-1, -1, -1):
        if abs(R[i][i]) < get_machine_epsilon():
            raise ValueError(f"Zero diagonal element at index {i}")
            
        x[i] = y[i]
        for j in range(i+1, n):
            x[i] -= R[i][j] * x[j]
        x[i] /= R[i][i]
        
    return x

def compute_determinant(R: List[List[float]]) -> float:
    """
    Compute determinant from QR decomposition.
    
    Args:
        R: Upper triangular matrix from QR decomposition
        
    Returns:
        float: Determinant of original matrix
    """
    return np.prod([R[i][i] for i in range(len(R))])

def least_squares_qr(A: List[List[float]], 
                    b: List[float]) -> List[float]:
    """
    Solve least squares problem using QR decomposition.
    
    Args:
        A: Coefficient matrix
        b: Right-hand side vector
        
    Returns:
        List[float]: Solution vector minimizing ||Ax - b||_2
    """
    m = len(A)
    n = len(A[0])
    
    # Compute QR decomposition
    Q, R = qr_decomposition(A)
    
    # Compute Q^T * b
    y = [sum(Q[j][i] * b[j] for j in range(m)) for i in range(m)]
    
    # Solve R1*x = y1 where R1 is the upper n×n block of R
    # and y1 contains the first n elements of y
    x = [0.0] * n
    for i in range(n-1, -1, -1):
        if abs(R[i][i]) < get_machine_epsilon():
            raise ValueError(f"Rank deficient least squares problem")
            
        x[i] = y[i]
        for j in range(i+1, n):
            x[i] -= R[i][j] * x[j]
        x[i] /= R[i][i]
        
    return x

# Example usage
if __name__ == "__main__":
    # Example 1: Square system
    A1 = [
        [1.0, -2.0, 3.0],
        [2.0, -5.0, 12.0],
        [0.0, 2.0, -10.0]
    ]
    b1 = [7.0, 17.0, -24.0]
    
    try:
        # Compute QR decomposition
        Q1, R1 = qr_decomposition(A1)
        
        print("Matrix Q:")
        for row in Q1:
            print([f"{x:8.4f}" for x in row])
            
        print("\nMatrix R:")
        for row in R1:
            print([f"{x:8.4f}" for x in row])
            
        # Verify orthogonality of Q
        print("\nVerify Q^T*Q = I:")
        QTQ = [[sum(Q1[k][i] * Q1[k][j] for k in range(len(Q1)))
                for j in range(len(Q1))] for i in range(len(Q1))]
        for row in QTQ:
            print([f"{x:8.4f}" for x in row])
            
        # Solve system
        x1 = solve_qr(A1, b1)
        print("\nSolution:")
        print([f"{x:8.4f}" for x in x1])
        
        # Verify solution
        res1 = [sum(A1[i][j] * x1[j] for j in range(len(x1))) - b1[i] 
                for i in range(len(b1))]
        print("\nResidual:")
        print([f"{x:8.4f}" for x in res1])
        
    except ValueError as e:
        print(f"Error: {e}")
        
    # Example 2: Least squares problem (overdetermined system)
    A2 = [
        [1.0, 0.0],
        [1.0, 1.0],
        [1.0, 2.0],
        [1.0, 3.0]
    ]
    b2 = [1.0, 0.8, 0.5, -0.2]
    
    try:
        # Solve least squares problem
        x2 = least_squares_qr(A2, b2)
        print("\nLeast squares solution:")
        print([f"{x:8.4f}" for x in x2])
        
        # Compute residual
        res2 = [sum(A2[i][j] * x2[j] for j in range(len(x2))) - b2[i] 
                for i in range(len(b2))]
        print("\nResidual norm:", np.sqrt(sum(r*r for r in res2)))
        
    except ValueError as e:
        print(f"Error: {e}")
        
    # Example 3: Compare numerical stability with increasing matrix size
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
    
    # Test matrices of different sizes
    sizes = [5, 10, 20, 50]
    condition = 1e6
    
    print("\nNumerical stability test:")
    print("=" * 60)
    print(f"{'Size':>5} {'Method':>10} {'Q orthog error':>15} {'A=QR error':>15}")
    print("-" * 60)
    
    for n in sizes:
        A = generate_test_matrix(n, condition)
        
        try:
            # Compute QR decomposition
            Q, R = qr_decomposition(A)
            
            # Check orthogonality of Q
            QTQ = [[sum(Q[k][i] * Q[k][j] for k in range(n))
                    for j in range(n)] for i in range(n)]
            Q_error = max(abs(QTQ[i][j] - (1.0 if i == j else 0.0))
                         for i in range(n) for j in range(n))
            
            # Check A = QR
            QR = [[sum(Q[i][k] * R[k][j] for k in range(n))
                   for j in range(n)] for i in range(n)]
            QR_error = max(abs(QR[i][j] - A[i][j])
                          for i in range(n) for j in range(n))
            
            print(f"{n:5d} {'QR':>10} {Q_error:15.2e} {QR_error:15.2e}")
            
        except ValueError as e:
            print(f"{n:5d} {'QR':>10} Failed: {str(e)}")
            
    # Example 4: Visual demonstration of least squares fit
    import matplotlib.pyplot as plt
    
    # Generate noisy data
    x_data = np.linspace(0, 5, 20)
    y_true = 2.0 * x_data - 1.0
    y_data = y_true + np.random.normal(0, 0.5, len(x_data))
    
    # Set up least squares problem
    A_ls = [[1.0, x] for x in x_data]
    b_ls = y_data.tolist()
    
    # Solve using QR
    coeffs = least_squares_qr(A_ls, b_ls)
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(x_data, y_data, 'bo', label='Data points')
    plt.plot(x_data, y_true, 'g-', label='True line')
    plt.plot(x_data, [coeffs[0] + coeffs[1]*x for x in x_data],
             'r--', label='QR fit')
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Least Squares Fit using QR Decomposition')
    plt.legend()
    plt.show()
    
    print("\nLeast squares coefficients:")
    print(f"y = {coeffs[0]:.4f} + {coeffs[1]:.4f}x")
    print(f"True: y = -1.0000 + 2.0000x")
