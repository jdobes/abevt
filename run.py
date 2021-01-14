#!/usr/bin/env python3
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

if __name__ == "__main__":
    for name, cost_function in COST_FUNCTIONS.items():
        for dimensions in [10, 30]:
            swarm = Swarm(bounds=BOUNDS[name], dimensions=dimensions, cost_function=cost_function)
            cost_best, position_best = swarm.simulate()
            print(f"{name}, {dimensions} dimensions: cost_best={cost_best}, position_best={position_best}")
