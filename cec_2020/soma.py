from ctypes import POINTER, c_double, byref
import numpy as np

FES_MULTIPLICATOR = 5000
PATH_LENGTH = 3
POP_SIZE = 50
PRT = 0.3
STEP = 0.33


# individual of the population. It holds parameters and fitness of the solution
class Individual:
    def __init__(self, params, fitness):
        self.params = params
        self.fitness = fitness

    def __repr__(self):
        return 'params: {} fitness: {}'.format(self.params, self.fitness)


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


def generate_prt_vector(dimensions):
    return np.random.choice([0, 1], dimensions, p=[PRT, 1-PRT])


# find leader of the population by its fitness (the lower the better)
def get_leader(population):
    return min(population, key = lambda individual: individual.fitness)


def run(cost_function, function_id, dimension, bounds):
    max_fes = FES_MULTIPLICATOR * dimension
    population = generate_population(cost_function, function_id, dimension, bounds)
    leader = get_leader(population)

    fes = 0
    best_fitnesses = []

    while True:
        if fes >= max_fes: # check fes
            break
        last_gen_leader = leader
        for individual in population:
            if fes >= max_fes: # check fes
                break
            if individual == last_gen_leader:
                continue
            prt_vector = generate_prt_vector(dimension)

            for t in np.arange(STEP, PATH_LENGTH, STEP):
                if fes >= max_fes: # check fes
                    break

                new_position = individual.params + (leader.params - individual.params) * t * prt_vector
                new_position = bounded(new_position, bounds)

                c_fitness = c_double()
                cost_function(new_position.ctypes.data_as(POINTER(c_double)), byref(c_fitness), dimension, 1, function_id)
                fitness = c_fitness.value
                fes += 1 # increment fes
                best_fitnesses.append(leader.fitness)

                if fitness < individual.fitness:
                    individual.fitness = fitness
                    individual.params = new_position
                    leader = get_leader(population)

    return best_fitnesses
