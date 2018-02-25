import pandas
import numpy as np
import logging
import logging.config

import settings
import consts
import clean

logger = settings.createLogger(__name__, filemode='w')

def errorData(data, x=None, y=None, title=None):
    #logger.info(str(title) + "\nCLEAN DATA\n" + str(data))
    logger.info(str(title) + "\nAVERAGES\n" + str(data.groupby(x)[y].mean()))
    logger.info(str(title) + "\nMAXES\n" + str(data.groupby(x)[y].max()))
    logger.info(str(title) + "\nMINS\n" + str(data.groupby(x)[y].min()))
