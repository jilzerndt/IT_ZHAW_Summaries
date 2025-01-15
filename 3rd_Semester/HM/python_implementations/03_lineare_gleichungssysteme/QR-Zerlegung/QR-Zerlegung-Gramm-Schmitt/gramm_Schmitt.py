import numpy as np

# Define the matrix A
A = np.array([[1, -2, 3],
              [-5, 1, 1],
              [2, -1, 3]], dtype=float)

# Initialize the vectors
u0 = A[:, 0]
u1 = A[:, 1]
u2 = A[:, 2]

# Perform the Gram-Schmidt process
q1 = u0 / np.linalg.norm(u0)
u1 = u1 - np.dot(u1, q1) * q1
q2 = u1 / np.linalg.norm(u1)
u2 = u2 - np.dot(u2, q1) * q1 - np.dot(u2, q2) * q2
q3 = u2 / np.linalg.norm(u2)

# Print the orthogonal vectors
print("q1:\n", q1)
print("q2:\n", q2)
print("q3:\n", q3)