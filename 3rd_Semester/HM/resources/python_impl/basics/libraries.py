"""
Basic utility functions and library overview for numerical computations.
Demonstrates key functions from math and numpy libraries.
"""

import numpy as np
import math
import sympy as sp
from typing import Union, List, Tuple, Callable
import matplotlib.pyplot as plt

x = 1
y = 2
z = 3


"""
math library
important functions:
"""
math.sqrt(x) # square root of x 
math.exp(x) # e^x
math.log(x) # ln(x)
math.log10(x) # log10(x)
math.sin(x) # sin(x)
math.cos(x) # cos(x)
math.tan(x) # tan(x)
math.asin(x) # arcsin(x)
math.acos(x) # arccos(x)
math.atan(x) # arctan(x)
math.degrees(x) # convert x from radians to degrees
math.radians(x) # convert x from degrees to radians
math.pi # pi
math.e # e

"""
numpy library
important functions:
"""
np.array([1, 2, 3]) # create an array
np.zeros(3) # create an array of zeros
np.ones(3) # create an array of ones
np.arange(3) # create an array from 0 to 3
np.linspace(0, 1, 5) # create an array from 0 to 1 with 5 elements
np.eye(3) # create an identity matrix of size 3x3
np.diag([1, 2, 3]) # create a diagonal matrix with the given diagonal

"""
operations on arrays: (elementwise)
"""
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
a + b # elementwise addition
a - b # elementwise subtraction
a * b # elementwise multiplication
a / b # elementwise division
a ** 2 # elementwise exponentiation

np.sum(a) # sum of all elements
np.mean(a) # mean of all elements
np.min(a) # minimum of all elements
np.max(a) # maximum of all elements
np.argmin(a) # index of the minimum element
np.argmax(a) # index of the maximum element

np.abs(a) # absolute values of all elements
np.round(a) # round all elements
np.floor(a) # round down all elements
np.ceil(a) # round up all elements

np.sqrt(a) # square root of all elements
np.exp(a) # e^x of all elements
np.log(a) # ln(x) of all elements
np.sin(a) # sin(x) of all elements
np.cos(a) # cos(x) of all elements

"""
Matrix and Vector operations:
"""
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
C = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) 
v = np.array([1, 2, 3])

A + B # elementwise addition
A - B # elementwise subtraction
A * B # elementwise multiplication / scalar multiplication
A / B # elementwise division
A @ B # matrix multiplication
np.matmul(A, B) # matrix multiplication
np.dot(a, b) # dot product
np.cross(a, b) # cross product

A2 = np.copy(A) # copy of A
np.transpose(A) # transpose of A
np.linalg.inv(A) # inverse of A
np.linalg.det(A) # determinant of A
np.linalg.eig(A) # eigenvalues and eigenvectors of A

np.linalg.norm(v) # Euklidean norm of a vector
np.linalg.norm(A, ord=1) # L1 norm of a matrix (Vektor auf Länge 1 normiert)
np.linalg.norm(A) # Frobenius norm of a matrix

np.linalg.solve(A, v) # solve the linear system Ax = v
np.linalg.lstsq(A, v) # least squares solution of Ax = v
np.roots([1, 2, 1]) # roots of the polynomial x^2 + 2x + 1
np.interp(2.5, [1, 2, 3], [4, 5, 6]) # linear interpolation

"""
sympy library
"""

def f(x):
    return x**2

def h(x):
    return np.sin(x)

arr = np.array([1, 2, 3])

sp.symbols('x') # create a symbol: use x = sp.symbols('x') and then use x in the function
sp.diff(f(x), x) # differentiate f(x) with respect to x
sp.integrate(f(x), x) # integrate f(x) with respect to x
sp.solve(f(x), x) # solve f(x) = 0 for x
sp.limit(f(x), x, 0) # limit of f(x) as x approaches 0
sp.series(f(x), x) # Taylor series of f(x) around x = 0


"""
matplotlib library
"""

plt.plot(arr, f(arr)) # plot f(arr) against arr
plt.plot(f(arr)) # plot f(arr) against the index of arr
plt.scatter(arr, f(arr)) # scatter plot of f(arr) against arr
plt.hist(arr) # histogram of arr
plt.bar(arr, f(arr)) # bar plot of f(arr) against arr
plt.pie(arr) # pie chart of arr

plt.xlabel('x-axis') # label for the x-axis
plt.ylabel('y-axis') # label for the y-axis
plt.title('title') # title of the plot
plt.legend(['f(x)']) # legend for the plot
plt.show() # show the plot



# Type aliases - idk if you're allowed to use this
Number = Union[int, float]
Vector = List[Number]
Matrix = List[List[Number]]




