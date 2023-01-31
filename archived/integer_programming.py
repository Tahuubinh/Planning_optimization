from ortools.linear_solver import pywraplp
import argparse
import time
import json
from numpyencoder import NumpyEncoder


def import_data(input_file):
    with open(input_file) as f:
        data = json.load(f)
        return data


def IP_solver(data, time_limit):
    min_start = min(data["s"])
    for i in range(data["N"]):
        data["s"][i] -= min_start
        data["e"][i] -= min_start
    D = max(data["e"])
    start = time.time()

    solver = pywraplp.Solver.CreateSolver("SCIP")

    # Create variable
    a = {}
    b = {}
    for i in range(0, data["N"]):
        for j in range(0, D + 1):
            a[i, j] = solver.IntVar(0, 1, "a[{}_{}]".format(i, j))
    max_day = solver.NumVar(lb=0, ub=data["M"], name="max_day")
    min_day = solver.NumVar(lb=0, ub=data["M"], name="min_day")

    # Add constraint
    for i in range(0, data["N"]):
        for j in range(0, data["s"][i]):
            solver.Add(a[i, j] == 0)
        solver.Add(solver.Sum([a[i, j] for j in range(
            data["s"][i], data["e"][i] + 1)]) == 1)
        for j in range(data["e"][i] + 1, D + 1):
            solver.Add(a[i, j] == 0)
    for j in range(0, D + 1):
        b[j] = solver.IntVar(0, 1, "b[{}]".format(j))
    for j in range(0, D + 1):
        for i in range(0, data["N"]):
            solver.Add(b[j] >= a[i, j])
        solver.Add(solver.Sum([a[i, j] * data['d'][i]
                   for i in range(0, data["N"])]) >= b[j])
    for j in range(0, D + 1):
        solver.Add(solver.Sum([a[i, j] * data['d'][i]
                   for i in range(0, data["N"])]) <= max_day)
        solver.Add(solver.Sum([a[i, j] * data['d'][i]
                   for i in range(0, data["N"])]) >= min_day)
        solver.Add(solver.Sum([a[i, j] * data['d'][i]
                   for i in range(0, data["N"])]) >= data["m"] * b[j])
    solver.Minimize(max_day - min_day)
    if time_limit:
        solver.set_time_limit(10)
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        solution = {}
        solution["obj"] = solver.Objective().Value()
        solution["time"] = time.time() - start
        solution["field"] = []
        for i in range(data["N"]):
            for j in range(0, D + 1):
                if a[i, j].solution_value() == 1:
                    solution["field"].append(j + min_start)
                    break
    else:
        solution = {}
        solution["obj"] = "No Solution"
        solution["time"] = time.time() - start
    return solution


def export(output_file, solution):
    if len(solution) == 3:
        with open(output_file, "w+") as f:
            json.dump({"Time": solution["time"], "Result": solution["obj"],
                      "Solution": solution["field"]}, f, cls=NumpyEncoder)
    else:
        with open(output_file, "w+") as f:
            json.dump({"Time": solution["time"], "Result": solution["obj"]}, f, cls=NumpyEncoder)


def process(input_file, output_file, time_limit):
    data = import_data(input_file)
    solution = IP_solver(data, time_limit)
    export(output_file, solution)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required=True)
    parser.add_argument("--output_file", required=True)
    parser.add_argument('--time_limit', action="store_true")
    args = parser.parse_args()
    process(args.input_file, args.output_file, args.time_limit)
