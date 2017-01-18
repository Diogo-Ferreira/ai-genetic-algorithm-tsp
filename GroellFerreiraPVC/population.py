from GroellFerreiraPVC.solution import Solution, cross_between
import random

class Population:
    EVOLUTION_STEP_PERCENTAGE = 0.6
    MUTATION_PERCENTAGE = 0.4

    def __init__(self, solutions=[]):
        self.solutions = solutions
        self.best_solution = None
        self.cut_a = int(len(self.solutions[0]) * 0.25)
        self.cut_b = int(len(self.solutions[0]) * 0.75)

    def __str__(self):
        return str(self.solutions)

    def selection(self):
        selected_size = int(len(self.solutions) * self.EVOLUTION_STEP_PERCENTAGE)

        sorted_solutions = sorted(self.solutions, key=lambda e: e.fitness())

        self.solutions = sorted_solutions[:selected_size]
        '''selected_solutions = []
        for i in range(selected_size):
            selected_chromosome = self._wheel_selection(self.solutions)
            selected_solutions.append(selected_chromosome)
            self.solutions.remove(selected_chromosome)

        self.solutions  = selected_solutions'''

    def _wheel_selection(self, population):
        max = sum([c.fitness for c in population])
        pick = random.uniform(0, max)
        current = 0
        for chromosome in population:
            current += chromosome.fitness
            if current > pick:
                return chromosome

    def crossover(self):
        childs = []
        choices = self.solutions


        for sol_ix in range(len(self.solutions)):
            child_a, child_b = cross_between(self.solutions[sol_ix],self.solutions[(sol_ix + 1) % len(self.solutions)],self.cut_a,self.cut_b)
            childs.append(child_a)
            childs.append(child_b)
        self.solutions = childs

        """
        for _ in range(len(self.solutions)):
           candidate_a, candidate_b = random.choice(self.solutions),random.choice(self.solutions)
           child_a, child_b = Solution.cross_between(candidate_a, candidate_b,cut_a,cut_b)
           childs.append(child_a)
           childs.append(child_b)
        self.solutions = childs
        """

        """
        for sol_ix in range(len(self.solutions)):
            child_a,child_b = Solution.cross_between(self.solutions[sol_ix],self.solutions[(sol_ix+1) % len(self.solutions)])
            childs.append(child_a)
            childs.append(child_b)
        self.solutions = childs
        """
    def mutation(self):
        for _ in range(int(len(self.solutions)* self.MUTATION_PERCENTAGE)):
            chromosome = random.choice(self.solutions)
            chromosome.mutate()

    def find_best_solution(self):

        if len(self.solutions) > 0:
            self.best_solution = min(self.solutions, key=lambda e: e.fitness())
        else:
            return self.best_solution

