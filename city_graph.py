import numpy as np

class CityGraph:
    def __init__(self, coords_file, map_file):
        self.coords = self.read_coords(coords_file)
        self.graph = self.read_map(map_file)
    
    def read_coords(self, filename):
        coords = {}

        with open(filename, 'r') as file:
            for line in file:
                city, coord = line.strip().split(':')
                latitude, longitude = map(float, coord.strip('()').split(','))
                coords[city] = (latitude,longitude)
        
        return coords

    def read_map(self, filename):
        pass

