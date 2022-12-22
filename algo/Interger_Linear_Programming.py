from ortools.linear_solver import pywraplp
from ortools.init import pywrapinit
import random
import math
import json
import os
from pathlib import Path

LINK_PROJECT = Path(os.path.abspath(__file__)).parent.parent
DATA_FOLDER = 'datatest20_3'
RESULT_FOLDER = f'{LINK_PROJECT}/result/Integer_Linear_Programming/{DATA_FOLDER}'
 
# Opening JSON file
with open(f'{LINK_PROJECT}/data/{DATA_FOLDER}/data.json') as json_file:
    data = json.load(json_file)
    N = data['N']; m = data['m']; M = data['M']; d = data['d']; s = data['s']; e = data['e']
    d = dict(zip([*range(1, N + 1)], d))
    s = dict(zip([*range(1, N + 1)], s))
    e = dict(zip([*range(1, N + 1)], e))

print(data)
print(d)
print(s)
print(e)

solver = pywraplp.Solver.CreateSolver('SCIP')
infinity = solver.infinity()

last_pos_day = max(e.values()) + 1
#print(max(e))

x = dict() # row as field, column as day
for field in range(1, N + 1):
    x[field] = dict()
    for day in range(last_pos_day):
        x[field][day] = solver.IntVar(0, 1, f'x[{field}][{day}]')

productivity = dict()
day_to_harvest = dict()
for day in range(last_pos_day):
    productivity[day] = solver.IntVar(0, infinity, f'productivity_day_{day}')
    day_to_harvest[day] = solver.IntVar(0, 1, f'harvest_in_day_{day}')

min_productivity_per_day = solver.IntVar(0, infinity, f'min_productivity_per_day')
max_productivity_per_day = solver.IntVar(0, infinity, f'max_productivity_per_day')

for field in range(1, N + 1):
    constraint = solver.RowConstraint(1, 1, f'day to harvest field {field}')
    for day in range(last_pos_day):
        constraint.SetCoefficient(x[field][day], 1)

# for field in range(1, N + 1):
#     print(d[field])

# 1 <= (1 - day_to_harvest)N + x1 + x2 + ... + xN <= N
for day in range(last_pos_day):
    constraint = solver.RowConstraint(1 - N, 0, f'assure to harvest only when having admission in day {day}')
    constraint.SetCoefficient(day_to_harvest[day], -N)
    for field in range(1, N + 1):
        constraint.SetCoefficient(x[field][day], 1)

for day in range(last_pos_day):
    # m <= (1 - day_to_harvest)m + x1d1 + x2d2 + ... + xNdN <= M
    constraint = solver.RowConstraint(0, M - m, f'productivity not surpass M and at least m in day {day}')
    constraint.SetCoefficient(day_to_harvest[day], -m)
    for field in range(1, N + 1):
        constraint.SetCoefficient(x[field][day], d[field])

for day in range(last_pos_day):
    constraint = solver.RowConstraint(0, 0, f'productivity in day {day}')
    constraint.SetCoefficient(productivity[day], -1)
    for field in range(1, N + 1):
        constraint.SetCoefficient(x[field][day], d[field])

for day in range(last_pos_day):
    # min_productivity_per_day <= M*(1 - day_to_harvest) + productivity
    constraint = solver.RowConstraint(-M, infinity, f'min productivity must not surpass productivity of field {field}')
    constraint.SetCoefficient(day_to_harvest[day], -M)
    constraint.SetCoefficient(min_productivity_per_day, -1)
    constraint.SetCoefficient(productivity[day], 1)

    constraint = solver.RowConstraint(0, infinity, f'max productivity must not below productivity of field {field}')
    constraint.SetCoefficient(productivity[day], -1)
    constraint.SetCoefficient(max_productivity_per_day, 1)

for field in range(1, N + 1):
    constraint = solver.RowConstraint(s[field], e[field], f'day to harvest must be valid in field {field}')
    for day in range(last_pos_day):
        constraint.SetCoefficient(x[field][day], day)



objective = solver.Objective()
objective.SetCoefficient(max_productivity_per_day, 1)
objective.SetCoefficient(min_productivity_per_day, -1)
objective.SetMinimization()

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print('Objective value =', objective.Value())
    print('Root of x: ')
    for field in range(1, N + 1):
        for day in range(last_pos_day):
            print(x[field][day].solution_value(), end = ' ')
        print()
    for day in range(last_pos_day):
        print(productivity[day].solution_value(), end = ' ')
    print()
    print(min_productivity_per_day.solution_value(), max_productivity_per_day.solution_value())
else:
    print('No solution!')






print('Number of variables =', solver.NumVariables())
print('Number of constraints =', solver.NumConstraints())
