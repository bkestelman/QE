import init # Must come first

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

def clean_data(data):
    data = clean.prettify_data(data)
    data = clean.clean_spikes(data)
    return data

def plot_raw_data(data):
    data = clean.prettify_data(data)
    data.plot.line(x='Time', color=['r','b','g']) # TODO: check that colors match quEd controller

def plot_data(data):
    with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
        logger.debug(data)
    data.plot(x='Angle')
    ax = data.plot.scatter(x='Angle', y='Single 0', color='Red')
    ax = data.plot.scatter(x='Angle', y='Single 1', color='Blue', ax=ax)
    data.plot.scatter(x='Angle', y='Coincidence', color='Green', ax=ax)

def sin_func(x, a, b, c, d):
    return a*np.sin(b*x+c)+d
def cos_func(x, a, b, c, d):
    return a*np.cos(np.radians(b*x+c))+d
def cos_sq(x):
    return np.cos(x)*np.cos(x)
def cos_sq_func(x, a, b, c, d):
    return a*cos_sq(np.radians(b*x+c))+d

def plot_fit(data, fit_func, x0, logname=None):
    colors = {'Single 0': 'Red', 'Single 1': 'Blue', 'Coincidence': 'Green'}
    #for key in ['Single 0', 'Single 1', 'Coincidence']:
    key = 'Coincidence'
    fit_data = fit.fit_data(data['Angle'], data[key], fit_func, x0, logname=key+' --- '+logname)
    ax = data.plot.scatter(x='Angle', y=key, color=colors[key])
    fit_data.plot.line(x='x', y='y', color='Black', ax=ax)

def save_plot(f, data_dir):
    plt.title(f + ' (' + data_dir + ')')
    dest = data_dir + '/' + f + '.png'
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    plt.savefig(dest)
    plt.close()

if __name__ == "__main__": 
    logger.info('Filepath(s) to data: ' + str(settings.args.files))
    for f in settings.args.files: 
        data = read_data(f) # always read data first
        # raw data
        plot_raw_data(data)
        save_plot(f, settings.RAW_DATA_DIR)
        # clean data (clean spikes)
        data = clean_data(data)
        plot_data(data)
        save_plot(f, settings.CLEAN_DATA_DIR)
        # fit coincidence to cos function
        x0 = fit.autoinit_wave(data['Angle'], data['Coincidence'])
        plot_fit(data, cos_func, x0, logname=f)
        save_plot(f, settings.FIT_DATA_DIR + '/Cos')
        # fit coincidence to cos^2 function
        x0 = fit.autoinit_sq_wave(data['Angle'], data['Coincidence'])
        plot_fit(data, cos_sq_func, x0, logname=f)
        save_plot(f, settings.FIT_DATA_DIR + '/Cos_sq')
        #plt.show()

