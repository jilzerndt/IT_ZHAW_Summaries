import numpy as np

# Funktionen zur Berechnung
def jacobi_decomposition(A):
    """Berechnet D, D^-1, L, R (L+U) aus der Matrix A."""
    D = np.diag(np.diag(A))  # Diagonale von A
    D_inv = np.linalg.inv(D)  # Inverse von D
    L = np.tril(A, -1)  # Untere Dreiecksmatrix ohne Diagonale
    U = np.triu(A, 1)  # Obere Dreiecksmatrix ohne Diagonale
    R = L + U  # L + U
    return D, D_inv, L, U, R


def jacobi_iteration(A, b, x0, num_iterations):
    """Führt Jacobi-Iterationen durch und speichert alle Zwischenergebnisse."""
    D, D_inv, L, U, R = jacobi_decomposition(A)
    B = -D_inv @ R  # Iterationsmatrix
    c = D_inv @ b  # Konstanter Vektor
    x = x0
    history = [x0]  # Speicherung der Zwischenergebnisse

    for _ in range(num_iterations):
        x_new = B @ x + c
        history.append(x_new)
        x = x_new

    return x, history, B, c


def calculate_a_posteriori_error(x_k, x_k_minus_1, B):
    """Berechnet den a-posteriori Fehler wie im Bild."""
    norm_B = np.linalg.norm(B, np.inf)
    error = (norm_B * np.linalg.norm(x_k - x_k_minus_1, np.inf)) / (1 - norm_B)
    return error


def calculate_a_priori_steps(tolerance, B, x1, x0):
    """Berechnet die benötigten Schritte a-priori wie im Bild."""
    norm_B = np.linalg.norm(B, np.inf)
    diff_norm = np.linalg.norm(x1 - x0, np.inf)
    numerator = np.log(tolerance * (1 - norm_B) / diff_norm)
    denominator = np.log(norm_B)
    steps = np.ceil(numerator / denominator)
    return steps


# Matrix A und Vektor b
A = np.array([[30, 10, 5], [10, 9, 1], [4, 2, 7]])
b = np.array([19, 5, 34])
x0 = np.array([1, -1, 3])  # Startvektor
num_iterations = 3  # Anzahl der Iterationen
tolerance = 1e-4  # Gewünschte Genauigkeit

# Jacobi-Verfahren
D, D_inv, L, U, R = jacobi_decomposition(A)
x_approx, history, B, c = jacobi_iteration(A, b, x0, num_iterations)

# Berechnung der genauen Lösung durch NumPy
x_exact = np.linalg.solve(A, b)

# A-posteriori Fehler nach der 3. Iteration
a_posteriori_error = calculate_a_posteriori_error(history[3], history[2], B)

# A-priori Abschätzung der Anzahl der Schritte
a_priori_steps = calculate_a_priori_steps(tolerance, B, history[1], history[0])

# Ausgabe
print("Matrix D:\n", D)
print("Matrix D^-1:\n", D_inv)
print("Matrix L (untere Dreiecksmatrix ohne Diagonale):\n", L)
print("Matrix U (obere Dreiecksmatrix ohne Diagonale):\n", U)
print("Matrix L + U:\n", R)

# Iterationen und Ergebnisse
print("\nIterationen:")
for i, x in enumerate(history):
    print(f"x^{i} =", x)

# Ergebnisse
print("\nA-posteriori Fehler:", a_posteriori_error)
print("\nA-priori geschätzte Anzahl Iterationen:", a_priori_steps)

# Exakte Lösung ausgeben
print("\nExakte Lösung (ausgerechnet mit np.linalg.solve):", x_exact)
