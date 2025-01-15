import numpy as np

# Example of a function f(x)
def f(x):
    return x*np.e**x  # Example: sine function

# Function to calculate the numerical derivative
def numerical_derivative(f, x, epsilon=1e-6):
    return (f(x + epsilon) - f(x - epsilon)) / (2 * epsilon)

def konditionszahl(x):
    # Calculate the condition number K
    f_x = f(x)
    f_prime_x = numerical_derivative(f, x)
    return abs(f_prime_x) * abs(x) / abs(f_x)

# Test with a specific value of x
x_value = (np.pi/3)  # Example value for x, gem. aufgabenstellung anpassen
k_value = konditionszahl(x_value)
print(f'Condition number K at x = {x_value}: {k_value}')