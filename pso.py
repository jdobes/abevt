import numpy as np


class Particle:
    def __init__(self, swarm, position):
        self.swarm = swarm
        self.position = position
        self.position_best = self.position.copy()
        self.cost_best = np.Inf
        self.velocity = np.zeros(self.swarm.dimensions)


class Swarm:
    def __init__(self, cost_function = None, dimensions: int = 10):
        self.bounds = [-10,10]
        self.c1 = self.c2 = 2.0
        self.wstart = 0.9
        self.wend = 0.4
        self.particles_count = 50
        self.particles = []

        if not cost_function:
            raise ValueError("Missing cost function!")

        self.cost_function = cost_function
        self.dimensions = dimensions
        self.fes = 5000 * self.dimensions

        self.position_best = np.zeros(dimensions)
        self.cost_best = np.Inf

        self.init_particles()

    def init_particles(self):
        for _ in range(self.particles_count):
            self.particles.append(Particle(self, self.random_position()))

    def random_position(self):
        return np.random.uniform(self.bounds[0], self.bounds[1], self.dimensions)

    def is_in_bounds(self, pos):
        return all([x >= self.bounds[0] and x <= self.bounds[1] for x in pos])

    def simulate(self):
        w = self.wstart
        # Works only for fes % particles_count == 0
        iterations = int(self.fes / self.particles_count)
        w_diff = (self.wstart - self.wend) / iterations
        for _ in range(iterations):
            for particle in self.particles:
                particle.velocity = w * particle.velocity + self.c1 * np.random.rand() * (particle.position_best - particle.position) + \
                    self.c2 * np.random.rand() * (self.position_best - particle.position)
                particle.position += particle.velocity
                if not self.is_in_bounds(particle.position):
                    #print("Particle out of bounds!")
                    particle.position = self.random_position()
                cost = self.cost_function(particle.position)
                if cost < particle.cost_best:
                    particle.cost_best = cost
                    particle.position_best = particle.position.copy()
                    if cost < self.cost_best:
                        self.cost_best = cost
                        self.position_best = particle.position.copy()
            w -= w_diff
            #print(f"New w: {w}")
            #print(f"Iteration: {_}, Best cost: {self.cost_best}, Best position: {self.position_best}")
        print(f"Best cost: {self.cost_best}, Best position: {self.position_best}")
