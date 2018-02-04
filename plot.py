import init

import pandas
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as optimization
import argparse
import logging
import logging.config

import settings
import consts
import clean
import Fitting.fit_pandas as fit
import physics_util

logger = settings.createLogger(__name__)
logger.info('plot.py log\n----------')

def read_data(datafile):
    with open(datafile) as f:
        return pandas.read_csv(f, delimiter='\t') 

def plot_raw_data(data):
    data = clean.prettify_data(data)
    data.plot.line(x='Time', color=['r','b','g']) # TODO: check that colors match quEd controller

def plot_clean_data(data):
    data = clean.prettify_data(data)
    data = clean.clean_spikes(data)
    with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
        logger.debug(data)
    data.plot(x='Angle')
    ax = data.plot.scatter(x='Angle', y='Single 0', color='Red')
    ax = data.plot.scatter(x='Angle', y='Single 1', color='Blue', ax=ax)
    data.plot.scatter(x='Angle', y='Coincidence', color='Green', ax=ax)

def func(x, a, b, c, d):
    return a * np.sin(b*x+c) + d

def sin_func(x, a, b, c, d):
    return a*np.sin(b*x)+d
def cos_func(x, a, b, c, d):
    return a*np.cos(b*x)+d

def plot_fit(data):
    data = clean.prettify_data(data)
    data = clean.clean_spikes(data)
    x0 = np.array([2000, physics_util.omega(period=200), 0, 18000])
    fit_data = fit.fit_data(data['Angle'], data['Single 1'], cos_func, x0)
    ax = data.plot.scatter(x='Angle', y='Single 1', color='Blue')
    fit_data.plot.line(x='x', y='y', color='Black', ax=ax)

parser = argparse.ArgumentParser(description='Plot quEd exmperiment results')
parser.add_argument('file', metavar='F', type=str, help='Filepath to data')
args = parser.parse_args()
logger.info('Filepath to data: ' + args.file)
data = read_data(args.file) 
plot_raw_data(data)
plt.title(args.file + ' (Raw Data)')
plot_clean_data(data)
plt.title(args.file + ' (Cleaned Spikes)')
plot_fit(data)
plt.show()

