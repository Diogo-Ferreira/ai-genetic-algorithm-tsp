import math


class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = float(x)
        self.y = float(y)

    def distance_from(self, city):
        return math.sqrt((self.x - city.x) ** 2 + (self.y - city.y) ** 2)

    def __str__(self, *args, **kwargs):
        return "%s x: %s y: %s" % (self.name, self.x, self.y)
