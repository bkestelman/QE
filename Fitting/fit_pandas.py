import numpy as np
import scipy.optimize as optimization
import pandas
import logging
import string

import settings
import physics_util

logger = settings.createLogger(__name__)

y_per_x = 5

# Fits func to pandas DataFrame columns xdata, ydata 
# Returns two-column DataFrame with xdata, yfit (output of feeding xdata into fit function)
def fit_data(xdata, ydata, func, x0=None, logname=None):
    xdata = np.array(xdata.tolist())
    ydata = np.array(ydata.tolist())
    fit = optimization.curve_fit(func, xdata, ydata, x0)
    logger.debug('***' + logname)
    logger.debug(str(func))
    alphabet = string.ascii_lowercase
    for param in range(len(x0)):
        logger.debug(alphabet[param] + '=' + str(fit[0][param]) + ' init=' + str(x0[param]))
    #yfit = np.array(func(xdata, fit[0][0], fit[0][1])) # Fit function data
    yfit = np.array(func(xdata, *fit[0]))
    return pandas.DataFrame({'x': xdata.tolist(), 'y': yfit.tolist()})

def auto_phase(ydata):
    period = 180
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
    return c

def autoinit_wave(xdata, ydata):
    a = (ydata.max() - ydata.min()) / 2
    #b = 1
    period = 180
    b = physics_util.omega(np.radians(period))
    c = auto_phase(ydata)
    d = ydata.mean()
    #d = 0 # for sq trig functions, 0 makes more sense
    logger.debug('autoinit ' + str([a, b, c, d]))
    return [a, b, c, d]

def autoinit_sq_wave(xdata, ydata):
    a = ydata.max()-ydata.min()
    #c = auto_phase(ydata)
    b = 1
    c = auto_phase(ydata) 
    d = 0
    return [a, b, c, d]
