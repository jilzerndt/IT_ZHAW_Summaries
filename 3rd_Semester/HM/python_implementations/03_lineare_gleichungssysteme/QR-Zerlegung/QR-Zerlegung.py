import numpy as np

# Definieren der Matrix A und des Vektors b
A = np.array([[1, -2, 3],
              [-5, 4, 1],
              [2, -1, 3]])
b = np.array([1, 9, 5])

# QR-Zerlegung durchführen
Q, R = np.linalg.qr(A)

# Lösung x berechnen mit Hilfe von Q und R
# Rx = Q^T * b (Rücksubstitution)
Q_T_b = np.dot(Q.T, b)
x = np.linalg.solve(R, Q_T_b)

# Ausgabe der Matrizen Q, R und der Lösung x
print("Matrix Q:")
print(Q)
print("\nMatrix R:")
print(R)
print("\nLösung x:")
print(x)
