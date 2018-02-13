import logging

LOG_DIR = 'Log'
RESULTS_DIR = 'Results'
RAW_DATA_DIR = RESULTS_DIR + '/Raw'
CLEAN_DATA_DIR = RESULTS_DIR + '/Clean'
FIT_DATA_DIR = RESULTS_DIR + '/Fit'

def log_path(filename):
    return LOG_DIR + '/' + filename + '.log'

def createLogger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(log_path(name), 'a')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

alpha = 0
