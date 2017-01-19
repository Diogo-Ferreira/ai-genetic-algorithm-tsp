import time

from GroellFerreiraPVC.data_import import import_cities_from_gui, import_cities_from_file
from GroellFerreiraPVC.gui import Gui
from GroellFerreiraPVC.population import Population
from GroellFerreiraPVC.problem import Problem

#in seconds
MAX_TIME = 90

MAX_STAGNATION = 3000


def ga_solve(file=None, gui=True, maxtime=0):
    gui = Gui()

    if file is None:
        cities = import_cities_from_gui(gui.get_cities())
    else:
        cities = import_cities_from_file(file)

    problem = Problem(cities=cities)
    evolution_loop(problem=problem, nb_solutions=20, gui=gui)
    while True:
        pass



def evolution_loop(problem, nb_solutions,gui):
    # Create solutions
    solutions = []
    current_time_left = MAX_TIME
    current_stagnation = 0
    current_best_solution = None

    for i in range(nb_solutions):
        solutions.append(problem.create_solution())

    population = Population(solutions=solutions)

    while current_time_left > 0 and current_stagnation < MAX_STAGNATION:
        start_time = time.time()

        population.selection()
        population.crossover()
        population.mutation()
        last_solution = population.best_solution
        population.find_best_solution()

        elapsed_time = time.time() - start_time
        current_time_left -= elapsed_time

        if last_solution and last_solution.fitness == population.best_solution.fitness:
            current_stagnation+=1
        else:
            current_stagnation = 0

        if  not current_best_solution or population.best_solution.fitness < current_best_solution.fitness:
            current_best_solution = population.best_solution

        print(population.best_solution)
        gui.send_solution(population.best_solution)

    gui.send_solution(current_best_solution)

    print(" BEST SOLUTION EVER BIIIM")
    print(current_best_solution)

if __name__ == "__main__":
    ga_solve(file='res/pb050.txt')
