import random

from GroellFerreiraPVC.solution import Solution


class Problem:
    def __init__(self, cities={}):
        self.cities = cities

    def __len__(self):
        return len(self.cities)

    def __iter__(self):
        return self.cities.items().__iter__()

    def create_solution(self):
        path = list(self.cities.keys())
        random.shuffle(path)
        return Solution(problem=self, path=path)
