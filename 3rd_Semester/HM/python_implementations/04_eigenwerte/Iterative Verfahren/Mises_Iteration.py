# -*- coding: utf-8 -*-
"""
Loesung Aufgabe 6

Created on Sun Jan  3 13:17:53 2021

@author: beer
"""

import numpy as np
import matplotlib.pyplot as plt
#Eingabe gemäss aufgabe
A = np.array([[13, -4],
              [30, -9]], dtype=np.float64)

"""
Aufgabe a):
-----------

Das charakteristische Polynom lautet: p(x) = x^2 - 4x + 3 = (x - 3)(x - 1).

Der Eigenraum zum Eigenwert 3 lautet: {x = a*(2, 5)^T; a in R}.

Der Eigenraum zum Eigenwert 1 lautet: {x = a*(1, 3)^T; a in R}.
"""

"""
Aufgabe b):
-----------

Aus a) und der Normierungsbedingung für die Spalten von T ergibt sich:
"""

T = np.array([[2 / np.sqrt(29), 1 / np.sqrt(10)],
              [5 / np.sqrt(29), 3 / np.sqrt(10)]], dtype=np.float64)

D = np.array([[3, 0],
              [0, 1]], dtype=np.float64)

print("T = ", T)
print("D = ", D)
print("T^-1*A*T = ", np.linalg.inv(T) @ A @ T)

"""
Aufgabe c):
-----------
"""

v = np.array([[1, 0]], dtype=np.float64).transpose()

max_iter = 40
err_l = np.zeros([max_iter, 1], dtype=np.float64)

for k in range(max_iter):
    v = A @ v / np.linalg.norm(A @ v)
    l = v.transpose() @ A @ v / (v.transpose() @ v)
    err_l[k] = np.abs(l - D[0, 0])

print("v = ", v)
print("lambda = ", l)

plt.figure(1)
plt.semilogy(err_l)
plt.grid()
plt.show()
