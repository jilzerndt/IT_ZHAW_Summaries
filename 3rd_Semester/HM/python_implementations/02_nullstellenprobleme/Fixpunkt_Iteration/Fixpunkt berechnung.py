import math


def fixed_point_iteration(F, x0, epsilon, lambda_const):
    """
    Berechnet den Fixpunkt einer Funktion F(x) mit vorgegebener Genauigkeit.

    Parameter:
    F : function
        Handle der Funktion F(x).
    x0 : float
        Startwert.
    epsilon : float
        Gewünschte Genauigkeit.
    lambda_const : float
        Lipschitzkonstante (muss < 1 sein).

    Rückgabewerte:
    - Der berechnete Fixpunkt.
    - Die Anzahl der notwendigen Iterationen.
    """
    # Startwerte setzen
    x_prev = x0
    iterations = 0

    while True:
        # Neue Iteration berechnen
        x_next = F(x_prev)
        iterations += 1

        # Abbruchbedingung prüfen
        if abs(x_next - x_prev) <= (epsilon * (1 - lambda_const) / lambda_const):
            break

        # Nächste Iteration starten
        x_prev = x_next

    return x_next, iterations


# Definition der Funktion F(x)
def F(x):
    return 1 / (math.cos(x + math.pi / 4) - 1) + 2


# Parameter für die Iteration
x0 = 1.5  # Startwert im Intervall [1, 2]
epsilon = 1e-6  # Gewünschte Genauigkeit
lambda_const = 0.6703  # Lipschitzkonstante aus Teil b, hier muss man das resultat eisnetzen vom höchsten Wert der ableitung bsp. f'(1) = 0.6703 oder f'(2) = 0.0929, f'(1) ist der höchste wert

# Fixpunktberechnung
fixpunkt, anzahl_iterationen = fixed_point_iteration(F, x0, epsilon, lambda_const)

# Ergebnisse ausgeben
print(f"Fixpunkt: {fixpunkt}")
print(f"Anzahl der Iterationen: {anzahl_iterationen}")
