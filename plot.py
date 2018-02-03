import pandas
import matplotlib.pyplot as plt

import consts
from math_util import *

def read_data(f):
    return pandas.read_csv(f, delimiter='\t') 

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

def plot_raw_data(datafile):
    with open(datafile) as f:
        data = read_data(f) 
        data = prettify_data(data)
        data.plot.line(x='Time', color=['r','b','g']) # TODO: check that colors match quEd controller
        plt.title('Raw data')

# deletes spikes produced between angle changes
# algorithm:
# 1. consider 10 points that definitely contain the data for an angle
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
    print(angles)
    clean_data = [] 
    while(angle_index <= 36):
        subseq = singles_0[start:consider+start] 
        closest = closest_subseq(subseq, select)
        print('angle', angle_index)
        print('subseq', subseq)
        print('closest', closest)
        cursor = start + closest['index']
        for point in range(select):
            clean_data.append({'Angle': angles[angle_index], 'Single 0': singles_0[cursor], 'Single 1': singles_1[cursor], 'Coincidence': coincidence[cursor]})
            cursor += 1
        angle_index += 1
        start += closest['index'] + select 
    return pandas.DataFrame(clean_data)

def plot_clean_data(datafile):
    with open(datafile) as f:
        data = read_data(f)
        data = prettify_data(data)
        data = clean_spikes(data)
        with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
            print(data)
        data.plot(x='Angle')
        ax = data.plot.scatter(x='Angle', y='Single 0', color='Red')
        ax = data.plot.scatter(x='Angle', y='Single 1', color='Blue', ax=ax)
        data.plot.scatter(x='Angle', y='Coincidence', color='Green', ax=ax)

plot_raw_data('Day_2_Data/Part1_a0.quCNTPlot')
plot_clean_data('Day_2_Data/Part1_a0.quCNTPlot')
plt.show()
