import numpy as np
from scipy.linalg import lu

# Definieren der Matrix A und Vektor b
A = np.array([[0.8, 2.2, 3.6],
              [2.0, 3.0, 4.0],
              [1.2, 2.0, 5.8]])

b = np.array([2.4, 1.0, 4.0])

# Setzen der Druckoptionen für NumPy Arrays
np.set_printoptions(formatter={'float': '{: 0.2f}'.format})

# LU-Zerlegung durchführen
P, L, U = lu(A)

# Ausgabe der Permutationsmatrix P, unteren Dreiecksmatrix L und oberen Dreiecksmatrix U
print("Permutationsmatrix P:\n", P)
print("Untere Dreiecksmatrix L:\n", L)
print("Obere Dreiecksmatrix U:\n", U)

# Lösung des Systems Ax = b mithilfe der Zerlegung
# Anwenden der Permutationsmatrix auf b
b_permuted = np.dot(P, b)

# Vorwärtseinsetzen, um y zu lösen mit Ly = Pb
y = np.linalg.solve(L, b_permuted)

# Rückwärtseinsetzen, um x zu lösen mit Ux = y
x = np.linalg.solve(U, y)

# Lösung x anzeigen
print("Lösung des Systems Ax = b:\n", x)
