#!/usr/bin/python
# -*- coding: utf-8 -*-
from operator import attrgetter
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

    [value, taken] = ProcessOrder( deadlines, requiredTimes, capacity)
    # prepare the solution in the specified output format

    combined_items = []
    for i, item in enumerate(taken):
        taken_order=[]
        if item == 1:
            combined_items.append(Item(i, requiredTimes[i], deadlines[i]))
    print(combined_items)
    # Fix Scheduling time
    # Sort as per deadline
    # 1. First endDate set to time duration of that order
    # 2. Add next time duration and so on
    sorted_deadlines = sorted(combined_items, key = attrgetter('deadline'))
    print(sorted_deadlines)
    data_for_graph = []
    for i,item in enumerate(sorted_deadlines):
        if i==0:
            data_for_graph.append([item.index, 0,
            item.requiredTime])
        else:
            data_for_graph.append([item.index, sorted_deadlines[i-1].requiredTime,
             sorted_deadlines[i-1].requiredTime+item.requiredTime])
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    print(data_for_graph)
    plot_schedule(data_for_graph)
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

def plot_schedule(process_orders):
    import numpy as np
    from matplotlib import pyplot as plt
    colors = ["r","g","b","y"]
    values = np.array(process_orders)
    # values = np.array([[data[name] for name in order] for data,order in zip(dataset, data_orders)])
    bottoms = np.arange(len([0]))
    print(process_orders)
    for i, order in enumerate(process_orders):
        value = order[2]
        left = order[1]
        plt.bar(left=left, height=0.01, width=value, bottom=bottoms, 
                color=colors[-i], orientation="horizontal", label='Order_%i'%order[0])
    plt.yticks(bottoms+0.4, ["data %d" % (t+1) for t in bottoms])
    plt.legend(loc="best", bbox_to_anchor=(1.0, 1.00))
    plt.subplots_adjust(right=0.85)
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
