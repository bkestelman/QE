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
        plt.show()

# deletes spikes produced between angle changes
# algorithm:
# 1. consider 10 points that definitely contain the data for an angle
# 2. select the 5 consecutive points with the smallest range (the 5 most similar points)
# 3. loop. consider the 10 points after the selected 5
# 4. use selected points
def clean_spikes(data):
    start = 0
    consider = 10
    select = 5
    single = data['Single 0']
    angles = [x for x in range(0, 361, 10)]
    angle_index = 0
    print(angles)
    clean_data = [] 
    while(start < len(single) - consider):
        subseq = single[start:consider+start] 
        closest = closest_subseq(subseq, select)
        for point in range(select):
            clean_data.append({'Angle': angles[angle_index], 'Single 0': point})
        angle_index += 1
    return pandas.DataFrame(clean_data)

def plot_clean_data(datafile):
    with open(datafile) as f:
        data = read_data(f)
        data = prettify_data(data)
        data = clean_spikes(data)
        print(data)
        # add angle column

plot_raw_data('Day_2_Data/Part1_a0.quCNTPlot')
#plot_clean_data('Day_2_Data/Part1_a0.quCNTPlot')

