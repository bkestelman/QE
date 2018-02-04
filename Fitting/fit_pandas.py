import numpy as np
import scipy.optimize as optimization
import pandas
import logging

import settings
import physics_util

logger = settings.createLogger(__name__)

y_per_x = 5

# Fits func to pandas DataFrame columns xdata, ydata 
# Returns two-column DataFrame with xdata, yfit (output of feeding xdata into fit function)
def fit_data(xdata, ydata, func, x0=None):
    xdata = np.array(xdata.tolist())
    ydata = np.array(ydata.tolist())
    fit = optimization.curve_fit(func, xdata, ydata, x0)
    logger.debug(fit)
    yfit = np.array(func(xdata, fit[0][0], fit[0][1], fit[0][2], fit[0][3])) # Fit function data
    return pandas.DataFrame({'x': xdata.tolist(), 'y': yfit.tolist()})

def autoinit_wave(xdata, ydata):
    a = (ydata.max() - ydata.min()) / 2
    period = 180 # Guess
    b = physics_util.omega(period=period) # TODO: Should this be in degrees?
    diffs = [abs(val) for val in [ydata.max()-ydata[0], ydata.mean()-ydata[0], ydata.min()-ydata[0]]]
    min_diff_idx = diffs.index(min(diffs))
    if min_diff_idx == 0:
        c = 0 # First element is max -> 0 phase shift (for cos wave)
    elif min_diff_idx == 2:
        c = period / 2 # First element is min -> period/2 phase shift (cos)
    else:
        # First element is in middle, check if going up or down
        if ydata[1] > ydata[0]:
            c = -period/4
        else:
            c = period/4
    d = ydata.mean()
    logger.debug('autoinit ' + str([a, b, c, d]))
    return np.array([a, b, c, d])
