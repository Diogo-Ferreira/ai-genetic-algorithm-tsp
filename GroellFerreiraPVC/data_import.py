from GroellFerreiraPVC.city import City


def import_cities_from_file(file):
    with open(file) as f:
        return {line.split()[0]: City(*line.split()) for line in f}


def import_cities_from_gui(gui_data):
    return {'test %s %s' % (x,y): City('test %s %s' % (x,y), x, y) for x, y in gui_data}
