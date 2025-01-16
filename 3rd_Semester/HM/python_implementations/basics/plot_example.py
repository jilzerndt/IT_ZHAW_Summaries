import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-10, 10, 400)

y = (x**5) - (5*x**4) - (30*x**3) + (110*x**2) + 29*x - 105

dy = (5*x**4) - (20*x**3) - (90*x**2) + (220*x) + 29

F = (1/6)*x**6 - (1/5)*x**5 - (15/4)*x**4 + (110/3)*x**3 + (29/2)*x**2 - 105*x

plt.figure(figsize=(10, 6))
plt.plot(x, y, label='$f(x) = x^5 - 5x^4 - 30x^3 + 110x^2 + 29x - 105$')
plt.plot(x, dy, label="Ableitung $f'(x)$", linestyle='--')
plt.plot(x, F, label="Stammfunktion $F(x)$", linestyle=':')

plt.title("Funktion, ihre Ableitung und Stammfunktion")
plt.xlabel("x-Achse")
plt.ylabel("y-Achse")
plt.xlim(-10, 10)
plt.ylim(-1000, 1000)
plt.grid(True)
plt.legend()
plt.show()
