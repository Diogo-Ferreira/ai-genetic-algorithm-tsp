from _operator import attrgetter, methodcaller

from GroellFerreiraPVC.solution import Solution, cross_between
import random


class Population:
    EVOLUTION_STEP_PERCENTAGE = 0.4
    MUTATION_PERCENTAGE = 0.35

    def __init__(self, solutions=[]):
        self.solutions = solutions
        self.best_solution = None
        self.cut_a = int(len(self.solutions[0]) * 0.25)
        self.cut_b = int(len(self.solutions[0]) * 0.75)
        self.sorted = False

    def __str__(self):
        return str(self.solutions)

    def selection(self):
        selected_size = int(len(self.solutions) * self.EVOLUTION_STEP_PERCENTAGE)

        if not self.sorted:
            self.solutions = sorted(self.solutions, key=attrgetter('fitness'))[:selected_size]
        else:
            self.solutions = self.solutions[:selected_size]

    def crossover(self):
        children = []
        choices = self.solutions

        for sol_ix in range(len(self.solutions)):
            child_a, child_b = cross_between(self.solutions[sol_ix], self.solutions[(sol_ix + 1) % len(self.solutions)],
                                             self.cut_a, self.cut_b)
            children.append(child_a)
            children.append(child_b)
        self.solutions = children

    def mutation(self):
        n = int(len(self.solutions) * self.MUTATION_PERCENTAGE)
        indexes = random.sample(range(0, len(self.solutions)), n)
        for ix in indexes:
            self.solutions.append(self.solutions[ix].reverse_mutate())
        self.sorted = False

    def find_best_solution(self):
        if len(self.solutions) > 0:
            self.solutions = sorted(self.solutions, key=attrgetter('fitness'))
            self.best_solution = self.solutions[0]
            self.sorted = True
        else:
            return self.best_solution
