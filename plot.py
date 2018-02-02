import pandas
import matplotlib.pyplot as plt

import consts

with open('Day_2_Data/Part1_a0.quCNTPlot') as f:
    # read data
    data = pandas.read_csv(f, delimiter='\t') 

    # clean data 
    data = data.rename(columns={'#time in s': 'Time', 'Coincidence 01': 'Coincidence'}) 
    data = data.drop('Unnamed: 4', axis=consts.COL)

    print(data)

    # plot data
    data.plot.line(x='Time', color=['r','b','g']) # check that colors match quEd controller
    plt.show()
