import numpy as np

# Defining the iteration function as given in the problem statement
def iteration_function(x):
    return (0.5 *2**x)

# Initial conditions
x0 = 1.5
tolerance = 1e-8
max_iterations = 1000

# Function to perform fixed point iteration
def fixed_point_iteration(x0, tolerance, max_iterations):
    x = x0
    results = []
    for i in range(max_iterations):
        x_next = iteration_function(x)
        results.append((i + 1, x, x_next, abs(x_next - x)))
        if abs(x_next - x) < tolerance:
            return x_next, i + 1, results
        x = x_next
    return x, max_iterations, results

# Performing the fixed point iteration
fixed_point, num_iterations, iteration_results = fixed_point_iteration(x0, tolerance, max_iterations)

# Printing results
for result in iteration_results:
    print(f"Iteration {result[0]}: x = {result[1]:.10f}, x_next = {result[2]:.10f}, Error = {result[3]:.10f}")

print(f"\nFixed point: {fixed_point:.10f} reached after {num_iterations} iterations with an error threshold of {tolerance}.")
