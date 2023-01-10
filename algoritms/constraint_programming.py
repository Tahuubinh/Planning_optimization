from ortools.sat.python import cp_model
import argparse
import time
import json
from numpyencoder import NumpyEncoder

def import_data(input_file):
    with open(input_file) as f:
        data = json.load(f)
        return data


def CP(data, time_limit):
    start = time.time()
    model = cp_model.CpModel()
    
    start_day = min(data['s'])
    end_day = max(data['e'])
    x = {}
    # x[i,j]: canh dong i se duoc thu hoach vao ngay thu j
    for i in range(data['N']):
        for j in range(start_day, end_day + 1):
            x[i,j] = model.NewIntVar(0, 1, 'x[%s,%s]'%(str(i), str(j)))

    product = {}
    # product[j]: san luong thu hoach ngay thu j
    for j in range(start_day, end_day + 1):
        product[j] = model.NewIntVar(0, data['M'], 'day[%s]'%(str(j)))

    max_product = model.NewIntVar(0, data['M'], 'max_product')
    min_product = model.NewIntVar(0, data['M'], 'min_product')

    # Moi canh dong chi thu hoach mot ngay, mot lan
    for i in range(data['N']):
        model.Add(sum(x[i,j] for j in range(start_day, end_day + 1)) == 1)
    # Canh dong i phai thu hoach trong khoang [si, ei]
    for i in range(data['N']):
        model.AddLinearConstraint(sum(x[i,j]*j for j in range(start_day, end_day + 1))\
                                  , data['s'][i], data['e'][i])
    # Ngay j thu hoach san luong bang product[j]
    for j in range(start_day, end_day + 1):
        model.Add(product[j] == sum(x[i,j]*data['d'][i] for i in range(data['N'])))
    # Neu product[j] != 0 thi prodcut[j] phai thuoc [m, M]
    for j in range(start_day, end_day + 1):
        b = model.NewBoolVar('b')
        model.Add(product[j] != 0).OnlyEnforceIf(b)
        model.Add(product[j] == 0).OnlyEnforceIf(b.Not())
        model.Add(product[j] >= data['m']).OnlyEnforceIf(b)
    # min_product, max_product
    model.AddMinEquality(min_product, [product[j] for j in range(start_day, end_day + 1)])
    model.AddMaxEquality(max_product, [product[j] for j in range(start_day, end_day + 1)])

    # Ham muc tieu
    model.Minimize(max_product - min_product)

    solver = cp_model.CpSolver()
    if time_limit:
        solver.parameters.max_time_in_seconds = 600
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        solution = {}
        solution["obj"] = solver.ObjectiveValue()
        solution["time"] = time.time() - start
        solution["field"] = []
        for i in range(data["N"]):
            for j in range(start_day, end_day + 1):
                if solver.Value(x[i,j]) == 1:
                    solution["field"].append(j)
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
    solution = CP(data, time_limit)
    export(output_file, solution)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required=True)
    parser.add_argument("--output_file", required=True)
    parser.add_argument('--time_limit', action="store_true")
    args = parser.parse_args()
    process(args.input_file, args.output_file, args.time_limit)
