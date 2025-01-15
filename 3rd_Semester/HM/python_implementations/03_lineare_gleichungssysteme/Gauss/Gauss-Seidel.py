import numpy as np


def gauss_seidel_decomposition(A):
    """Berechnet (D + L) und U aus der Matrix A."""
    D = np.diag(np.diag(A))  # Diagonale von A
    L = np.tril(A, -1)  # Untere Dreiecksmatrix ohne Diagonale
    U = np.triu(A, 1)  # Obere Dreiecksmatrix ohne Diagonale
    DL = D + L  # D + L
    return D, L, U, DL


def gauss_seidel_iteration(A, b, x0, num_iterations):
    """Führt das Gauss-Seidel-Verfahren aus und speichert alle Iterationen."""
    D, L, U, DL = gauss_seidel_decomposition(A)
    DL_inv = np.linalg.inv(DL)  # Inverse von D + L
    c = DL_inv @ b  # Konstanter Vektor
    B = -DL_inv @ U  # Iterationsmatrix
    x = x0
    history = [x0]  # Speicherung der Zwischenergebnisse

    for _ in range(num_iterations):
        x_new = B @ x + c
        history.append(x_new)
        x = x_new

    return x, history, B, c


def calculate_a_posteriori_error(x_approx, x_exact):
    """Berechnet den a-posteriori Fehler ||x^(k) - x||."""
    error = np.linalg.norm(x_approx - x_exact, np.inf)
    return error


def estimate_iterations_a_priori(tolerance, B, x1, x0):
    """Schätzt die Anzahl der Iterationen a-priori ab wie im Bild."""
    norm_B = np.linalg.norm(B, np.inf)
    diff_norm = np.linalg.norm(x1 - x0, np.inf)
    numerator = np.log(tolerance * (1 - norm_B) / diff_norm)
    denominator = np.log(norm_B)
    steps = np.ceil(numerator / denominator)
    return steps


# Matrix A und Vektor b
A = np.array([[8, 5, 2], [5, 9, 1], [4, 2, 7]])
b = np.array([19, 5, 34])
x0 = np.array([1, -1, 3])  # Startvektor
num_iterations = 5  # Anzahl der Iterationen
tolerance = 1e-4  # Gewünschte Genauigkeit

# Gauss-Seidel-Verfahren
D, L, U, DL = gauss_seidel_decomposition(A)
x_approx, history, B, c = gauss_seidel_iteration(A, b, x0, num_iterations)

# Berechnung der genauen Lösung durch NumPy
x_exact = np.linalg.solve(A, b)

# A-posteriori Fehler berechnen
a_posteriori_error = calculate_a_posteriori_error(history[3], x_exact)

# A-priori Abschätzung der Anzahl Iterationen
a_priori_iterations = estimate_iterations_a_priori(tolerance, B, history[1], history[0])

# Für den Fall, dass x^(2) als Startvektor verwendet wird
x2 = history[2]
a_priori_iterations_with_x2 = estimate_iterations_a_priori(tolerance, B, x2, history[1])

# Ergebnisse ausgeben
print("Matrix D:\n", D)
print("Matrix L (untere Dreiecksmatrix ohne Diagonale):\n", L)
print("Matrix U (obere Dreiecksmatrix ohne Diagonale):\n", U)
print("Matrix (D + L):\n", DL)

# Iterationen
print("\nIterationen:")
for i, x in enumerate(history):
    print(f"x^{i} (Gauss-Seidel) =", x)

print("\nA-posteriori Fehler (nach 3 Iterationen):", a_posteriori_error)

print("\nA-priori geschätzte Anzahl Iterationen (mit x^(0) als Startvektor):", a_priori_iterations)
print("A-priori geschätzte Anzahl Iterationen (mit x^(2) als Startvektor):", a_priori_iterations_with_x2)

# Exakte Lösung
print("\nExakte Lösung (ausgerechnet mit np.linalg.solve):", x_exact)
