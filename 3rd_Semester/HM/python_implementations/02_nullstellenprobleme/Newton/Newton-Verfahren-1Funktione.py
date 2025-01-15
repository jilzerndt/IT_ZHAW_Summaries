import numpy as np
import math

# Definieren Sie hier Ihre Funktion f(x)
def f(x):
    return np.sqrt(x) + 2-np.exp(x) # Beispiel für eine Funktion

# Funktion zur Berechnung der numerischen Ableitung
def numerical_derivative(f, x, epsilon=1e-6):
    return (f(x + epsilon) - f(x - epsilon)) / (2 * epsilon)

# Newton's method implementation
def newton_method_auto_derivative(x0, tolerance, max_iterations, func):
    x = x0
    for i in range(max_iterations):
        f_x = func(x)
        df_x = numerical_derivative(func, x)
        if df_x == 0 or np.isnan(df_x):
            raise ValueError("Derivative zero or undefined at x = {}".format(x))
        x_next = x - f_x / df_x
        if abs(x_next - x) < tolerance:
            return x_next, i + 1
        x = x_next
    return x, max_iterations

# Initial conditions, x= muss gem aufgabenstellung angepasst werden
x0 = 0.5  # Startwert
tolerance = 1e-7  # Toleranz für die Konvergenz
max_iterations = 1000  # Maximale Anzahl an Iterationen

# Execute Newton's method
root, iterations = newton_method_auto_derivative(x0, tolerance, max_iterations, f)

print(f"Root: {root:.10f}, Iterations: {iterations}")
