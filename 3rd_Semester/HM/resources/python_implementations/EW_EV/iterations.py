"""
Iterative methods for eigenvalue calculations.
Includes power iteration and QR algorithm implementations.
"""

import numpy as np
from complex_numbers import Complex
from ew_matrix import is_hermitian, matrix_multiply, conjugate_transpose
from basics.matrix_vector_basics import normalize_vector


def power_iteration_with_deflation(A, num_eigenvalues, max_iter=100, tol=1e-10):
    """
    Find multiple eigenvalues using power iteration with deflation.
    Uses successive deflation to find additional eigenvalues after the dominant one.
    
    Args:
        A: Input matrix (2D list of floats)
        num_eigenvalues: Number of eigenvalues to find (integer)
        max_iter: Maximum iterations per eigenvalue (integer)
        tol: Tolerance for convergence (float)
        
    Returns:
        List of tuples (eigenvalue, eigenvector)
        
    Notes:
        - Uses deflation to remove found eigenvalues/vectors
        - May not find all eigenvalues in difficult cases
    """
    n = len(A)
    if num_eigenvalues > n:
        raise ValueError("Cannot find more eigenvalues than matrix dimension")
        
    results = []
    # Make a copy of the matrix to modify during deflation
    current_matrix = [row[:] for row in A]
    
    # Find eigenvalues one at a time
    for k in range(num_eigenvalues):
        # Initial guess vector (k-th unit vector)
        x = normalize_vector([1.0 if i == k else 0.0 for i in range(n)])
        lambda_old = 0.0
        
        # Power iteration loop
        for _ in range(max_iter):
            # Matrix-vector multiplication (y = Ax)
            y = [sum(current_matrix[i][j] * x[j] for j in range(n))
                 for i in range(n)]
            
            # Compute Rayleigh quotient (x^T Ax)
            lambda_new = sum(x[i] * y[i] for i in range(n))
            
            # Normalize the new vector
            try:
                x = normalize_vector(y)
            except ValueError:
                break
                
            # Check for convergence
            if abs(lambda_new - lambda_old) < tol:
                results.append((lambda_new, x))
                
                # Deflate matrix by subtracting λxx^T
                for i in range(n):
                    for j in range(n):
                        current_matrix[i][j] -= lambda_new * x[i] * x[j]
                break
                
            lambda_old = lambda_new
            
    return results

def inverse_iteration_with_shifts(A, shifts, max_iter=100, tol=1e-10):
    """
    Find eigenvalues near given shifts using inverse iteration.
    More effective than power iteration when targeting specific eigenvalues.
    
    Args:
        A: Input matrix (2D list of floats)
        shifts: List of shift values to target specific eigenvalues
        max_iter: Maximum iterations per shift
        tol: Tolerance for convergence
        
    Returns:
        List of tuples (eigenvalue, eigenvector)
        
    Notes:
        - Very effective when good shift values are known
        - May fail if shift is exactly equal to an eigenvalue
    """
    from LGS.gauss import gauss_elimination
    
    n = len(A)
    results = []
    
    # Process each shift value
    for mu in shifts:
        # Initial normalized guess vector
        x = normalize_vector([1.0/np.sqrt(n)] * n)
        lambda_old = mu
        
        # Create shifted matrix A - μI
        A_shifted = [[A[i][j] if i != j else A[i][j] - mu 
                     for j in range(n)] for i in range(n)]
        
        # Inverse iteration loop
        for _ in range(max_iter):
            try:
                # Solve linear system (A - μI)y = x
                y = gauss_elimination(A_shifted, x)
                x = normalize_vector(y)
                
                # Compute Rayleigh quotient with original matrix
                Ax = [sum(A[i][j] * x[j] for j in range(n))
                      for i in range(n)]
                lambda_new = sum(x[i] * Ax[i] for i in range(n))
                
                if abs(lambda_new - lambda_old) < tol:
                    results.append((lambda_new, x))
                    break
                    
                lambda_old = lambda_new
                
            except ValueError:
                break
                
    return results

