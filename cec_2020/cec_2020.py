#!/usr/bin/env python3

from ctypes import CDLL, POINTER, Structure, c_int, c_double, Array
import matplotlib.pyplot as plt
import numpy as np

SOMA_SO_LIB = "./SOMA.so"
JDE_SO_LIB = "./JDE.so"

DIMENSIONS = [10, 20]
BOUNDS = 100
RUNS = 30

FUNCTIONS = {
    1: "bent_cigar", # 100
    2: "schwefel", # 1100
    3: "lunacek_bi_rastrigin", # 700
    4: "rosenbrock_griewangk", # 1900
    5: "hybrid_one", # 1700
    6: "hybrid_two", # 1600
    7: "hybrid_three", # 2100
    8: "composition_one", # 2200
    9: "composition_two", # 2400
    10: "composition_three" # 2500
}

OUTPUT_DIR = "output/"

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

    # Evaluate test functions using SOMA and jDE
    global_results = {x: {y: {} for y in DIMENSIONS} for x in FUNCTIONS}
    for func_id in FUNCTIONS:
        for dimension in DIMENSIONS:
            for algo_name, algo_lib in algos.items():
                print(f"Starting evaluation of {algo_name}_F{func_id}_{FUNCTIONS[func_id]}_{dimension}d.")
                all_run_results = []
                for i in range(RUNS):
                    result_buff = (Result * 200000)()
                    result_length = algo_lib.run(dimension, func_id, BOUNDS, result_buff)
                    result_buff = result_buff[:result_length]
                    for idx, res in enumerate(result_buff):
                        if idx >= len(all_run_results):
                            all_run_results.append([])
                        all_run_results[idx].append(np.double(res.cost))
                    print(f"Run {i+1}/{RUNS} completed.")
                average_run_results = []
                for run_result in all_run_results:
                    average_run_result = np.mean(run_result)
                    average_run_results.append(average_run_result)
                global_results[func_id][dimension][algo_name] = average_run_results

                minimum = np.min(average_run_results)
                maximum = np.max(average_run_results)
                mean = np.mean(average_run_results)
                median = np.median(average_run_results)
                stddev = np.std(average_run_results)
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
