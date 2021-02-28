from ctypes import POINTER, c_double, byref
import numpy as np
import random

FES_MULTIPLICATOR = 5000
POP_SIZE = 50
F = 0.5
CR = 0.9

TAU_F = 0.1
TAU_CR = 0.1


# individual of the population. It holds parameters, fitness of the solution, CR and F
class Individual:
    def __init__(self, params, fitness):
        self.params = params
        self.fitness = fitness
        self.f = F
        self.cr = CR

    def __repr__(self):
        return 'params: {} fitness: {}, F: {}, CR: {}'.format(self.params, self.fitness, self.f, self.cr)


def bounded(params, bounds):
    return np.array([np.random.uniform(bounds[0], bounds[1])
            if params[d] < bounds[0] or params[d] > bounds[1] 
            else params[d] 
            for d in range(len(params))])


# generate individual params
def generate_individual(cost_function, function_id, dimensions, bounds):
    params = np.random.uniform(bounds[0], bounds[1], dimensions)
    fitness = c_double()
    # writes to fitness var
    cost_function(params.ctypes.data_as(POINTER(c_double)), byref(fitness), dimensions, 1, function_id)
    return Individual(params, fitness.value)


# generate initial population
def generate_population(cost_function, function_id, dimensions, bounds):
    return [generate_individual(cost_function, function_id, dimensions, bounds) for _ in range(POP_SIZE)]


def select_individuals(population, individual, count):
    population_copy = population.copy()
    population_copy.remove(individual)
    return random.sample(population_copy, count)


def run(cost_function, function_id, dimension, bounds):
    max_fes = FES_MULTIPLICATOR * dimension
    population = generate_population(cost_function, function_id, dimension, bounds)

    fes = 0
    best_fitnesses = []

    best_fitness = population[0].fitness

    while True:
        if fes >= max_fes: # check fes
            break
        for individual in population:
            # First mutate F and CR
            if np.random.uniform(0,1) < TAU_F:
                new_f = TAU_F + np.random.uniform(0,1) * (1-TAU_F)
            else:
                new_f = individual.f
            
            if np.random.uniform(0,1) < TAU_CR:
                new_cr = np.random.uniform(0,1)
            else:
                new_cr = individual.cr
            
            # Mutate 3 individuals, DE/rand/1
            selected_individuals = select_individuals(population, individual, 3)
            mutated_individual_params = [selected_individuals[0].params[d] + new_f * (selected_individuals[1].params[d] - selected_individuals[2].params[d]) for d in range(dimension)]
            mutated_individual_params = bounded(mutated_individual_params, bounds)

            # Crossbreed individual and mutated individual
            new_individual_params = []
            for j in range(dimension):
                if np.random.uniform(0,1) < new_cr or j == int(np.random.uniform(0,dimension)):
                    new_individual_params.append(mutated_individual_params[j])
                else:
                    new_individual_params.append(individual.params[j])
            new_individual_params = np.array(new_individual_params)

            c_fitness = c_double()
            cost_function(new_individual_params.ctypes.data_as(POINTER(c_double)), byref(c_fitness), dimension, 1, function_id)
            fitness = c_fitness.value

            if fitness < individual.fitness:
                individual.fitness = fitness
                individual.params = new_individual_params
                individual.f = new_f
                individual.cr = new_cr
                
                if fitness < best_fitness:
                    best_fitness = fitness
            
            best_fitnesses.append(best_fitness)
            fes += 1 # increment fes
            if fes >= max_fes: # check fes
                break


    return best_fitnesses
