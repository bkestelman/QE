import pandas
import matplotlib.pyplot as plt
import numpy
import scipy.optimize as optimization
import argparse
import logging
import logging.config

import settings
import consts
import clean

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger('plot')
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
    return a * numpy.sin(b*x+c) + d

def plot_fit(data):
    data = clean.prettify_data(data)
    data = clean.clean_spikes(data)
    xdata = numpy.array(data['Angle'].tolist())
    ydata = numpy.array(data['Single 1'].tolist())
    x0 = numpy.array([0, 0, 0, 0])
    print(optimization.curve_fit(func, xdata, ydata, x0))

parser = argparse.ArgumentParser(description='Plot quEd exmperiment results')
parser.add_argument('file', metavar='F', type=str, help='Filepath to data')
args = parser.parse_args()
logger.info('Filepath to data: ' + args.file)
data = read_data(args.file) 
plot_raw_data(data)
plt.title(args.file + ' (Raw Data)')
plot_clean_data(data)
plt.title(args.file + ' (Cleaned Spikes)')
#plt.show()

plot_fit(data)
