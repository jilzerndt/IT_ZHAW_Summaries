import numpy as np


# Definieren Sie hier die Funktionen f(x) und h(x)
def f(x):
    return np.exp(x)  # g(x) = e^x


def h(x):
    return np.sqrt(x) + 2  # h(x) = sqrt(x) + 2


# Funktion zur Berechnung der Differenz
def diff_function(x):
    return h(x) - f(x)


# Newton's method implementation, including automatic derivative calculation
def newton_method(x0, tolerance, max_iterations, func):
    epsilon = 1e-6  # Epsilon für numerische Ableitung

    def numerical_derivative(x):
        return (func(x + epsilon) - func(x - epsilon)) / (2 * epsilon)

    x = x0
    for i in range(max_iterations):
        f_x = func(x)
        df_x = numerical_derivative(x)  # Automatische Berechnung der Ableitung
        if df_x == 0 or np.isnan(df_x):
            raise ValueError("Derivative zero or undefined at x = {}".format(x))
        x_next = x - f_x / df_x
        if abs(x_next - x) < tolerance:
            return x_next, i + 1
        x = x_next
    return x, max_iterations


# Initial conditions, x= muss gem aufgabenstellung angepasst werden
x0 = 1.0  # Startwert
tolerance = 1e-7  # Toleranz für die Konvergenz
max_iterations = 1000  # Maximale Anzahl an Iterationen

# Execute Newton's method
root, iterations = newton_method(x0, tolerance, max_iterations, diff_function)

print(f"Root: {root:.10f}, Iterations: {iterations}")
