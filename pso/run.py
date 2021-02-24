#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from numpy import asarray

from pso import Swarm


def first_dejong(x):
    return np.sum(x**2)

def second_dejong(x):
    return np.sum(100 * (x[:-1] ** 2 - x[1:]) ** 2 + (1 - x[:-1]) ** 2)

def schweffel(x):
    return np.sum((-1) * x * np.sin(np.sqrt(np.abs(x))))

def rastrigin(x):
    return 2 * len(x) + np.sum(x ** 2 - 10 * np.cos(2 * np.pi * x))

RUNS = 30

COST_FUNCTIONS = {
    "first_dejong": first_dejong,
    "second_dejong": second_dejong,
    "schweffel": schweffel,
    "rastrigin": rastrigin
}

BOUNDS = {
    "first_dejong": [-5,5],
    "second_dejong": [-2,2],
    "schweffel": [0,500],
    "rastrigin": [-2,2]
}

GRAPH_BOUNDS = {
    "first_dejong_10": (0,5000,0,20),
    "first_dejong_30": (0,20000,0,20),
    "second_dejong_10": (0,50000,0,20),
    "second_dejong_30": (0,100000,0,50),
    "schweffel_10": (0,50000,-419*10,0),
    "schweffel_30": (0,2000,-419*10,0),
    "rastrigin_10": (0,50000,-200*10,0),
    "rastrigin_30": (0,100000,-200*30,0)
}

def init_graph(fun_name, dimensions, title):
    plt.xlabel("FES")
    plt.ylabel("cost function")
    plt.grid(True)
    plt.axis(GRAPH_BOUNDS[f"{fun_name}_{dimensions}"])
    plt.title(title)

if __name__ == "__main__":
    for name, cost_function in COST_FUNCTIONS.items():
        for dimensions in [10, 30]:
            init_graph(name, dimensions, f"{name}, {dimensions} dimensions, {RUNS} runs")
            cost_best_results = []
            cost_history_results = []
            for _ in range(RUNS):
                swarm = Swarm(bounds=BOUNDS[name], dimensions=dimensions, cost_function=cost_function)
                cost_best, position_best, costs_history = swarm.simulate()
                cost_best_results.append(cost_best)
                cost_history_results.append(costs_history)
                #print(f"{name}, {dimensions} dimensions: cost_best={cost_best}, position_best={position_best}")
                plt.plot(range(1, len(costs_history)+1), costs_history, linewidth=0.5)

            plt.savefig(f"{name}_{dimensions}_all.png")
            plt.clf()
            plt.cla()
            plt.close()

            minimum = np.min(cost_best_results)
            maximum = np.max(cost_best_results)
            mean = np.mean(cost_best_results)
            median = np.median(cost_best_results)
            stddev = np.std(cost_best_results)

            average_run_history = np.mean(cost_history_results, axis=0)
            init_graph(name, dimensions, f"{name}, {dimensions} dimensions, average best run")
            plt.plot(range(1, len(average_run_history)+1), average_run_history, linewidth=1)
            plt.savefig(f"{name}_{dimensions}_average.png")
            plt.clf()
            plt.cla()
            plt.close()

            print(f"{name}, {dimensions} dimensions: min={minimum}, max={maximum}, mean={mean}, median={median}, stddev={stddev}")

