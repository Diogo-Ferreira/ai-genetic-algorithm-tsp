"""

Implémentation du problème du voyageur de commerce à l'aide d'un algorithme génétique.

Etudiants: Groell Sarah, Ferreira Venancio Diogo


"""

import argparse
import time
import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import sys
from pygame.math import Vector2
import random
from _operator import attrgetter

# nombres de solutions identique à la suite pour considère qu'on "stagne", doit être assez élèves du faites
# qu'on utilise beaucoup d'aléatoire et que cela génère beaucoup de bruit
MAX_STAGNATION = 3000

# instance de l'interface graphique
global_gui = None

"""
========================================================================================================================
####################################################FONCTIONS###########################################################
========================================================================================================================
"""


def import_cities_from_file(file):
    with open(file) as f:
        return {line.split()[0]: City(*line.split()) for line in f}


def import_cities_from_gui(gui_data):
    return {'test %s %s' % (x, y): City('test %s %s' % (x, y), x, y) for x, y in gui_data}


def rotate(lst, x):
    lst[:] = lst[-x:] + lst[:-x]


def reverse_sublist(lst, start, end):
    lst[start:end] = lst[start:end][::-1]
    return lst


def cross_between(sol_a, sol_b, cross_point_a, cross_point_b):
    """
    croisement d'ordre 1 entre 2 solutions
    :param sol_a: première solution
    :param sol_b: seconde solution
    :return: 2 solutions enfants croisées
    """

    # Créer les enfants, avec les sous villes entre les 2 points de coupe
    child_a, child_b = sol_a.path[cross_point_a:cross_point_b], sol_b.path[cross_point_a:cross_point_b]

    size = len(sol_a)

    for i in range(size):
        current_city_ix = (cross_point_b + i) % size

        current_a_from_parent, current_b_from_parent = sol_a.path[current_city_ix], sol_b.path[current_city_ix]

        # Est-ce la ville courant du parent b se trouve dans l'enfant a ?
        if current_b_from_parent not in child_a:
            child_a.append(current_b_from_parent)

            # Est-ce la ville courant du parent a se trouve dans l'enfant b ?
        if current_a_from_parent not in child_b:
            child_b.append(current_a_from_parent)

    # Pivote les enfants, comme ça la première ville commence au point de coupe
    rotate(child_a, cross_point_a)
    rotate(child_b, cross_point_a)

    return Solution(sol_a.problem, child_a), Solution(sol_b.problem, child_b)


"""
========================================================================================================================
######################################################CLASSES###########################################################
========================================================================================================================
"""


class Gui(object):
    def __init__(self):
        self.screen_x = 500
        self.screen_y = 500

        self.city_color = [10, 10, 200]  # blue
        self.city_radius = 3

        self.font_color = [255, 255, 255]  # white

        pygame.init()
        self.window = pygame.display.set_mode((self.screen_x, self.screen_y))
        pygame.display.set_caption('IA TP2 PVC FERREIRA & GROELL')
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)

        pygame.event.wait()

    def wait(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_RETURN):
                    return

    def get_cities(self):
        cities = []
        self.draw(cities)

        collecting = True

        while collecting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_RETURN:
                    collecting = False
                elif event.type == MOUSEBUTTONDOWN:
                    cities.append(pygame.mouse.get_pos())
                    self.draw(cities)

        self.screen.fill(0)
        pygame.draw.lines(self.screen, self.city_color, True, cities)
        text = self.font.render("Un chemin, pas le meilleur!", True, self.font_color)
        textRect = text.get_rect()
        self.screen.blit(text, textRect)
        pygame.display.flip()

        return cities

    def draw(self, positions, draw_lines=False):
        self.screen.fill(0)
        for pos in positions:
            pygame.draw.circle(self.screen, self.city_color, pos, self.city_radius)
        if len(positions) > 1 and draw_lines:
            pygame.draw.lines(self.screen, self.city_color, True, positions)

        text = self.font.render("Nombre: %i" % len(positions), True, self.font_color)
        textRect = text.get_rect()
        self.screen.blit(text, textRect)
        pygame.display.flip()

    def send_solution(self, solution):
        solution = [sol for sol in solution]
        self.draw(solution, draw_lines=True)


class Population(object):
    """
    Définit une population, qui est un essemble de solutions
    """

    # le nombre de solutions qu'on prends à chaque séléction
    EVOLUTION_STEP_PERCENTAGE = 0.4

    # le nombre d'individus à mutés à chaque mutation
    MUTATION_PERCENTAGE = 0.35

    def __init__(self, solutions=[]):
        self.solutions = solutions
        self.cut_a = int(len(self.solutions[0]) * 0.25)
        self.cut_b = int(len(self.solutions[0]) * 0.75)
        self.EVOLUTION_STEP_PERCENTAGE = 0.4
        self.MUTATION_PERCENTAGE = 0.35
        self.selected_size = len(self.solutions)
        self.current_best = None

    def power_up(self):
        """
        Tente d'augmenter les chances de variété
        en boostant les mutations, attention la
        fenêtre de séléction est réduite pour les performances.
        """
        self.EVOLUTION_STEP_PERCENTAGE = 0.35
        self.MUTATION_PERCENTAGE = 0.65

    def sort_and_get_best_solution(self):
        """
        Tris les solutions et retourne la meilleur, attention
        cette méthode doit être appeler à chaque fois avant la
        séléction !
        :return:
        """
        self.solutions = sorted(self.solutions, key=attrgetter('fitness'))
        if len(self.solutions) > 0:
            self.current_best = self.solutions[0]
        return self.current_best

    def __str__(self):
        return str(self.solutions)

    def selection(self):
        """
        Séléction elliste, attention à appeler
         sort_and_get_best_solution pour effectuer le tris.
        :return:
        """
        self.selected_size = int(len(self.solutions) * self.EVOLUTION_STEP_PERCENTAGE)
        self.solutions = self.solutions[:self.selected_size]

    def crossover(self):
        """
        Effectue le croisement des paires de solutions
        """
        children = []
        for sol_ix in range(len(self.solutions)):
            child_a, child_b = cross_between(
                self.solutions[sol_ix],
                self.solutions[(sol_ix + 1) % len(self.solutions)],
                self.cut_a, self.cut_b
            )

            children.append(child_a)
            children.append(child_b)

        self.solutions = children

    def mutation(self):
        """
        Effectue les mutations sur des solutions prises au hasard
        :return:
        """
        n = int(len(self.solutions) * self.MUTATION_PERCENTAGE)
        indexes = random.sample(range(0, len(self.solutions)), n)
        for ix in indexes:
            self.solutions.append(self.solutions[ix].reverse_mutate())


