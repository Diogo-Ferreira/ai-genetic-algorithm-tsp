from GroellFerreiraPVC.data_import import import_cities_from_gui, import_cities_from_file
from GroellFerreiraPVC.gui import Gui
from GroellFerreiraPVC.population import Population
from GroellFerreiraPVC.problem import Problem


def ga_solve(file=None, gui=True, maxtime=0):
    gui = Gui()

    if file is None:
        cities = import_cities_from_gui(gui.get_cities())
    else:
        cities = import_cities_from_file(file)

    problem = Problem(cities)

    [print(city) for city in problem]


def evolution_loop(problem, nb_solutions, max_iter=10):
    # Create solutions
    solutions = []
    for i in range(nb_solutions):
        solutions.append(problem.create_solution())

    population = Population(solutions=solutions)

    for i in range(max_iter):
        population.selection()
        population.crossover()
        #population.mutation()

        print(population)



if __name__ == "__main__":
    # ga_solve(file='res/pb005.txt')

    cities = import_cities_from_file(file='res/pb005.txt')
    my_fucking_problem = Problem(cities=cities)
    evolution_loop(problem=my_fucking_problem, nb_solutions=10)
