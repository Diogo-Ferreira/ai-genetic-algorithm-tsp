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

    problem = Problem(cities=cities)
    evolution_loop(problem=problem, nb_solutions=100, gui=gui)
    while True:
        pass



def evolution_loop(problem, nb_solutions,gui, max_iter=50):
    # Create solutions
    solutions = []
    for i in range(nb_solutions):
        solutions.append(problem.create_solution())

    population = Population(solutions=solutions)

    for i in range(max_iter):
        population.selection()
        population.crossover()
        population.mutation()
        population.find_best_solution()

        print(population.best_solution)
        gui.send_solution(population.best_solution)

        #print(population)



if __name__ == "__main__":
    ga_solve(file='res/pb010.txt')

    '''cities = import_cities_from_file(file='res/pb005.txt')
    my_fucking_problem = Problem(cities=cities)
    evolution_loop(problem=my_fucking_problem, nb_solutions=24)'''
