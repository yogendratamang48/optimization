#!/usr/bin/python
# -*- coding: utf-8 -*-
from operator import attrgetter
from collections import namedtuple
from collections import OrderedDict
import numpy as np
from matplotlib import pyplot as plt
# import pudb
# pudb.set_trace()
# Values == requiredTime
# weights =  deadline
Item = namedtuple("Item", ['index','requiredTime', 'deadline'])
Product = namedtuple('Product',['index', 'name', 'setupTime', 'unitProductionTime'])
Order = namedtuple('Order',['orderID','productIndex', 'quantity', 'deadline', 'workIndex'])


def solve(input_data, capacity=None):
    # Modify this code to run your optimization algorithm

    # parse the input
    deadlines = [data[2] for data in input_data]
    requiredTimes = [data[1] for data in input_data]
    if capacity is None:
        capacity=max(deadlines)

    [value, taken] = ProcessOrder( deadlines, requiredTimes, capacity)
    # prepare the solution in the specified output format

    combined_items = []
    for i, item in enumerate(taken):
        taken_order=[]
        if item == 1:
            combined_items.append(Item(i, requiredTimes[i], deadlines[i]))
    # Fix Scheduling time
    # Sort as per deadline
    # 1. First endDate set to time duration of that order
    # 2. Add next time duration and so on
    sorted_deadlines = sorted(combined_items, key = attrgetter('deadline'))
    print("RESULTS:")
    output_data = str(value) + ' ' + str(0)
    # output_data += ' '.join(map(str, taken))
    print(output_data)
    data_for_graph = []
    for i,item in enumerate(sorted_deadlines):
        if i==0:
            data_for_graph.append([item.index, 0,
            item.requiredTime])
        else:
            data_for_graph.append([item.index, data_for_graph[i-1][-1],
             data_for_graph[i-1][-1]+item.requiredTime])
    # plot_schedule(data_for_graph)
    return taken

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
    # Maximize Machine Usage
    n = len(d)
    c=zeros(n, K+1)
    for i in range(n): # i in [0, 1] if there are two items
        for j in range(K+1): # j in [0, 1, 2...11] if deadline is 11
            if r[i]<=j:
                c[i][j]=max(r[i]+c[i-1][j-r[i]], c[i-1][j])
            else:
                c[i][j]=c[i-1][j]
    return [c[n-1][K], getUsedItems(r,c)]

def ProcessProdcut(d, r, s, K):
    # Minimize Machine Setup
    # d = 
    # r=
    # K=Capacity
    n = len(d) # number of orders
    c=zeros(n, K+1)
    for i in range(n): # i in [0, 1] if there are two items
        for j in range(K+1): # j in [0, 1, 2...11] if deadline is 11
            if r[i]<=j:
                c[i][j]=min(r[i]+c[i-1][j-r[i]], c[i-1][j])
            else:
                c[i][j]=c[i-1][j]
    return [c[n-1][K], getUsedItems(r,c)]

def plot_schedule(list_process_orders, products):
    colors = ["r","g","b","y"]
    values = np.array(list_process_orders)
    fig = plt.figure(figsize=(12, 3))
    ax1 = fig.add_subplot(111)
    left = 0
    color_index = -1
    plt.axvline(x=left, color='black')
    for j, process_orders in enumerate(list_process_orders):
        for i, order in enumerate(process_orders):
            value = order[1]
            if color_index != -1:
                setupTime = [product.setupTime for product in products if product.index == color_index]
            else:
                setupTime = [product.setupTime for product in products if product.index == order[3]]
            setupTime = setupTime[0]
            if color_index != order[3]:
                value = order[1]-setupTime
                plt.axvline(x=left, color='yellow')
                left += setupTime
                plt.axvline(x=left, color='yellow')
            color_index = order[3]
            ax1.barh(y=0,left=left, width=value, linewidth=0.5, 
                    color=colors[color_index])
            left += value
        ax1.text(left/2, 0, "oder")
        # plt.yticks(bottoms+0.4, ["data %d" % (t+1) for t in bottoms])
        plt.axvline(x=left, color='black')
    plt.legend(loc="best", bbox_to_anchor=(1.0, 1.00))
    # plt.subplots_adjust(right=0.85)
    plt.show()

