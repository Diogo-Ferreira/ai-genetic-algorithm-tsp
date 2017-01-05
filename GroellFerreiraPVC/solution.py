import random


class Solution:
    def __init__(self, problem):
        self.problem = problem
        self.path = []

    def __len__(self):
        return len(self.path)

    def __iter__(self):
        return self.path.__iter__()

    def __getitem__(self, item):
        return self.path[item]

    @staticmethod
    def cross_between(sol_a, sol_b, cut_size=3):
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
        cross_point_a = random.randrange(0, len(sol_b) - 1 - cut_size)

        cross_point_b = cross_point_a + cut_size

        #cross_point_a, cross_point_b = 2, 5

        # Creates our children, with the sub cities between the 2 cutting points
        child_a, child_b = sol_a[cross_point_a:cross_point_b], sol_b[cross_point_a:cross_point_b]

        size = len(sol_a)

        for i in range(size):
            current_city_ix = (cross_point_b + i) % size

            current_a_from_parent, current_b_from_parent = sol_a[current_city_ix], sol_b[current_city_ix]

            # Is the current city from b parent in a child ?
            if current_b_from_parent not in child_a:
                child_a.append(current_b_from_parent)

            # Is the current city from a parent in b child ?
            if current_a_from_parent not in child_b:
                child_b.append(current_a_from_parent)

        # Rotates the child, so the first city are inside the cutting points
        Solution.rotate(child_a, cross_point_a)
        Solution.rotate(child_b, cross_point_a)

        return child_a, child_b

    @staticmethod
    def rotate(lst, x):
        lst[:] = lst[-x:] + lst[:-x]


if __name__ == "__main__":
    sol_a = Solution(None)
    sol_a.path = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    sol_b = Solution(None)
    sol_b.path = ['B', 'E', 'F', 'H', 'A', 'D', 'G', 'C']

    print(Solution.cross_between(sol_a, sol_b))
