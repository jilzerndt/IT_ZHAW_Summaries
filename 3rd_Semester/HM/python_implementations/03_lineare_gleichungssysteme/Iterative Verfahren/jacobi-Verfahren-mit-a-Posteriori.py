import numpy as np

def jacobi_method(A, b, x0, max_iterations, tol):
    """
    Implementiert das Jacobi-Verfahren, um ein lineares Gleichungssystem zu lösen.
    """
    n = len(b)
    x = x0.copy()
    x_new = np.zeros_like(x)
    for k in range(max_iterations):
        for i in range(n):
            sum_ = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i + 1:], x[i + 1:])
            x_new[i] = (b[i] - sum_) / A[i, i]
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new, k + 1  # Gibt die Lösung und die Anzahl der Iterationen zurück
        x = x_new.copy()
    return x, max_iterations

# Eingabewerte
A = np.array([
    [4, -1, 0, 0, 0, 0],
    [-1, 4, -1, 0, 0, 0],
    [0, -1, 4, -1, 0, 0],
    [0, 0, -1, 4, -1, 0],
    [0, 0, 0, -1, 4, -1],
    [0, 0, 0, 0, -1, 4]
], dtype=float)

b = np.array([4, 0, 0, 0, 0, 4], dtype=float)

# Jacobi-Parameter
tol = 1e-5  # Toleranz
max_iterations = 100  # Maximale Iterationen
x0 = np.zeros(len(b))  # Anfangsvektor

# Jacobi-Verfahren ausführen
jacobi_solution, jacobi_iterations = jacobi_method(A, b, x0, max_iterations, tol)

# Ergebnisse ausgeben
print("Eingegebene Matrix A:")
print(A)
print("\nRechter Vektor b:")
print(b)
print("\nStartvektor x0:")
print(x0)
print("\nLösung mit Jacobi-Verfahren:")
print(jacobi_solution)
print("\nAnzahl der Iterationen:")
print(jacobi_iterations)
