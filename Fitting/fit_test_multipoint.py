import numpy as np
import scipy.optimize as optimization
import matplotlib.pyplot as plt

points = 2

# Function to fit
def func(x, a, b, c, d):
    return a * np.sin(b*x+c) + d

# Random noise
def noise(amount):
    return (np.random.random()-0.5)*amount

# Generate data for function with noise
xdata_base = np.array([n*np.pi/8 for n in range(16)])
xdata = np.array([n*np.pi/8 for n in range(16)] * points) # Repeat xdata 'points' times
print(xdata)
ydata = np.array([np.sin(x)+noise(1) for x in xdata])

# Fit data
fit = optimization.curve_fit(func, xdata, ydata)
print(fit) # Look at output from print to understand structure of fit object

yfit = np.array(func(xdata_base, fit[0][0], fit[0][1], fit[0][2], fit[0][3])) # Fit function data

plt.plot(xdata, ydata, 'ro') # Scatter plot of original, noisy data
plt.plot(xdata_base, yfit) # Line plot of fit function
plt.show()
