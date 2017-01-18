import random

from GroellFerreiraPVC.data_import import import_cities_from_file
#from GroellFerreiraPVC.problem import Problem

def rotate(lst, x):
    lst[:] = lst[-x:] + lst[:-x]

def cross_between(sol_a, sol_b, cross_point_a, cross_point_b, cut_size=3):
    """
    OX operator between 2 solutions
    Help here :
        http://stackoverflow.com/questions/11782881/how-to-implement-ordered-crossover
        http://www.dmi.unict.it/mpavone/nc-cs/materiale/moscato89.pdf
    :param sol_a:
    :param sol_b:
    :param cut_size:
    :return: the 2 crossed children
    """
    # cut_size = int(len(sol_a.path)/2)
    # cross_point_a = Solution.indexes[Solution.current_index%(len(sol_b) - 1 - cut_size)]
    # cross_point_a = random.randrange(0, len(sol_b) - 1 - cut_size)


    # cross_point_b = cross_point_a + cut_size

    # cross_point_a, cross_point_b = 2, 5

    # Creates our children, with the sub cities between the 2 cutting points
    child_a, child_b = sol_a.path[cross_point_a:cross_point_b], sol_b.path[cross_point_a:cross_point_b]

    size = len(sol_a)

    for i in range(size):
        current_city_ix = (cross_point_b + i) % size

        current_a_from_parent, current_b_from_parent = sol_a.path[current_city_ix], sol_b.path[current_city_ix]

        # Is the current city from b parent in a child ?
        if current_b_from_parent not in child_a:
            child_a.append(current_b_from_parent)

        # Is the current city from a parent in b child ?
        if current_a_from_parent not in child_b:
            child_b.append(current_a_from_parent)

    # Rotates the child, so the first city are inside the cutting points
    rotate(child_a, cross_point_a)
    rotate(child_b, cross_point_a)

    return Solution(sol_a.problem, child_a), Solution(sol_b.problem, child_b)

class Solution(object):
    indexes = [random.randrange(0, 20) for _ in range(20)]
    current_index = 0

    def __init__(self, problem, path=[]):
        self.problem = problem
        self.path = path
        self._fitness = None

    def __len__(self):
        return len(self.path)

    def __iter__(self):
        return [self.problem.cities[city_name] for city_name in self.path].__iter__()

    def __getitem__(self, item):
        return self.path[item]

    def __str__(self):
        return "%s : %s" % (str(self.path) ,self.fitness())




    def mutate(self):
        city_a, city_b = random.sample(range(0, len(self)), 2)
        self.path[city_a], self.path[city_b] = self[city_b], self[city_a]

    def fitness(self):
        if not self._fitness:
            total = 0
            last_city = self.problem.cities[self.path[0]]
            for city_name in self.path[1:]:
                current = self.problem.cities[city_name]
                total += current.pos.distance_to(last_city.pos)
                last_city = current
            total += last_city.pos.distance_to(self.problem.cities[self.path[0]].pos)
            self._fitness = total
        return self._fitness





if __name__ == "__main__":
    """
    cities = import_cities_from_file(file='res/pb005.txt')
    my_fucking_problem = Problem(cities=cities)
    sol_a = Solution(my_fucking_problem)
    sol_a.path = ['v0', 'v1', 'v2', 'v3', 'v4']

    print(sol_a.fitness)
    """

