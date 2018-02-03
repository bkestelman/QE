import numpy as np
import scipy.optimize as optimization
import matplotlib.pyplot as plt

def func(x, a, b, c, d):
    return a * np.sin(b*x+c) + d

def noise(amount):
    return (np.random.random()-0.5)*amount

xdata = np.array([n*np.pi/8 for n in range(8)])
ydata = np.array([np.sin(x)+noise(1) for x in xdata])

fit = optimization.curve_fit(func, xdata, ydata)
print(fit)

yfit = np.array(func(xdata, fit[0][0], fit[0][1], fit[0][2], fit[0][3]))

plt.plot(xdata, ydata, 'ro')
plt.plot(xdata, yfit)
plt.show()
