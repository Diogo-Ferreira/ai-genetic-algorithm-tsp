from GroellFerreiraPVC.solution import Solution


class Population:
    EVOLUTION_STEP_PERCENTAGE = 0.6

    def __init__(self, solutions=[]):
        self.solutions = solutions

    def __str__(self):
        return str(self.solutions)

    def selection(self):
        selected_size = int(len(self.solutions) * self.EVOLUTION_STEP_PERCENTAGE)

        sorted_solutions = sorted(self.solutions, key=lambda e: e.fitness)

        self.solutions = sorted_solutions[:selected_size]

    def crossover(self):
        childs = []
        for sol_ix in range(len(self.solutions)):
            child_a,child_b = Solution.cross_between(self.solutions[sol_ix],self.solutions[(sol_ix+1) % len(self.solutions)])
            childs.append(child_a)
            childs.append(child_b)
        self.solutions = childs

    def mutation(self):
        for sol in self.solutions:
            sol.mutate()
