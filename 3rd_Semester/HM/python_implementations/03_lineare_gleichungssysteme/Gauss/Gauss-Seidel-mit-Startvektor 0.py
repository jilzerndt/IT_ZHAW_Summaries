import numpy as np

def gauss_seidel(A, b, x0, iterations):
    """
    Führt das Gauss-Seidel-Verfahren durch, um ein lineares Gleichungssystem Ax = b zu lösen.

    Parameter:
    A : numpy.ndarray
        Koeffizientenmatrix.
    b : numpy.ndarray
        Konstantenvektor.
    x0 : numpy.ndarray
        Startvektor.
    iterations : int
        Anzahl der Iterationen.

    Rückgabewerte:
    - Vektor der Lösungen nach den angegebenen Iterationen.
    - Liste der Iterationsschritte.
    """
    n = len(b)
    x = x0.copy()
    steps = []

    for _ in range(iterations):
        x_new = x.copy()
        for i in range(n):
            sum1 = sum(A[i][j] * x_new[j] for j in range(i))  # Summen für bereits aktualisierte Werte
            sum2 = sum(A[i][j] * x[j] for j in range(i + 1, n))  # Summen für nicht aktualisierte Werte
            if A[i][i] == 0:
                raise ValueError("Das Diagonalelement der Matrix ist 0. Eine Umordnung der Matrix ist erforderlich.")
            x_new[i] = (b[i] - sum1 - sum2) / A[i][i]
        x = x_new
        steps.append(x.copy())

    return x, steps


# Umgeformte Matrix A (diagonaldominant)
A = np.array([
    [10, -4, -2],
    [-4, 10, -4],
    [-6, -2, 12]
], dtype=float)

# Konstantenvektor b
b = np.array([2, 3, 1], dtype=float)

# Startvektor x0
x0 = np.zeros(3)

# Anzahl der Iterationen
iterations = 3

# Gauss-Seidel-Verfahren anwenden
try:
    solution, steps = gauss_seidel(A, b, x0, iterations)

    # Ergebnisse ausgeben
    print("Lösung nach x Iterationen:")
    print(solution)
    print("\nIterationsschritte:")
    for i, step in enumerate(steps):
        print(f"Schritt {i + 1}: {step}")
except ValueError as e:
    print(e)
