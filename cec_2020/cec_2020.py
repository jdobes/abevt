#!/usr/bin/env python3

import csv
from ctypes import CDLL, POINTER, Structure, c_int, c_double, Array

SOMA_SO_LIB = "./SOMA.so"
JDE_SO_LIB = "./JDE.so"

DIMENSIONS = [10, 20]
BOUNDS = 100
RUNS = 30

FUNC_NAMES = {
    1: "bend-cigar",
    2: "rotated-schwefel",
    3: "lunacek",
    4: "rosenbrock",
    5: "hybrid-one",
    6: "hybrid-one-two",
    7: "hybrid-one-three",
    8: "composition-one",
    9: "composition-two",
    10: "composition-three"
}

class Result(Structure):
    _fields_ = [
       ("fez", c_int),
       ("cost", c_double)]


def main():
    soma = CDLL(SOMA_SO_LIB)
    soma.run.argtypes = [c_int, c_int, c_int, POINTER(Result)]
    soma.run.restype = c_int
    jde = CDLL(JDE_SO_LIB)
    jde.run.argtypes = [c_int, c_int, c_int, POINTER(Result)]
    jde.run.restype = c_int

    algos = {"soma": soma, "jde": jde}

    for algo_name, algo_lib in algos.items():
        for dimension in DIMENSIONS:
            for func_id in range(1,11):
                results = []
                for _ in range(RUNS):
                    result_buff = (Result * 100000)()
                    result_length = algo_lib.run(dimension, func_id, BOUNDS, result_buff)
                    result_buff = result_buff[:result_length]
                    results.append(result_buff)
                
                csv_transformed_results = []
                for run_0_data in results[0]:
                    csv_transformed_results.append([run_0_data.fez, run_0_data.cost])
                for run_data in results[1:]:
                    for i, run_x_data in enumerate(run_data):
                        csv_transformed_results[i].append(run_x_data.cost)

                with open(f"output/{algo_name}-{FUNC_NAMES[func_id]}-{dimension}-dim.csv", "w", newline="") as csvfile:
                    writer = csv.writer(csvfile, delimiter=";", quotechar="\"", quoting=csv.QUOTE_MINIMAL)
                    for row in csv_transformed_results:
                        writer.writerow(row)


if __name__ == "__main__":
    main()
