#!/usr/bin/env python3
from numpy import asarray

from pso import Swarm


def first_dejong(x):
    return sum(x**2)

def second_dejong(x):
    return sum(100 * (x[:-1] ** 2 - x[1:]) ** 2 + (1 - x[:-1]) ** 2)


if __name__ == "__main__":
    swarm = Swarm(cost_function=first_dejong)
    swarm.simulate()

    swarm = Swarm(cost_function=second_dejong)
    swarm.simulate()
