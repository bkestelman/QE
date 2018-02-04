import init

import pandas
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as optimization
import argparse
import logging
import logging.config
import os

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
    return a*np.cos(b*x+c)+d

def plot_fit(data, filename=None):
    data = clean.prettify_data(data)
    data = clean.clean_spikes(data)
    colors = {'Single 0': 'Red', 'Single 1': 'Blue', 'Coincidence': 'Green'}
    for key in ['Single 0', 'Single 1', 'Coincidence']:
        x0 = fit.autoinit_wave(data['Angle'], data[key])
        fit_data = fit.fit_data(data['Angle'], data[key], cos_func, x0)
        ax = data.plot.scatter(x='Angle', y=key, color=colors[key])
        fit_data.plot.line(x='x', y='y', color='Black', ax=ax)
        if filename is not None:
            dest = settings.RESULTS_DIR + '/' + filename + '_' + key.replace(' ', '_') + '.png'
            logger.debug('saving to ' + dest)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            plt.savefig(dest)

parser = argparse.ArgumentParser(description='Plot quEd exmperiment results')
parser.add_argument('files', metavar='F', type=str, nargs='+', help='Filepath(s) to data')
args = parser.parse_args()
logger.info('Filepath(s) to data: ' + str(args.files))
for f in args.files:
    data = read_data(f) 
    #plot_raw_data(data)
    #plt.title(args.file + ' (Raw Data)')
    #plot_clean_data(data)
    #plt.title(args.file + ' (Cleaned Spikes)')
    plot_fit(data, filename=f)
    #plt.show()

