#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
# Values == requiredTime
# weights =  deadline
Item = namedtuple("Order", ['index','requiredTime', 'deadline'])

def solve(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    requiredTimes = []
    deadlines = []

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))
        requiredTimes.append(int(parts[0]))
        deadlines.append(int(parts[1]))

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    # value = 0
    # weight = 0
    # taken = [0]*len(items)
    # update values to give priority to least deadlines
    # values = [(capacity-value) for value in deadlines]

    [value, taken] = ProcessOrder( deadlines, requiredTimes, capacity)
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

def zeros(rows, cols):
    zeroList=[]
    for i in range(0, rows):
        tmpList = []
        for j in range(0, cols):
            tmpList.append(0)
        zeroList.append(tmpList)
    return zeroList

def getUsedItems(w, c):
    i=len(c)-1
    currentW = len(c[0])-1
    marked = []
    for i in range(i+1):
        marked.append(0)
    while (i>=0 and currentW>=0):
        if (i==0 and c[i][currentW] >0) or c[i][currentW] != c[i-1][currentW]:
            marked[i] = 1
            currentW = currentW-w[i]
        i=i-1
    return marked

def ProcessOrder(d, r, K):
    n = len(d)
    c=zeros(n, K+1)
    for i in range(n): # i in [0, 1] if there are two items
        for j in range(K+1): # j in [0, 1, 2...11] if knapsack is of size 11
            if r[i]<=j:
                c[i][j]=max(r[i]+c[i-1][j-r[i]], c[i-1][j])
            else:
                c[i][j]=c[i-1][j]
    return [c[n-1][K], getUsedItems(r,c)]

def plot_diagram():
    import matplotlib.pyplot as plt
    import numpy as np

    data = [[1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 0, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 3, 0, 3]]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_aspect(1)

    def avg(a, b):
        return (a + b) / 2.0

    for y, row in enumerate(data):
        for x, col in enumerate(row):
            x1 = [x, x+1]
            y1 = [0, 0]
            y2 = [1, 1]
            if col == 1:
                plt.fill_between(x1, y1, y2=y2, color='red')
                plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "A", 
                        horizontalalignment='center',
                        verticalalignment='center')
            if col == 2:
                plt.fill_between(x1, y1, y2=y2, color='orange')
                plt.text(avg(x1[0], x1[0]+1), avg(y1[0], y2[0]), "B", 
                        horizontalalignment='center',
                        verticalalignment='center')
            if col == 3:
                plt.fill_between(x1, y1, y2=y2, color='yellow')
                plt.text(avg(x1[0], x1[0]+1), avg(y1[0], y2[0]), "C", 
                        horizontalalignment='center',
                        verticalalignment='center')

    plt.ylim(1, 0)
    plt.show()
    
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/order_4)')
    plot_diagram()

