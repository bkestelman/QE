import init # Must come first

import pandas
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as optimization
import argparse
import logging
import logging.config
import os
import re

import settings
import consts
import clean
import Fitting.fit_pandas as fit
import Fitting.functions as func
import physics_util
import analysis

logger = settings.createLogger(__name__)
logger.info('plot.py log\n----------')
plt.rcParams.update({'font.size': 16})

def read_data(datafile):
    with open(datafile) as f:
        return pandas.read_csv(f, delimiter='\t') 

def clean_data(data, clean_keys=None, clean_ranges=None):
    data = clean.prettify_data(data)
    data = clean.clean_spikes(data, clean_keys=clean_keys, clean_ranges=clean_ranges)
    return data

def plot_raw_data(data):
    data = clean.prettify_data(data)
    data.plot.line(x='Time', color=['r','b','g'], legend=None) # TODO: check that colors match quEd controller
    plt.ylabel('Photon counts/sec')
    plt.tight_layout()

def plot_data(data):
    with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
        logger.debug(data)
    data.plot(x='Angle')
    ax = data.plot.scatter(x='Angle', y='Single 0', color='Red')
    ax = data.plot.scatter(x='Angle', y='Single 1', color='Blue', ax=ax)
    data.plot.scatter(x='Angle', y='Coincidence', color='Green', ax=ax)
    plt.ylabel('Photon counts/sec')
    plt.tight_layout()

def plot_fit(data, fit_func, x0, logname=None):
    colors = {'Single 0': 'Red', 'Single 1': 'Blue', 'Coincidence': 'Green'}
    #for key in ['Single 0', 'Single 1', 'Coincidence']:
    key = 'Coincidence'
    fit_data = fit.fit_data(data['Angle'], data[key], fit_func, x0, logname=key+' --- '+logname)
    ax = data.plot.scatter(x='Angle', y=key, color=colors[key])
    fit_data.plot.line(x='x', y='y', color='Black', ax=ax, legend=None)
    plt.ylabel('Photon counts/sec')
    plt.xlabel('Angle')
    plt.tight_layout()

def save_plot(f, data_dir):
    #plt.title(f + ' (' + data_dir + ')')
    dest = data_dir + '/' + f + '.png'
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    plt.savefig(dest)
    plt.close()

def alpha(f):
    alphas = [0, 45, 90, 135]
    for a in alphas:
        if f.find('a' + str(a)) >= 0:
            return a

def fix_guess(f, x0):
    x0[2] = 0
    return x0

def minCoincidenceAvg(data):
    smallest = -1 
    angle_coincidence = 0
    angle = -10 
    for i in range(len(data['Coincidence'])):
        if i % 5 == 0:
            angle += 10
            if angle_coincidence / 5 < smallest or smallest < 0:
                smallest = angle_coincidence
        angle_coincidence += data['Coincidence'][i]
    return smallest
def maxCoincidenceAvg(data):
    biggest = -1 
    angle_coincidence = 0
    angle = -10 
    for i in range(len(data['Coincidence'])):
        if i % 5 == 0:
            angle += 10
            if angle_coincidence / 5 > biggest or biggest < 0:
                biggest = angle_coincidence
        angle_coincidence += data['Coincidence'][i]
    return biggest 
def visibilityAvg(data):
    max_c = maxCoincidenceAvg(data)
    min_c = minCoincidenceAvg(data)
    return (max_c - min_c) / (max_c + min_c) * 100

def minCoincidence(data):
    return min(data['Coincidence'].tolist())
def maxCoincidence(data):
    return max(data['Coincidence'].tolist())
def visibility(data):
    max_c = maxCoincidence(data)
    min_c = minCoincidence(data)
    return (max_c - min_c) / (max_c + min_c) * 100

if __name__ == "__main__": 
    logger.info('Filepath(s) to data: ' + str(settings.args.files))
    for f in settings.args.files: 
        print("reading file", f)
        logger.info("reading file" + str(f))
        data = read_data(f) # always read data first
        # raw data
        plot_raw_data(data)
        save_plot(f, settings.RAW_DATA_DIR)
        if settings.args.task == 'raw':
            continue
        # clean data (clean spikes)
        ck = ['Single 0']
        cr = [360]
        if 'Part1_a0' in f:
            ck = ['Coincidence', 'Single 0']
            cr = [90, 360]
        data = clean_data(data, clean_keys=ck, clean_ranges=cr)
        plot_data(data)
        save_plot(f, settings.CLEAN_DATA_DIR)

        analysis.errorData(data, x='Angle', y=['Coincidence', 'Single 0', 'Single 1'], title=f)

        if settings.args.task == 'clean':
            continue

        if 'Part1' not in f:
            continue

        # fit coincidence to cos function
        #x0 = fit.autoinit_wave(data['Angle'], data['Coincidence']) #[a, b, c, d]
        #x0 = fix_guess(f, x0) #fix guess based on file name 
        #plot_fit(data, func.cos_func, np.array(x0), logname=f)
        #save_plot(f, settings.FIT_DATA_DIR + '/Cos')
        # fit coincidence to cos^2 function (pvv plus)
        x0 = fit.autoinit_sq_wave(data['Angle'], data['Coincidence'])
        del x0[3]
        del x0[2] # delete phase shift parameter
        del x0[1] # delete frequency parameter
        settings.alpha = alpha(f)
        print('alpha', settings.alpha)
        plot_fit(data, func.cos_sq_func_pvv_plus, np.array(x0), logname=f)
        save_plot(f, settings.FIT_DATA_DIR + '/Pvv_plus')
        # fit to sin^2 (pvv minus)
        x0 = fit.autoinit_sq_wave(data['Angle'], data['Coincidence'])
        del x0[3]
        del x0[2] # delete phase shift parameter
        del x0[1] # delete frequency parameter
        #settings.alpha = alpha(f)
        print('alpha', settings.alpha)
        plot_fit(data, func.cos_sq_func_pvv_minus, np.array(x0), logname=f)
        save_plot(f, settings.FIT_DATA_DIR + '/Pvv_minus')
        # fit to cos^2(alpha+beta)
        x0 = fit.autoinit_sq_wave(data['Angle'], data['Coincidence'])
        del x0[3]
        del x0[2] # delete phase shift parameter
        del x0[1] # delete frequency parameter
        settings.alpha = alpha(f)
        print('alpha', settings.alpha)
        plot_fit(data, func.cos_sq_pvv_manual, np.array(x0), logname=f)
        save_plot(f, settings.FIT_DATA_DIR + '/Pvv_manual')

        # fit to f(beta) (for visibility check)
        #x0 = fit.autoinit_wave(data['Angle'], data['Coincidence'])
        #x0 = [ maxCoincidence(data), 1, 90, 1 ]
        x0 = [ maxCoincidence(data), 1, 45*180/(2*np.pi), 180/(2*np.pi) ]
        settings.alpha = alpha(f)
        #settings.amp = maxCoincidence(data)
        plot_fit(data, func.beta_visibility, np.array(x0), logname=f)
        #fake = [ func.beta_visibility(beta, 1) for beta in range(0, 360, 5) ]
        #plt.plot(fake)
        save_plot(f, settings.FIT_DATA_DIR + '/F_beta_visibility')

        print('max coincidence', maxCoincidence(data))
        print('min coincidence', minCoincidence(data))
        print('visibility', visibility(data))
#        print('max coincidence avg', maxCoincidenceAvg(data))
#        print('min coincidence avg', minCoincidenceAvg(data))
#        print('visibility avg', visibilityAvg(data))

        #plt.show()

