class Problem:
    def __init__(self, cities=[]):
        self.cities = cities

    def __len__(self):
        return len(self.cities)

    def __iter__(self):
        return self.cities.__iter__()
