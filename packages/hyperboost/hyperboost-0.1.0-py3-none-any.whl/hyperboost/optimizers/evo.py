import random
import numpy as np
from hyperboost.utils.visual import plot_convergence


class EvolutionaryOptimizer:
    def __init__(self, space, objective_func):
        self.space = space
        self.objective_func = objective_func
        self.population = []
        self.history = []

    def _create_individual(self):
        return self.space.sample()[0]

    def _evaluate_population(self):
        scores = []
        for ind in self.population:
            score = self.objective_func(ind)
            scores.append((ind, score))
        return sorted(scores, key=lambda x: x[1])

    def _crossover(self, parent1, parent2):
        child = {}
        for name in self.space.param_names:
            if random.random() < 0.5:
                child[name] = parent1[name]
            else:
                child[name] = parent2[name]
        return child

    def _mutate(self, individual, mutation_rate=0.1):
        mutated = individual.copy()
        for name in self.space.param_names:
            if random.random() < mutation_rate:
                param = self.space.space_dict[name]
                mutated[name] = param.sample()[0]
        return mutated

    def optimize(self, population_size=20, generations=10):
        self.population = self.space.sample(population_size)
        for gen in range(generations):
            evaluated = self._evaluate_population()
            next_gen = [evaluated[0][0]]  # Elitism
            while len(next_gen) < population_size:
                p1, p2 = random.choices(evaluated[:5], k=2)
                child = self._crossover(p1[0], p2[0])
                child = self._mutate(child)
                next_gen.append(child)
            self.population = next_gen
            best_score = evaluated[0][1]
            self.history.append(best_score)
        plot_convergence(self.history)
        best = self._evaluate_population()[0][0]
        return best
