"""
Implementation of complex number operations for eigenvalue calculations.
Provides complex arithmetic and matrix operations without using numpy's complex type.
"""

import math
import numpy as np

class Complex:
    """Complex number representation using real and imaginary parts."""
    def __init__(self, real, imag):
        self.real = float(real)
        self.imag = float(imag)
    
    def __add__(self, other):
        """Add two complex numbers."""
        return Complex(self.real + other.real, self.imag + other.imag)
        
    def __sub__(self, other):
        """Subtract two complex numbers."""
        return Complex(self.real - other.real, self.imag - other.imag)
        
    def __mul__(self, other):
        """Multiply two complex numbers."""
        return Complex(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real
        )
        
    def __truediv__(self, other):
        """Divide two complex numbers."""
        denominator = other.real**2 + other.imag**2
        if denominator == 0:
            raise ValueError("Division by zero")
            
        return Complex(
            (self.real * other.real + self.imag * other.imag) / denominator,
            (self.imag * other.real - self.real * other.imag) / denominator
        )
        
    def conjugate(self):
        """Return complex conjugate."""
        return Complex(self.real, -self.imag)
        
    def abs(self):
        """Return absolute value (modulus)."""
        return math.sqrt(self.real**2 + self.imag**2)
        
    def arg(self):
        """Return argument (angle) in radians."""
        return math.atan2(self.imag, self.real)
        
    def __str__(self):
        """String representation."""
        if self.imag >= 0:
            return f"{self.real:.4f} + {self.imag:.4f}i"
        return f"{self.real:.4f} - {abs(self.imag):.4f}i"
        
    def to_polar(self):
        """Convert to polar form (r, θ)."""
        return (self.abs(), self.arg())
        
    @classmethod
    def from_polar(cls, r, theta):
        """Create complex number from polar form."""
        return cls(r * math.cos(theta), r * math.sin(theta))
        
    def __pow__(self, n):
        """Raise complex number to integer power."""
        if not isinstance(n, int):
            raise ValueError("Only integer powers supported")
            
        r, theta = self.to_polar()
        return Complex.from_polar(r**n, theta*n)

def roots_of_unity(n):
    """
    Calculate n-th roots of unity.
    Returns list of n complex numbers representing the n-th roots.
    """
    return [Complex.from_polar(1, 2*math.pi*k/n) for k in range(n)]

def solve_quadratic(a, b, c):
    """
    Solve quadratic equation ax² + bx + c = 0.
    Uses numerically stable formula for roots.
    Returns tuple of two Complex numbers representing the roots.
    """
    if a == 0:
        if b == 0:
            raise ValueError("Not a quadratic equation")
        return (Complex(-c/b, 0), Complex(-c/b, 0))
        
    # Use numerically stable formula for better accuracy
    q = -(b + math.copysign(math.sqrt(b*b - 4*a*c), b))/2
    
    x1 = Complex(q/a, 0)
    x2 = Complex(c/q, 0) if q != 0 else Complex(0, 0)
    
    return x1, x2

def cis(theta):
    """
    Return e^(iθ) = cos(θ) + i*sin(θ).
    Represents a complex number on the unit circle at angle θ.
    """
    return Complex(math.cos(theta), math.sin(theta))

def matrix_multiply(A, B):
    """
    Multiply two complex matrices.
    Each matrix element should be a Complex object.
    """
    n, m = len(A), len(A[0])
    p = len(B[0])
    
    C = [[Complex(0, 0) for _ in range(p)] for _ in range(n)]
    
    for i in range(n):
        for j in range(p):
            for k in range(m):
                C[i][j] += A[i][k] * B[k][j]
                
    return C

def conjugate_transpose(A):
    """
    Compute conjugate transpose (Hermitian transpose) of complex matrix.
    Each matrix element should be a Complex object.
    """
    n, m = len(A), len(A[0])
    return [[A[j][i].conjugate() for j in range(n)] for i in range(m)]

def matrix_eigenvalues(A, max_iter=100, tol=1e-10):
    """
    Estimate eigenvalues of 2x2 complex matrix using characteristic equation.
    Returns list of Complex numbers representing eigenvalues.
    """
    if len(A) != 2 or len(A[0]) != 2:
        raise ValueError("Only 2x2 matrices supported")
        
    # Get coefficients of characteristic equation: λ² + bλ + c = 0
    b = -(A[0][0].real + A[1][1].real)
    c = (A[0][0] * A[1][1] - A[0][1] * A[1][0]).real
    
    # Solve quadratic equation
    return solve_quadratic(1, b, c)

# Example usage and testing
if __name__ == "__main__":
    # Basic complex arithmetic
    z1 = Complex(1, 2)
    z2 = Complex(3, -1)
    
    print(f"Complex number operations:")
    print(f"z1 = {z1}")
    print(f"z2 = {z2}")
    print(f"z1 + z2 = {z1 + z2}")
    print(f"z1 * z2 = {z1 * z2}")
    print(f"z1 / z2 = {z1 / z2}")
    print(f"|z1| = {z1.abs()}")
    
    # Polar form
    r, theta = z1.to_polar()
    print(f"\nPolar form of z1:")
    print(f"r = {r:.4f}, θ = {theta:.4f} rad")
    z3 = Complex.from_polar(r, theta)
    print(f"Reconstructed from polar: {z3}")
    
    # Roots of unity
    print(f"\n4th roots of unity:")
    for z in roots_of_unity(4):
        print(z)
        
    # Solve quadratic equation
    print(f"\nSolving x² + 2x + 2 = 0:")
    root1, root2 = solve_quadratic(1, 2, 2)
    print(f"x₁ = {root1}")
    print(f"x₂ = {root2}")
    
    # Complex matrices
    A = [
        [Complex(1, 0), Complex(0, 1)],
        [Complex(0, -1), Complex(1, 0)]
    ]
    
    B = [
        [Complex(1, 1), Complex(0, 0)],
        [Complex(0, 0), Complex(1, -1)]
    ]
    
    print("\nMatrix multiplication:")
    C = matrix_multiply(A, B)
    for row in C:
        print([str(z) for z in row])
        
    print("\nConjugate transpose:")
    AH = conjugate_transpose(A)
    for row in AH:
        print([str(z) for z in row])
        
    print("\nMatrix eigenvalues:")
    eigvals = matrix_eigenvalues(A)
    print([str(z) for z in eigvals])
