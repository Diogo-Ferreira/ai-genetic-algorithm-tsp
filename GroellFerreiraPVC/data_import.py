from GroellFerreiraPVC.city import City


def import_cities_from_file(file):
    with open(file) as f:
        return [City(*line.split()) for line in f]


def import_cities_from_gui(gui_data):
    return [City("test", x, y) for x, y in gui_data]
