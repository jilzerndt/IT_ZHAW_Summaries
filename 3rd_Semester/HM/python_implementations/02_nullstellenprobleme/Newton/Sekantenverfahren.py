import numpy as np
import matplotlib.pyplot as plt
import math

# Definiere die Funktion f(x)
def f(x):
    return math.exp(x**2) + x**(-3) - 10

# Definiere die Ableitung von f(x)
def f_prime(x):
    return 2 * x * math.exp(x**2) - 3 * x**(-4)

# Implementiere das Newton-Verfahren
def newton_verfahren(f, f_prime, x0, iterations):
    xn = x0
    for _ in range(iterations):
        xn = xn - f(xn) / f_prime(xn)
    return xn

# Implementiere das Sekantenverfahren
def sekanten_verfahren(f, x0, x1, iterations):
    for _ in range(iterations):
        if f(x1) - f(x0) == 0:
            raise ZeroDivisionError("Division durch Null")
        x_temp = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        x0, x1 = x1, x_temp
    return x1

# Skizzieren der Funktion
x_vals = np.linspace(-3, 3, 400)
y_vals = [f(x) for x in x_vals]
plt.figure(figsize=(8, 4))
plt.plot(x_vals, y_vals, label='f(x) = $e^{x^2} + x^{-3} - 10$')
plt.axhline(0, color='red', lw=0.5)
plt.grid(True)
plt.legend()
plt.title('Plot der Funktion $f(x)$')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.show()

# Newton-Verfahren Anwendung
newton_result = newton_verfahren(f, f_prime, 0.5, 4)
print("Newton-Verfahren bei x0 = 0.5, Ergebnis: {:.4f}".format(newton_result))

# Sekantenverfahren Anwendung
sekanten_result = sekanten_verfahren(f, -1.0, -1.2, 4)
print("Sekantenverfahren mit Startwerten -1.0 und -1.2, Ergebnis: {:.4f}".format(sekanten_result))
