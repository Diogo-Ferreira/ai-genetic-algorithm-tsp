import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import sys


class Gui:
    def __init__(self):
        self.screen_x = 500
        self.screen_y = 500

        self.city_color = [10, 10, 200]  # blue
        self.city_radius = 3

        self.font_color = [255, 255, 255]  # white

        pygame.init()
        self.window = pygame.display.set_mode((self.screen_x, self.screen_y))
        pygame.display.set_caption('Exemple')
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)

        pygame.event.wait()

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

    def draw(self, positions):
        self.screen.fill(0)
        for pos in positions:
            pygame.draw.circle(self.screen, self.city_color, pos, self.city_radius)
        pygame.draw.lines(self.screen, self.city_color, True, positions)

        text = self.font.render("Nombre: %i" % len(positions), True, self.font_color)
        textRect = text.get_rect()
        self.screen.blit(text, textRect)
        pygame.display.flip()

    def send_solution(self, solution):
        self.solution = [(int(city.x),int(city.y)) for city in solution]
        self.draw(self.solution)


if __name__ == "__main__":
    Gui()
