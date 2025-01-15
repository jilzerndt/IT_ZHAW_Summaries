import sympy as sp
import math

# Definiere die Funktion f(x) und deren Ableitung
x = sp.Symbol('x')
f = 0.5 * 2**x
f_prime = sp.diff(f, x)

# Intervall I = [0.5, 1.5]
a, b = 0.5, 1.5

# 1. Überprüfen des Banachschen Fixpunktsatzes
# Prüfe, ob f(I) ⊆ I
f_I = [f.subs(x, a).evalf(), f.subs(x, b).evalf()]
print(f"f(a) = {f_I[0]:.10f}, f(b) = {f_I[1]:.10f}")
if all(a <= val <= b for val in f_I):
    print("f bildet I in sich ab.")
else:
    print("f bildet I nicht in sich ab.")

# Berechne die Lipschitz-Konstante λ
# Lipschitz-Konstante ist das Maximum von |f'(x)| im Intervall [0.5, 1.5]
f_prime_vals = [f_prime.subs(x, a).evalf(), f_prime.subs(x, b).evalf()]
lambda_ = max(abs(val) for val in f_prime_vals)
print(f"Lipschitz-Konstante λ = {lambda_:.10f}")

# 2. A-priori-Fehler und maximale Iterationsanzahl
epsilon = 1e-8  # gewünschte Genauigkeit
x0 = 1.5        # Startwert, wert den man bei der ablieutn iengibt um banach zu überprüfen

# Maximale Anzahl der Iterationen
n_max = math.ceil(math.log(epsilon * (1 - lambda_)) / math.log(lambda_))
print(f"Maximale Iterationsanzahl für gewünschte Genauigkeit: {n_max}")

# Iterative Berechnung des Fixpunkts
x_n = x0
for i in range(n_max):
    x_n = f.subs(x, x_n).evalf()
    print(f"Iteration {i+1}: x_n = {x_n}")

print(f"Fixpunkt (geschätzt): {x_n}")