class Problem(object):
    """
    Un problème créer une solution et
    contiens une références à toutes les villes
    dans un dictionnaire cities.
    """
    def __init__(self, cities={}):
        self.cities = cities

    def create_solution(self):
        """
        Créer une solution avec des
        villes dans un ordre au hasard
        :return: Solution
        """
        path = list(self.cities.keys())
        random.shuffle(path)
        return Solution(problem=self, path=path)


class Solution(object):

    def __init__(self, problem, path=[]):
        self.problem = problem
        self.path = path
        self.fitness = 0
        self.compute_fitness()

    def __len__(self):
        return len(self.path)

    def __str__(self):
        return "%s : %s" % (str(self.fitness), str(self.path))

    def __iter__(self):
        return [(
                    int(self.problem.cities[city_name].pos.x),
                    int(self.problem.cities[city_name].pos.y)
                ) for city_name in self.path].__iter__()

    def reverse_mutate(self):
        """
        Effectue la mutation, qui inverse le chemin
        entre 2 villes randoms.
        :return: nouvelles solution muté
        """
        city_a, city_b = random.sample(range(0, len(self.path)), 2)
        new_path = reverse_sublist(self.path, city_a, city_b)
        self.compute_fitness()
        return Solution(problem=self.problem, path=new_path)

    def compute_fitness(self):
        """
        Calcule le score courant de la solution, remarquez qu'on utilise
        les vec2 de pygame pour augmenter les performances du calcul de distance
        :return:
        """
        total = 0
        last_city = self.problem.cities[self.path[0]]
        for city_name in self.path[1:]:
            current = self.problem.cities[city_name]
            total += current.pos.distance_to(last_city.pos)
            last_city = current
        total += last_city.pos.distance_to(self.problem.cities[self.path[0]].pos)
        self.fitness = total


class City(object):
    def __init__(self, name, x, y):
        self.name = name
        self.pos = Vector2(float(x), float(y))

    def __str__(self):
        return "%s x: %s y: %s" % (self.name, self.pos.x, self.pos.y)


def ga_solve(file=None, gui=True, max_time=60):
    global global_gui

    if gui and not global_gui:
        global_gui = Gui()

    if file:
        cities = import_cities_from_file(file)
    else:
        cities = import_cities_from_gui(global_gui.get_cities())

    problem = Problem(cities=cities)

    best_solution = evolution_loop(problem=problem, nb_solutions=20, max_time=max_time)

    return best_solution.fitness, best_solution.path


def evolution_loop(problem, nb_solutions, max_time):

    solutions = []
    current_time_left = max_time
    current_stagnation = 0
    current_best_solution = None
    boosted = False

    global global_gui

    # Créations des solutions
    for i in range(nb_solutions):
        solutions.append(problem.create_solution())

    population = Population(solutions=solutions)

    quart_of_time = max_time / 4

    while current_time_left > 0 and current_stagnation < MAX_STAGNATION:
        start_time = time.time()

        # début d'un cycle d'évolution
        last_solution = population.sort_and_get_best_solution()
        population.selection()
        population.crossover()
        population.mutation()
        population.sort_and_get_best_solution()
        # Fin d'un cycle

        elapsed_time = time.time() - start_time
        current_time_left -= elapsed_time

        if last_solution and last_solution.fitness == population.sort_and_get_best_solution().fitness:
            current_stagnation += 1
        else:
            current_stagnation = 0

        if not current_best_solution or population.sort_and_get_best_solution().fitness < current_best_solution.fitness:
            current_best_solution = population.sort_and_get_best_solution()

        if global_gui:
            global_gui.send_solution(population.sort_and_get_best_solution())

        # boost les coefficients de mutation et selection lorsqu'il reste peu de temps, afin de maximiser les chances
        if not boosted and current_time_left < quart_of_time:
            population.power_up()
            boosted = True

        # print(current_best_solution)
    return current_best_solution


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--nogui', action='store_true')
    parser.add_argument('--maxtime', default=60)
    parser.add_argument('filename',nargs='?',default=False)

    args = vars(parser.parse_args())

    print(ga_solve(file=args['filename'], gui=not args['nogui'], max_time=int(args['maxtime'])))

    if not args['nogui']:
        global_gui.wait()
