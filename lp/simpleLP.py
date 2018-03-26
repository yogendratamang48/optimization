#!/usr/bin/env python
# Linear Optimizatio using or-tools
# GLOP = Google Linear Optimization Programming
'''
Steps:
    0. Instantiate Solver
    1. Create Variables (add to solver)
    2. Define Constraints using Variables (add to solver)
    3. Define Objective Function (add to solver)
    4. Solve
'''
from ortools.linear_solver import pywraplp


def main():

    # Instantiate 
    solver = pywraplp.Solver('Linear Example',
                             pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    # Create Variables
    x = solver.NumVar(-solver.infinity(), solver.infinity(), 'x')
    y = solver.NumVar(-solver.infinity(), solver.infinity(), 'y')

    # Constraint1 x + 2y <= 14
    constraint1 = solver.Constraint(-solver.infinity(), 14)
    constraint1.SetCoefficient(x, 1)
    constraint1.SetCoefficient(y, 2)

    # Constraint 2: 3x-y >= 0
    constraint2 = solver.Constraint(0, solver.infinity())
    constraint2.SetCoefficient(x, 3)
    constraint2.SetCoefficient(y, -1)

    # Constraint 3: x-y <= 2
    constraint3 = solver.Constraint(-solver.infinity(), 2)
    constraint3.SetCoefficient(x, 1)
    constraint3.SetCoefficient(y, -1)

    # Objective Function 3x+4y
    objective = solver.Objective()
    objective.SetCoefficient(x, 3)
    objective.SetCoefficient(y, 4)
    objective.SetMaximization()

    # Solve the problem
    solver.Solve()
    opt_solution = 3*x.solution_value() + 4*y.solution_value()
    print('Num of Variables: ', solver.NumVariables())
    print('Num of Contraints: ', solver.NumConstraints())

    # Values
    print("Solution: ")
    print("x: ", x.solution_value())
    print('y: ', y.solution_value())
    print('Optimal Value: ', opt_solution)

if __name__=='__main__':
    main()
