"""
Implementation of complex number operations for eigenvalue calculations.
"""

from typing import Union, List, Tuple
import math
from dataclasses import dataclass

@dataclass
class Complex:
    """Complex number representation using real and imaginary parts."""
    real: float
    imag: float
    
    def __add__(self, other: 'Complex') -> 'Complex':
        """Add two complex numbers."""
        return Complex(self.real + other.real, self.imag + other.imag)
        
    def __sub__(self, other: 'Complex') -> 'Complex':
        """Subtract two complex numbers."""
        return Complex(self.real - other.real, self.imag - other.imag)
        
    def __mul__(self, other: 'Complex') -> 'Complex':
        """Multiply two complex numbers."""
        return Complex(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real
        )
        
    def __truediv__(self, other: 'Complex') -> 'Complex':
        """Divide two complex numbers."""
        denominator = other.real**2 + other.imag**2
        if denominator == 0:
            raise ValueError("Division by zero")
            
        return Complex(
            (self.real * other.real + self.imag * other.imag) / denominator,
            (self.imag * other.real - self.real * other.imag) / denominator
        )
        
    def conjugate(self) -> 'Complex':
        """Return complex conjugate."""
        return Complex(self.real, -self.imag)
        
    def abs(self) -> float:
        """Return absolute value (modulus)."""
        return math.sqrt(self.real**2 + self.imag**2)
        
    def arg(self) -> float:
        """Return argument (angle) in radians."""
        return math.atan2(self.imag, self.real)
        
    def __str__(self) -> str:
        """String representation."""
        if self.imag >= 0:
            return f"{self.real} + {self.imag}i"
        return f"{self.real} - {abs(self.imag)}i"
        
    def to_polar(self) -> Tuple[float, float]:
        """Convert to polar form (r, θ)."""
        return (self.abs(), self.arg())
        
    @classmethod
    def from_polar(cls, r: float, theta: float) -> 'Complex':
        """Create complex number from polar form."""
        return cls(r * math.cos(theta), r * math.sin(theta))
        
    def __pow__(self, n: int) -> 'Complex':
        """Raise complex number to integer power."""
        if not isinstance(n, int):
            raise ValueError("Only integer powers supported")
            
        r, theta = self.to_polar()
        return Complex.from_polar(r**n, theta*n)

def roots_of_unity(n: int) -> List[Complex]:
    """
    Calculate n-th roots of unity.
    
    Args:
        n: Order of roots
        
    Returns:
        List[Complex]: List of n-th roots of unity
    """
    return [Complex.from_polar(1, 2*math.pi*k/n) for k in range(n)]

def solve_quadratic(a: float, b: float, c: float) -> Tuple[Complex, Complex]:
    """
    Solve quadratic equation ax² + bx + c = 0.
    Uses numerically stable formula for roots.
    
    Args:
        a, b, c: Coefficients of quadratic equation
        
    Returns:
        Tuple[Complex, Complex]: Two roots of equation
    """
    if a == 0:
        if b == 0:
            raise ValueError("Not a quadratic equation")
        return (Complex(-c/b, 0), Complex(-c/b, 0))
        
    # Use numerically stable formula
    q = -(b + math.copysign(math.sqrt(b*b - 4*a*c), b))/2
    
    x1 = Complex(q/a, 0)
    x2 = Complex(c/q, 0) if q != 0 else Complex(0, 0)
    
    return x1, x2

def cis(theta: float) -> Complex:
    """
    Return e^(iθ) = cos(θ) + i*sin(θ).
    
    Args:
        theta: Angle in radians
        
    Returns:
        Complex: Complex number on unit circle
    """
    return Complex(math.cos(theta), math.sin(theta))

# Matrix operations with complex numbers
def matrix_multiply(A: List[List[Complex]], 
                   B: List[List[Complex]]) -> List[List[Complex]]:
    """
    Multiply two complex matrices.
    
    Args:
        A, B: Complex matrices to multiply
        
    Returns:
        List[List[Complex]]: Product matrix
    """
    n, m = len(A), len(A[0])
    p = len(B[0])
    
    C = [[Complex(0, 0) for _ in range(p)] for _ in range(n)]
    
    for i in range(n):
        for j in range(p):
            for k in range(m):
                C[i][j] += A[i][k] * B[k][j]
                
    return C

def conjugate_transpose(A: List[List[Complex]]) -> List[List[Complex]]:
    """
    Compute conjugate transpose (Hermitian transpose) of matrix.
    
    Args:
        A: Complex matrix
        
    Returns:
        List[List[Complex]]: Conjugate transpose matrix
    """
    n, m = len(A), len(A[0])
    return [[A[j][i].conjugate() for j in range(n)] for i in range(m)]

# Example usage
if __name__ == "__main__":
    # Basic complex arithmetic
    z1 = Complex(1, 2)
    z2 = Complex(3, -1)
    
    print(f"z1 = {z1}")
    print(f"z2 = {z2}")
    print(f"z1 + z2 = {z1 + z2}")
    print(f"z1 * z2 = {z1 * z2}")
    print(f"z1 / z2 = {z1 / z2}")
    print(f"|z1| = {z1.abs()}")
    
    # Polar form
    r, theta = z1.to_polar()
    print(f"\nPolar form of z1: r = {r:.4f}, θ = {theta:.4f} rad")
    
    # Roots of unity
    print("\n4th roots of unity:")
    for z in roots_of_unity(4):
        print(z)
        
    # Solve quadratic equation
    print("\nSolving x² + 2x + 2 = 0:")
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
