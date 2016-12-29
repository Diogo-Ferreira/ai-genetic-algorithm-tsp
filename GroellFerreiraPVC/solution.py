import random


class Solution:
    def __init__(self, problem):
        self.problem = problem
        self.path = []

    def __len__(self):
        return len(self.path)

    def __iter__(self):
        return self.path.__iter__()

    @staticmethod
    def cross_between(sol_a, sol_b, cut_size=3):
        """
        Gives the cross solutions between 2 solutions
        :param sol_a:
        :param sol_b:
        :param cut_size:
        :return: solution who resulted from the crossment
        """
        cross_point_a = random.randrange(0, len(sol_b) - 1 - cut_size)

        cross_point_b = cross_point_a + cut_size

        sequence = sol_b.path[1:4]

        sol_a_prepared = ['*' if sol in sequence or ix in range(cross_point_a, cross_point_b) else sol for ix, sol in
                          enumerate(sol_a)]

        print(sol_a_prepared)

        Solution.push_solution(sol_a_prepared, 'B', cross_point_a, cross_point_b)

    @staticmethod
    def push_solution(sol, elem, first_point, second_point):
        """
        Replaces the * in the solutions by the item
        :param sol:
        :param elem:
        :param first_point: first point of cut
        :param second_point: last point of cut (Usually first_point + 3)
        :return:
        """
        sol_left_part = sol[:first_point]
        sol_right_part = sol[second_point:]
        print(sol_left_part)
        print(sol_right_part)


if __name__ == "__main__":
    sol_a = Solution(None)
    sol_a.path = ['A', 'B', 'C', 'D', 'E', 'F', 'F', 'G', 'H']
    sol_b = Solution(None)
    sol_b.path = ['B', 'E', 'F', 'H', 'A', 'D', 'G', 'C']

    Solution.cross_between(sol_a, sol_b)
