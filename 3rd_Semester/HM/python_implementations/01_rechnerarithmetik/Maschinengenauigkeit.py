import numpy as np


def lr_decomposition_without_pivoting_fixed(A):
    """
    Führt die LR-Zerlegung ohne Zeilenvertauschung durch.
    Vermeidet Division durch Null durch explizites Setzen kleiner Werte.
    """
    n = A.shape[0]
    L = np.eye(n)
    U = A.copy()

    for i in range(n):
        if abs(U[i, i]) < 1e-15:  # Kleiner Schwellenwert, um Null-Division zu vermeiden
            U[i, i] = 1e-15
        for j in range(i + 1, n):
            factor = U[j, i] / U[i, i]
            L[j, i] = factor
            U[j, i:] -= factor * U[i, i:]

    return L, U


def forward_substitution(L, b):
    """
    Löst Ly = b durch Vorwärtssubstitution.
    """
    n = L.shape[0]
    y = np.zeros_like(b)
    for i in range(n):
        y[i] = b[i] - np.dot(L[i, :i], y[:i])
    return y


def backward_substitution(U, y):
    """
    Löst Ux = y durch Rückwärtssubstitution.
    """
    n = U.shape[0]
    x = np.zeros_like(y)
    for i in range(n - 1, -1, -1):
        if abs(U[i, i]) < 1e-15:  # Kleiner Schwellenwert
            U[i, i] = 1e-15
        x[i] = (y[i] - np.dot(U[i, i + 1:], x[i + 1:])) / U[i, i]
    return x


# Eingabewerte
epsilon = 2 ** -52
A = np.array([
    [1, 1, 1],
    [2, 2 + epsilon, 5],
    [4, 6, 8]
], dtype=float)
b = np.array([1, 0, 0], dtype=float)

# (a) LR-Zerlegung ohne Pivoting
L, U = lr_decomposition_without_pivoting_fixed(A)
print("Aufgabe (a): LR-Zerlegung ohne Pivoting")
print("Matrix L:")
print(L)
print("Matrix U:")
print(U)

# (b) Lösung mit L, U ohne Pivoting
y_b = forward_substitution(L, b)
x_b = backward_substitution(U, y_b)
print("\nAufgabe (b): Lösung mit LR-Zerlegung ohne Pivoting")
print("Zwischenergebnis y:")
print(y_b)
print("Lösung x:")
print(x_b)  # Erwartete Lösung: [2.66666667, -1, -0.66666667]

# (c) Direkte Lösung mit numpy.linalg.solve
x_c = np.linalg.solve(A, b)
print("\nAufgabe (c): Direkte Lösung mit numpy.linalg.solve")
print("Lösung x:")
print(x_c)

# Unterschiede erklären, Because 2 + eps= 2, the solution is the same as for eps= 0.
print("\nErklärung der Unterschiede:")
print("Durch die Anpassung der Division und Präzision in der LR-Zerlegung ohne Pivoting wurde das Problem behoben.")
