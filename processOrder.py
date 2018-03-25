from ortools.constraint_solver import pywrapcp
import pudb
# pudb.set_trace()

def main():
    # Create Solver
    solver = pywrapcp.Solver("ProcessOrder")

    # Data Feed
    machines_count = 1
    all_machines = range(0, machines_count)

    # ["Knife", 5] means it takes 5 minutes to setup machine M1 for production
    # of "Knife"
    all_products = [["Knife", 3],
                    ["Spoon", 2],
                    ["Fork", 5]]

    # 30, [1,5] means 5 unit time is needed for product 1 on deadline 30th.
    all_orders = [[60,[[0, 5], [2, 6]]],
                  [40,[[0, 15], [1, 10], [2,10]]],
                  [70,[[0, 7],[2, 4]]],
                  [25,[[1, 7],[2, 8]]],
                  [30,[[0, 9],[1, 5],[2, 2]]],
                 ]
    machines = [[0, 0],
               [0, 0, 0],
               [0, 0],
               [0, 0],
               [0, 0, 0],
               ]
    setup_times = [3, 2, 5]

    orders = []
    # Separate product processing times
    processing_times = []
    deadlines = []
    for i, order in enumerate(all_orders):
        productwise_time = []
        for j, products in enumerate(order[1]):
            productwise_time.append(products[1])
        processing_times.append(productwise_time)
        deadlines.append(order[0])
        orders.append(order[1])

    print("Problem Information".center(40, "*"))
    print("Orders: ".center(20, '='))
    for i, order in enumerate(orders):
        print("Order: {0}".format(i), order[0:])
    print("Processing Times: ".ljust(20), processing_times)
    print("Deadlines ".ljust(20), deadlines)

    #Statistics
    num_machines = len(all_machines)
    num_products = len(all_products)
    num_orders = len(all_orders)

    print("Number of Machines: ".ljust(20), num_machines)
    print("Number of Products: ".ljust(20), num_products)
    print("Number of Orders: ".ljust(20), num_orders)

    # Compute horizon
    horizon = 0
    for i in range(num_orders):
        horizon += sum(processing_times[i])
    print("Horizon : ".ljust(20), horizon)
    print("Problem Information".center(40, "*"))

    # Creating TASKS
    # task(i, j) = represents i-th order and j-th product task
    all_tasks = {}
    for i, order in enumerate(orders):
        for j, product in enumerate(order):
            all_tasks[(i, j)] = solver.FixedDurationIntervalVar(0,
                                                                deadlines[i],
                                                                processing_times[i][j],
                                                                False,
                                                                'Order_%i_Product_%i' % (i, j)
                                                               )
    # Create Sequence Variables
    all_sequences = []
    all_machine_jobs = []
    machine_jobs = []
    for i in all_machines:
        machine_jobs = []
        for j, order in enumerate(orders):
            for k, product in enumerate(order):
                if machines[j][k] == i:
                    machine_jobs.append(all_tasks[(j, k)])
        disj = solver.DisjunctiveConstraint(machine_jobs, 'Machine %i'%i)
        all_sequences.append(disj.SequenceVar())
        solver.Add(disj)
    print("Machine Jobs".center(40, "*"))
    print(machine_jobs)

    # Setting Objective
    # To minimize setup lengh of 

    obj_var = solver.Max([all_tasks[(i, len(machines[i])-1)].EndExpr() for i, order in enumerate(orders)])
    objective_monitor = solver.Minimize(obj_var, 1)
  # Create search phases.
    sequence_phase = solver.Phase([all_sequences[i] for i in all_machines],
                                solver.SEQUENCE_DEFAULT)
    vars_phase = solver.Phase([obj_var],
                            solver.CHOOSE_FIRST_UNBOUND,
                            solver.ASSIGN_MIN_VALUE)
    main_phase = solver.Compose([sequence_phase, vars_phase])
  # Create the solution collector.
    collector = solver.LastSolutionCollector()

  # Add the interesting variables to the SolutionCollector.
    collector.Add(all_sequences)
    collector.AddObjective(obj_var)

    for i in all_machines:
        sequence = all_sequences[i];
        sequence_count = sequence.Size();
        for j in range(0, sequence_count):
            t = sequence.Interval(j)
            collector.Add(t.StartExpr().Var())
            collector.Add(t.EndExpr().Var())
      # Solve the problem.
    disp_col_width = 10
    if solver.Solve(main_phase, [objective_monitor, collector]):
        print("\nOptimal Schedule Length:", collector.ObjectiveValue(0), "\n")
        sol_line = ""
        sol_line_tasks = ""
        print("Optimal Schedule", "\n")

    for i in all_machines:
        seq = all_sequences[i]
        sol_line = "Machine " + str(i) + ": "
        sol_line_tasks = "Machine " + str(i) + ": "
        sequence = collector.ForwardSequence(0, seq)
        seq_size = len(sequence)

        for j in range(0, seq_size):
            t = seq.Interval(sequence[j]);
         # Add spaces to output to align columns.
            sol_line_tasks +=  t.Name() + " " * (disp_col_width - len(t.Name()))

        for j in range(0, seq_size):
            t = seq.Interval(sequence[j]);
            sol_tmp = "[" + str(collector.Value(0, t.StartExpr().Var())) + ","
            sol_tmp += str(collector.Value(0, t.EndExpr().Var())) + "] "
            # Add spaces to output to align columns.
            sol_line += sol_tmp + " " * (disp_col_width - len(sol_tmp))

        sol_line += "\n"
        sol_line_tasks += "\n"

    print(sol_line_tasks)
    print("Time Intervals for Tasks\n")
    print(sol_line)
    


    


if __name__=='__main__':
    main()


