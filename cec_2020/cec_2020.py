#!/usr/bin/env python3

from ctypes import CDLL, POINTER, c_int, c_double
import matplotlib.pyplot as plt
import numpy as np
import sys

import jde
import soma

CEC20_SO_LIB = "./cec20_test_func.so"

DIMENSIONS = [10, 20]
BOUNDS = [-100, 100]
RUNS = 30

FUNCTIONS = {
    1: "bent_cigar", # 100
#    2: "schwefel", # 1100
#    3: "lunacek_bi_rastrigin", # 700
#    4: "rosenbrock_griewangk", # 1900
#    5: "hybrid_one", # 1700
#    6: "hybrid_two", # 1600
#    7: "hybrid_three", # 2100
#    8: "composition_one", # 2200
#    9: "composition_two", # 2400
#    10: "composition_three" # 2500
}

OUTPUT_DIR = "output/"


def main():
    # Define C library interface
    cec20 = CDLL(CEC20_SO_LIB)
    cec20.cec20_test_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int]
    cec20.cec20_test_func.restype = None

    # Alias for C function
    cost_function = cec20.cec20_test_func

    algos = {"jde": jde, "soma": soma}

    # Evaluate test functions using SOMA and jDE
    global_results = {x: {y: {} for y in DIMENSIONS} for x in FUNCTIONS}
    for func_id in FUNCTIONS:
        for dimension in DIMENSIONS:
            for algo_name, algo_lib in algos.items():
                print(f"Starting evaluation of {algo_name}_F{func_id}_{FUNCTIONS[func_id]}_{dimension}d.")
                all_run_results = []
                best_run_results = []
                for i in range(RUNS):
                    best_results = algo_lib.run(cost_function, func_id, dimension, BOUNDS)
                    for idx, res in enumerate(best_results):
                        if idx >= len(all_run_results):
                            all_run_results.append([])
                        all_run_results[idx].append(res)
                    sys.stdout.write(f"\rRun {i+1}/{RUNS} completed.")
                    sys.stdout.flush()
                    best_run_result = np.min(best_results)
                    best_run_results.append(best_run_result)
                print("")
                average_run_results = []
                for run_result in all_run_results:
                    average_run_result = np.mean(run_result)
                    average_run_results.append(average_run_result)
                global_results[func_id][dimension][algo_name] = average_run_results

                minimum = np.min(best_run_results)
                maximum = np.max(best_run_results)
                mean = np.mean(best_run_results)
                median = np.median(best_run_results)
                stddev = np.std(best_run_results)
                print(f"Evaluation of {algo_name}_F{func_id}_{FUNCTIONS[func_id]}_{dimension}d finished, min={minimum}, max={maximum}, mean={mean}, median={median}, stddev={stddev}")

    # Plot graphs
    print(f"Plotting graphs to output dir: {OUTPUT_DIR}")
    for func_id in FUNCTIONS:
        for dimension in DIMENSIONS:
            plt.xlabel("FES")
            plt.ylabel("cost")
            plt.grid(True)
            plt.title(f"F{func_id}_{FUNCTIONS[func_id]}_{dimension}d, average best run")
            for algo_name, algo_average_run_result in global_results[func_id][dimension].items():
                plt.plot(range(1, len(algo_average_run_result)+1), algo_average_run_result, linewidth=1, label=algo_name)
            plt.legend()
            plt.savefig(f"{OUTPUT_DIR}F{func_id}_{FUNCTIONS[func_id]}_{dimension}d.png")
            plt.clf()
            plt.cla()
            plt.close()
    print("Plotting graphs finished.")


if __name__ == "__main__":
    main()
