import pandas
import matplotlib.pyplot as plt
import argparse
import logging
import logging.config

import settings
import consts
import clean
from math_util import *

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger('plot')
logger.info('plot.py log\n----------')

def read_data(f):
    return pandas.read_csv(f, delimiter='\t') 

def plot_raw_data(datafile):
    with open(datafile) as f:
        data = read_data(f) 
        data = clean.prettify_data(data)
        data.plot.line(x='Time', color=['r','b','g']) # TODO: check that colors match quEd controller

def plot_clean_data(datafile):
    with open(datafile) as f:
        data = read_data(f)
        data = clean.prettify_data(data)
        data = clean.clean_spikes(data)
        with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
            logger.debug(data)
        data.plot(x='Angle')
        ax = data.plot.scatter(x='Angle', y='Single 0', color='Red')
        ax = data.plot.scatter(x='Angle', y='Single 1', color='Blue', ax=ax)
        data.plot.scatter(x='Angle', y='Coincidence', color='Green', ax=ax)

parser = argparse.ArgumentParser(description='Plot quEd exmperiment results')
parser.add_argument('file', metavar='F', type=str, help='Filepath to data')
args = parser.parse_args()
logger.info('Filepath to data: ' + args.file)
plot_raw_data(args.file)
plt.title(args.file + ' (Raw Data)')
plot_clean_data(args.file)
plt.title(args.file + ' (Cleaned Spikes)')
plt.show()
