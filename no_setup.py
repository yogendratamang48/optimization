#! /usr/bin/env python
# Processing Order with deadlines
from ortools.constraint_solver import pywrapcp
import pudb
import matplotlib.pyplot as plt
# pudb.set_trace()


def main():
    # Define Data
    num_orders = 4
    num_products = 3
    all_products = range(0, num_products)
    all_orders = range(0, num_orders)

    orders = [[0, 1, 2],
                 [0, 1],
                  [1, 2],
                  [0, 2]
                 ]
    processing_times = [[5, 2, 3],
                        [3, 4, 5],
                        [2, 5],
                        [2, 1]
                       ]
    deadlines = [15, 45, 30, 35]

    required_times = [sum(i) for i in processing_times]

    # Horizon
    horizon = max(deadlines)

    solver = pywrapcp.Solver("ProcessOrder")

    # find Processing Times and create sequence variable
    # Creating TASKS
    # task(i, j) = represents i-th order and j-th product task
    all_tasks = {}
    for i in all_orders:
        for j in range(len(orders[i])):
            all_tasks[(i, j)] = solver.FixedDurationIntervalVar(0,
                                                                deadlines[i],
                                                                processing_times[i][j],
                                                                False,
                                                                'Order_%i_Product_%i' % (i, j)
                                                               )

    # Instantiate Solver
    # print("All TASKS: ")
    # print(all_tasks)
    print("Problem Information".center(60, '*'))
    print("ProductTypes: ", [_ for _ in all_products])
    print("Total Orders: ", len(orders))
    for i, order in enumerate(orders):
        print('Order %i -- %s'%(i, order))
    
    print(" Processing Times ".center(40, '='))
    for i, time in enumerate(required_times):
        print('Order %i -- %i'%(i, time))

    print(" Deadlines ".center(40, '='))
    for i, deadline in enumerate(deadlines):
        print('Order %i -- %i'%(i, deadline))

    print("Solution".center(60, '*'))
    # Algorithm
    # 1. Find Maximum Order Deadline
    totalTimeSlots = []
    tmp_deadlines = list(deadlines)
    tmp_required_times = list(required_times)
    while len(tmp_deadlines)>0:
        maxDeadline = max(tmp_deadlines)
        maxIndex = tmp_deadlines.index(maxDeadline)
        orderIndex = deadlines.index(maxDeadline)
        requiredTime = tmp_required_times[maxIndex]
        timeSlots = {}
        timeSlots["start"] = maxDeadline - requiredTime
        timeSlots["end"] = maxDeadline
        timeSlots["orderIndex"]=orderIndex
        totalTimeSlots.append(timeSlots)
        del tmp_required_times[maxIndex]
        del tmp_deadlines[maxIndex]

    optimizedTimeSlot = []
    # Find Required Shift Needed
    # Apply Shift to all
    # get orderedlist as per start date
    ordered_list = sorted(totalTimeSlots, key = lambda k: k['start'])

    # Setting Initial Time to 0
    # Matching End time of Order i with start of Order (i+1)
    for i, order in enumerate(ordered_list):
        if i == 0:
            shift = ordered_list[i]['start']-0
        else:
            shift = ordered_list[i]['start']-ordered_list[i-1]['end']
        order['start'] -= shift
        order['end'] -= shift

    print("Optimized List")
    for order in ordered_list:
        print("Order %i - (%i, %i) " % (order['orderIndex'], order['start'],
              order['end']))
    # Order list by start and End
    # Plotting Figure




if __name__=='__main__':
    main()
