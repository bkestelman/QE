import pathlib
import argparse

import settings

def init_dirs():
    pathlib.Path(settings.LOG_DIR).mkdir(exist_ok=True)

def init_args():
    parser = argparse.ArgumentParser(description='Plot quEd exmperiment results')
    parser.add_argument('files', metavar='F', type=str, nargs='+', help='Filepath(s) to data')
    settings.args = parser.parse_args()

def init():
    init_dirs()
    init_args()

init()
