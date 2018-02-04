# Data cleaning algorithms for quED data

import pandas
import logging

import settings
import consts
from math_util import *

logger = settings.createLogger(__name__)
logger.info('clean.py log\n----------')

# rename columns, drop extra column, remove times with no measurements
def prettify_data(data): 
    data = data.rename(columns={'#time in s': 'Time', 'Coincidence 01': 'Coincidence'}) 
    data = data.drop('Unnamed: 4', axis=consts.COL) # extra column
    # drop points from before we started collecting data 
    drop_list = []
    for row in range(len(data)):
        if data['Single 0'][row] == 0 and data['Single 1'][row] == 0: # 0 counts recorded -> not collecting data
            drop_list.append(row)
    data = data.drop(data.index[drop_list])
    return data

# deletes spikes produced between angle changes
# params: DataFrame data
# algorithm:
# 1. consider 10 points that definitely contain the data for an angle (but not for two angles)
# 2. select the 5 consecutive points with the smallest range (the 5 most similar points)
# 3. loop. consider the 10 points after the selected 5
# 4. use selected points
def clean_spikes(data):
    start = 0
    consider = 13 # 13 seems to work better than 10 because sometimes we waited longer than 5 seconds
    select = 5
    singles_0 = data['Single 0'].tolist()
    singles_1 = data['Single 1'].tolist()
    coincidence = data['Coincidence'].tolist()
    angles = [x for x in range(0, 361, 10)]
    angle_index = 0
    logger.debug(angles)
    clean_data = [] 
    while(angle_index <= 36):
        subseq = singles_0[start:consider+start] 
        closest = closest_subseq(subseq, select)
        logger.debug('angle: ' + str(angle_index))
        logger.debug('subseq: ' + str(subseq))
        logger.debug('closest: ' + str(closest))
        cursor = start + closest['index']
        for point in range(select):
            clean_data.append({'Angle': angles[angle_index], 'Single 0': singles_0[cursor], 'Single 1': singles_1[cursor], 'Coincidence': coincidence[cursor]})
            cursor += 1
        angle_index += 1
        start += closest['index'] + select 
    return pandas.DataFrame(clean_data)


