import numpy as np

# Gegebene Matrix A
A = np.array([
    [1, 1, 0],
    [3, -1, 2],
    [2, -1, 3]
])

# Startvektor
x = np.array([1, 0, 0], dtype=float)

# Toleranz und maximale Iterationen
tolerance = 1e-4
max_iterations = 1000


# von-Mises-Iteration
def von_mises_iteration(A, x, tolerance, max_iterations):
    x = x / np.linalg.norm(x)  # Normieren des Startvektors
    for k in range(max_iterations):
        x_next = np.dot(A, x)  # Matrix-Vektor-Multiplikation
        x_next = x_next / np.linalg.norm(x_next)  # Normieren des neuen Vektors

        # Abbruchbedingung
        if np.linalg.norm(x_next - x) < tolerance:
            break

        x = x_next

    # Berechnung des zugehörigen Eigenwerts
    eigenvalue = np.dot(x.T, np.dot(A, x)) / np.dot(x.T, x)
    return eigenvalue, x, k + 1


# Berechnung des Eigenwerts und Eigenvektors
eigenvalue, eigenvector, iterations = von_mises_iteration(A, x, tolerance, max_iterations)

# Überprüfung mit np.linalg.eig
eigenvalues, eigenvectors = np.linalg.eig(A)

# Ausgabe
print(f"Berechneter größter Eigenwert: {eigenvalue}")
print(f"Zugehöriger Eigenvektor: {eigenvector}")
print(f"Anzahl Iterationen: {iterations}")
print("\nÜberprüfung mit numpy.linalg.eig:")
print(f"Eigenwerte: {eigenvalues}")
print(f"Eigenvektoren: \n{eigenvectors}")
