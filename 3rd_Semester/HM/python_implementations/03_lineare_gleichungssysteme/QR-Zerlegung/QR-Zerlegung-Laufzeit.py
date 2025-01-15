import numpy as np
import timeit

def manual_qr_decomposition(A):
    A = A.astype(np.float64)  # Konvertiere A zu float64, um sicherzustellen, dass alle Operationen als float ausgeführt werden
    m, n = A.shape
    Q = np.zeros((m, n), dtype=np.float64)
    R = np.zeros((n, n), dtype=np.float64)
    for k in range(n):
        u = np.copy(A[:, k])
        for i in range(k):
            proj = np.dot(Q[:, i], A[:, k]) * Q[:, i]
            u -= proj
        R[k, k] = np.linalg.norm(u)
        Q[:, k] = u / R[k, k]
        for j in range(k+1, n):
            R[k, j] = np.dot(Q[:, k], A[:, j])
            A[:, j] -= R[k, j] * Q[:, k]
    return Q, R

# Matrix A aus Aufgabe 1, explizit als float
A = np.array([[1, -2, 3],
              [-5, 4, 1],
              [2, -1, 3]], dtype=np.float64)

# Zeitmessung für die eigene QR-Zerlegung
t1 = timeit.repeat("manual_qr_decomposition(A)", "from __main__ import manual_qr_decomposition, A", number=100)
avg_t1 = np.average(t1) / 100

# Zeitmessung für die eingebaute QR-Zerlegung von numpy
t2 = timeit.repeat("np.linalg.qr(A)", "from __main__ import np, A", number=100)
avg_t2 = np.average(t2) / 100

print(f"Average time for manual QR decomposition: {avg_t1} seconds")
print(f"Average time for numpy.linalg.qr(): {avg_t2} seconds")
