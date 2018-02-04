import numpy as np
import scipy.optimize as optimization
import pandas
import logging

import settings

logger = settings.createLogger(__name__)

# Fits func to pandas DataFrame columns xdata, ydata 
# Returns two-column DataFrame with xdata, yfit (output of feeding xdata into fit function)
def fit_data(xdata, ydata, func, x0=None):
    xdata = np.array(xdata.tolist())
    ydata = np.array(ydata.tolist())
    fit = optimization.curve_fit(func, xdata, ydata, x0)
    logger.debug(fit)
    yfit = np.array(func(xdata, fit[0][0], fit[0][1], fit[0][2], fit[0][3])) # Fit function data
    return pandas.DataFrame({'x': xdata.tolist(), 'y': yfit.tolist()})
