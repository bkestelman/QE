import pathlib
import argparse

import settings

def init_dirs():
    pathlib.Path(settings.LOG_DIR).mkdir(exist_ok=True)

def init_args():
    parser = argparse.ArgumentParser(description='Plot quEd exmperiment results')
    parser.add_argument('files', metavar='F', type=str, nargs='+', help='Filepath(s) to data')
    parser.add_argument('task', metavar='T', type=str, help='Task to perform: raw|clean|pvv|visibility')
    settings.args = parser.parse_args()

def init():
    init_dirs()
    init_args()

init()
