import math

from pygame.math import Vector2


class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.pos = Vector2(float(x),float(y))

    def __str__(self, *args, **kwargs):
        return "%s x: %s y: %s" % (self.name, self.x, self.y)
