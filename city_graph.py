import numpy as np

class CityGraph:
    def __init__(self, coords_file, map_file):
        self.coords = self.read_coords(coords_file)
        self.graph = self.read_map(map_file)
    
    def read_coords(self, filename):
        pass

    def read_map(self, filename):
        pass

