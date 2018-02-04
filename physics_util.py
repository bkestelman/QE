import numpy as np
import logging
import sys

import settings

logger = settings.createLogger(__name__)

def omega(period=None):
    if period is not None:
        logger.debug(2*np.pi/period)
        return 2*np.pi/period
    else:
        sys.exit('No arguments given to function omega')