def get_clean_data(order_data, product_data):
    product_lines = product_data.split('\n')
    product_count = len(product_lines)-1
    products = []
    for i in range(1, product_count):
        lines = product_lines[i].split(',')
        products.append(Product(int(lines[3]), lines[0], int(lines[1]), int(lines[2])))

    order_lines = order_data.split('\n')
    order_count = len(order_lines)-1
    orders = []
    for i in range(1, order_count):
        lines = order_lines[i].split(',')
        orders.append(Order(int(lines[0]), int(lines[1]), int(lines[2]),
                            int(lines[3]), int(lines[4])))
    processed_orders = []
    for order in orders:
        # in format Order(requiredTime, deadline)
        product = [p for p in products if p.index == order.productIndex]
        processed_orders.append([order.orderID,int(order.quantity/product[0].unitProductionTime
                                                   + product[0].setupTime),
                                 order.deadline, order[1] ])

        # Combining order wise
    combined_orders = []
    for orderID in set([order[0] for order in processed_orders]):
        combined_orders.append([orderID,
                                sum([order[1] for order in processed_orders if order[0]==orderID]), #Required Time
                                ([order[2] for order in processed_orders if order[0]==orderID])[0], # Deadlines
                                    ])
    
    return products, orders, processed_orders, combined_orders 

def getProductWithMaxSetupTime(common, products):
    max_value=max([product.setupTime for product in products if product.index in common])
    productID = [product.index for product in products if product.setupTime==max_value and product.index in common]
    return productID[0]

def getProductWithMinSetupTime(remaining, products):
    max_value=max([product.setupTime for product in products if product.index in remaining])
    productID = [product.index for product in products if product.setupTime==max_value and product.index in remaining]
    return productID[0]

def optimize_product(taken_products, products):
    # get Order Id in sequence
    orderIDs = list(OrderedDict.fromkeys([order[0] for order in taken_products]))
    # Find Common Product between Order1 and following Order 2
    common_products = []
    for i, orderID in enumerate(orderIDs):
        if i<(len(orderIDs)-1):
            current_products = set([taken[3] for taken in taken_products if taken[0]==orderID])
            next_products = set([taken[3] for taken in taken_products if taken[0]==orderIDs[i+1]])
            common_products.append(current_products & next_products)
    common_products = list(common_products)

    # 2. find product of maximum setUpTime
    transitions = []
    for i, common in enumerate(common_products):
        if common not in transitions:
            common = list(common)
            maxProductID=getProductWithMaxSetupTime(common, products)
            transitions.append([maxProductID])

    # Find Product with minimum setUpTime from remaining productID for every
    # order
    orders = taken_products
    otherProducts=[]
    for i, orderID in enumerate(orderIDs):
        if i ==0:
            otherProducts.append([order[3] for order in orders if order[0]==orderID and order[3] not in transitions[i]])
        elif i==(len(orderIDs)-1):
            otherProducts.append([order[3] for order in orders if order[0]==orderID and order[3] not in transitions[i-1]])
        else:
            otherProducts.append([order[3] for order in orders if order[0]==orderID and order[3] not in transitions[i] and order[3] not in transitions[i-1]])
    slots = []
    combined_sequence = [ ]
    for i, other in enumerate(otherProducts):
        if i==0:
            try:
                other.append(transitions[i][0])
            except:
                pass
        elif i == (len(otherProducts)-1):
            try:
                other.insert(0, transitions[i-1][0])
            except:
                pass
        else:
            try:
                other.insert(0, transitions[i-1][0])
            except:
                pass
            try:
                other.append(transitions[i][0])
            except:
                pass
        combined_sequence.append(other)
    return orderIDs, combined_sequence
    
    
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        with open("data/products.txt", 'r') as product_file:
            product_data= product_file.read()
        products, orders, processed_orders, combined_orders= get_clean_data(input_data, product_data)
        taken=solve(combined_orders)
        taken_products = [order for order in processed_orders if taken[order[0]]==1]
        orderIDs, combined_sequence=optimize_product(taken_products, products)
        print("\nTAKEN ORDERS")
        print(taken_products)
        print("\We should run following ORDERS: ")
        print(orderIDs)
        print("\nPRODUCT Run Sequence")
        print(combined_sequence)
        print("\nORDERS")
        print(orders)
        print("\nProducts")
        print(products)
        new_list = []
        # Re-arrage taken orders
        for i, orderID in enumerate(orderIDs):
            new_list.append([order for order in taken_products if order[0]==orderID])
        # Sort new_list as per combined_sequence
        print("New LIST")
        print(new_list)
        final_list = []
        for i, item in enumerate(new_list):
            final_list.append(sorted(item, key=lambda x: combined_sequence[i].index(x[3])))
        print("\nFinal LIST")
        print(final_list)
        plot_schedule(final_list, products)
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/order_4)')