def qr_algorithm_basic(A, max_iter=100, tol=1e-10):
    """
    Basic QR algorithm for eigenvalue computation.
    Iteratively performs QR decomposition and multiplication in reverse order.
    
    Args:
        A: Input matrix (2D list of floats)
        max_iter: Maximum number of iterations
        tol: Tolerance for convergence
        
    Returns:
        List of eigenvalues (floats)
        
    Notes:
        - No shifts used, so convergence may be slow
        - Works best for symmetric matrices
    """
    from LGS.qr_comp import qr_decomposition
    
    n = len(A)
    current = [row[:] for row in A]
    
    for _ in range(max_iter):
        # Store current diagonal elements
        old_diag = [current[i][i] for i in range(n)]
        
        # Perform QR decomposition
        Q, R = qr_decomposition(current)
        
        # Multiply in reverse order (RQ)
        current = matrix_multiply(R, Q)
        
        # Check convergence on diagonal elements
        new_diag = [current[i][i] for i in range(n)]
        if max(abs(new - old) for new, old in zip(new_diag, old_diag)) < tol:
            break
            
    return [current[i][i] for i in range(n)]

def qr_algorithm_with_shifts(A, max_iter=100, tol=1e-10):
    """
    QR algorithm with Wilkinson shifts for better convergence.
    Uses sophisticated shift strategy to accelerate convergence.
    
    Args:
        A: Input matrix (2D list of floats)
        max_iter: Maximum number of iterations
        tol: Tolerance for convergence
        
    Returns:
        List of eigenvalues (floats)
        
    Notes:
        - Much faster convergence than basic QR algorithm
        - Uses Wilkinson shift for optimal shift selection
    """
    from LGS.qr_comp import qr_decomposition
    
    def wilkinson_shift(A, n):
        """
        Compute Wilkinson shift using 2x2 bottom right corner.
        Chooses shift closer to bottom-right element.
        """
        if n < 2:
            return 0.0
            
        # Extract 2x2 bottom right corner
        a = A[n-2][n-2]
        b = A[n-2][n-1]
        c = A[n-1][n-2]
        d = A[n-1][n-1]
        
        # Compute shift using quadratic formula
        tr = a + d
        det = a*d - b*c
        
        disc = np.sqrt(tr*tr/4 - det)
        mu1 = tr/2 + disc
        mu2 = tr/2 - disc
        
        # Choose eigenvalue closer to d
        return mu2 if abs(d - mu2) < abs(d - mu1) else mu1
    
    n = len(A)
    current = [row[:] for row in A]
    eigenvalues = []
    
    # Main iteration loop - reduces matrix size by 1 each time
    while n > 1:
        # Iterate until bottom subdiagonal element becomes negligible
        for _ in range(max_iter):
            # Compute and apply shift
            mu = wilkinson_shift(current, n)
            
            # Form shifted matrix A - μI
            shifted = [[current[i][j] if i != j else current[i][j] - mu 
                       for j in range(n)] for i in range(n)]
            
            # QR decomposition of shifted matrix
            Q, R = qr_decomposition(shifted)
            
            # Form RQ + μI
            current = [[0.0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    current[i][j] = sum(R[i][k] * Q[k][j] for k in range(n))
                    if i == j:
                        current[i][j] += mu
            
            # Check if bottom subdiagonal element is negligible
            if abs(current[n-1][n-2]) < tol:
                break
                
        # Extract eigenvalue and deflate matrix
        eigenvalues.append(current[n-1][n-1])
        n -= 1
        current = [[current[i][j] for j in range(n)] for i in range(n)]
        
    # Handle the final 1x1 case
    if n == 1:
        eigenvalues.append(current[0][0])
        
    return sorted(eigenvalues, reverse=True)

def simultaneous_iteration(A, num_eigenvalues, max_iter=100, tol=1e-10):
    """
    Compute several eigenvalues and eigenvectors simultaneously.
    Also known as subspace iteration or orthogonal iteration.
    
    Args:
        A: Input matrix (2D list of floats)
        num_eigenvalues: Number of eigenvalues to compute
        max_iter: Maximum number of iterations
        tol: Tolerance for convergence
        
    Returns:
        Tuple containing:
        - List of eigenvalues
        - List of corresponding eigenvectors
        
    Notes:
        - More efficient than power iteration for multiple eigenvalues
        - Maintains orthogonality of eigenvectors
    """
    from LGS.qr_comp import qr_decomposition
    
    n = len(A)
    k = min(num_eigenvalues, n)
    
    # Initialize with part of identity matrix
    Q = [[0.0] * k for _ in range(n)]
    for j in range(k):
        Q[j][j] = 1.0
        
    # Main iteration loop
    for _ in range(max_iter):
        # Power iteration step on all vectors simultaneously
        Y = [[sum(A[i][l] * Q[l][j] for l in range(n))
              for j in range(k)] for i in range(n)]
        
        # Orthogonalize using QR factorization
        Q_new, R = qr_decomposition(Y)
        
        # Check convergence using diagonal dominance
        diff = max(abs(sum(Q_new[i][j] * Q[i][j] for i in range(n)) - 1.0)
                  for j in range(k))
        if diff < tol:
            break
            
        Q = Q_new
        
    # Compute Rayleigh quotients for eigenvalues
    H = [[sum(sum(Q[l][i] * A[l][m] * Q[m][j] 
                  for m in range(n)) for l in range(n))
          for j in range(k)] for i in range(k)]
    
    # Extract eigenvalues using QR algorithm
    eigenvalues = qr_algorithm_with_shifts(H)
    
    return eigenvalues, [[Q[i][j] for i in range(n)] for j in range(k)]

# Example usage and testing code remains the same...
# Example usage
if __name__ == "__main__":
    # Example 1: Power iteration with deflation
    A1 = [
        [4.0, -1.0, 1.0],
        [-1.0, 3.0, -2.0],
        [1.0, -2.0, 3.0]
    ]
    
    print("Power iteration with deflation:")
    try:
        results = power_iteration_with_deflation(A1, 2)
        for i, (eigenval, eigenvec) in enumerate(results):
            print(f"\nEigenvalue {i+1}: {eigenval:.6f}")
            print(f"Eigenvector {i+1}:", [f"{x:.6f}" for x in eigenvec])
            
    except ValueError as e:
        print(f"Error: {e}")
    
    # Example 2: Inverse iteration with shifts
    shifts = [3.0, 4.0]
    print("\nInverse iteration with shifts:")
    try:
        results = inverse_iteration_with_shifts(A1, shifts)
        for i, (eigenval, eigenvec) in enumerate(results):
            print(f"\nShift {shifts[i]}:")
            print(f"Found eigenvalue: {eigenval:.6f}")
            print("Eigenvector:", [f"{x:.6f}" for x in eigenvec])
            
    except ValueError as e:
        print(f"Error: {e}")
    
    # Example 3: QR algorithm
    print("\nQR algorithm (basic):")
    try:
        eigenvalues = qr_algorithm_basic(A1)
        print("Eigenvalues:", [f"{x:.6f}" for x in eigenvalues])
        
    except ValueError as e:
        print(f"Error: {e}")
    
    print("\nQR algorithm (with shifts):")
    try:
        eigenvalues = qr_algorithm_with_shifts(A1)
        print("Eigenvalues:", [f"{x:.6f}" for x in eigenvalues])
        
    except ValueError as e:
        print(f"Error: {e}")
    
    # Example 4: Simultaneous iteration
    print("\nSimultaneous iteration:")
    try:
        eigenvals, eigenvecs = simultaneous_iteration(A1, 2)
        print("Eigenvalues:", [f"{x:.6f}" for x in eigenvals])
        print("\nEigenvectors:")
        for i, vec in enumerate(eigenvecs):
            print(f"v{i+1}:", [f"{x:.6f}" for x in vec])
            
    except ValueError as e:
        print(f"Error: {e}")
    
    # Convergence comparison
    import matplotlib.pyplot as plt
    
    def generate_convergence_data(A: List[List[float]], 
                                max_iter: int = 50) -> dict:
        """Generate convergence data for different methods."""
        n = len(A)
        data = {}
        
        # Power iteration
        x = normalize_vector([1.0] * n)
        values = []
        for _ in range(max_iter):
            y = [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
            lambda_val = sum(x[i] * y[i] for i in range(n))
            values.append(lambda_val)
            x = normalize_vector(y)
        data['Power'] = values
        
        # QR algorithm
        from LGS.qr_comp import qr_decomposition
        current = [row[:] for row in A]
        values = []
        for _ in range(max_iter):
            Q, R = qr_decomposition(current)
            current = matrix_multiply(R, Q)
            values.append(current[0][0])
        data['QR'] = values
        
        return data
    
    convergence_data = generate_convergence_data(A1)
    
    plt.figure(figsize=(10, 6))
    for method, values in convergence_data.items():
        plt.plot(values, label=method)
    plt.grid(True)
    plt.xlabel('Iteration')
    plt.ylabel('Approximate eigenvalue')
    plt.title('Convergence Comparison')
    plt.legend()
    plt.show()