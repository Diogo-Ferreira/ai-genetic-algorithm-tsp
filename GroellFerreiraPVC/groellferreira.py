from GroellFerreiraPVC.data_import import import_cities_from_gui, import_cities_from_file
from GroellFerreiraPVC.gui import Gui
from GroellFerreiraPVC.problem import Problem


def ga_solve(file=None, gui=True, maxtime=0):
    gui = Gui()

    if file is None:
        cities = import_cities_from_gui(gui.get_cities())
    else:
        cities = import_cities_from_file(file)

    problem = Problem(cities)

    [print(city) for city in problem]


if __name__ == "__main__":
    ga_solve(file='res/pb005.txt')
