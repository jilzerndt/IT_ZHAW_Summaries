import numpy as np


def jacobi_decomposition(A):
    """Berechnet D, D^-1, L, R (L+U) aus der Matrix A."""
    D = np.diag(np.diag(A))  # Diagonale von A
    D_inv = np.linalg.inv(D)  # Inverse von D
    L = np.tril(A, -1)  # Untere Dreiecksmatrix ohne Diagonale
    U = np.triu(A, 1)  # Obere Dreiecksmatrix ohne Diagonale
    R = L + U  # L + U
    return D, D_inv, L, U, R


def jacobi_iteration(A, b, x0, num_iterations):
    """Verwendet die Jacobi-Formeln, um Iterationen auszuführen."""
    D, D_inv, L, U, R = jacobi_decomposition(A)
    B = -D_inv @ R  # Iterationsmatrix
    c = D_inv @ b  # Konstanter Vektor
    x = x0

    print("Jacobi-Formeln:")
    print("B = -D^(-1) * (L + U):\n", B)
    print("c = D^(-1) * b:\n", c)

    # Iterationen
    print("\nIterationen:")
    for i in range(1, num_iterations + 1):
        x_new = B @ x + c
        print(f"x^{i} =", x_new)
        x = x_new

    return x

# Nur das muss angepasst werden aufgrund der Aufgabenstellung
# Beispiel: Matrix A und Vektor b
A = np.array([[4, -1, 1], [-2, 5, 1], [1, -2, 5]])
b = np.array([5, 11, 12])
x0 = np.array([0, 0, 0])  # Startvektor, ist nicht immer [0,0,0], kann auch adner sein wie bsp. [1,-10,3], siehe Aufgabenstellung
num_iterations = 2  # Anzahl der Iterationen

# Jacobi-Verfahren
D, D_inv, L, U, R = jacobi_decomposition(A)

print("Matrix D:\n", D)
print("Matrix D^-1:\n", D_inv)
print("Matrix L (untere Dreiecksmatrix ohne Diagonale):\n", L)
print("Matrix U (obere Dreiecksmatrix ohne Diagonale):\n", U)
print("Matrix L + U:\n", R)

# Iterationen durchführen
x_final = jacobi_iteration(A, b, x0, num_iterations)

print("\nLösung nach", num_iterations, "Iterationen:\n", x_final)
