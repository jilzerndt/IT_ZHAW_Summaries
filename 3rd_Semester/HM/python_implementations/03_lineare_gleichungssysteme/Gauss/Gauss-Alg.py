import numpy as np


def gauss_elimination(A, b):
    n = len(b)
    # Vorwärtseradikation zur Transformation in obere Dreiecksform
    for i in range(n):
        # Pivotisierung: Suche das größte Element in der i-ten Spalte
        max_row = np.argmax(np.abs(A[i:, i])) + i
        # Tausche die aktuelle Zeile mit der Zeile des größten Pivotelements
        A[[i, max_row]] = A[[max_row, i]]
        b[[i, max_row]] = b[[max_row, i]]

        # Stelle sicher, dass das Pivot-Element nicht Null ist
        if A[i, i] == 0:
            raise ValueError("Matrix ist singulär und kann nicht gelöst werden.")

        # Eliminationsschritt
        for j in range(i + 1, n):
            factor = A[j, i] / A[i, i]
            A[j, i:] = A[j, i:] - factor * A[i, i:]
            b[j] = b[j] - factor * b[i]

    # Rücksubstitution zur Lösung des Gleichungssystems
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        sum_ax = 0
        for j in range(i + 1, n):
            sum_ax += A[i, j] * x[j]
        x[i] = (b[i] - sum_ax) / A[i, i]
    return x


# Definition der Koeffizientenmatrix und des Lösungsvektors aus deinem Bild
A = np.array([[240, 120, 80],
              [60, 180, 170],
              [60, 90, 500]], dtype=float)
b = np.array([3080, 4070, 5030], dtype=float)

x = gauss_elimination(A, b)
print("Lösung des Gleichungssystems:")
print(x)
