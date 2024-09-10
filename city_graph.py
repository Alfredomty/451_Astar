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
        graph = {}

        with open(filename, 'r') as file:
            for line in file:
                # Splitting at the dash to get the starting city and neighbors

                line_parts = line.strip().split('-') #['SanJose', 'SanFrancisco(48.4),Monterey(71.7),Fresno(149),SantaCruz(32.7)']
                starting_city = line_parts[0] #['SanJose']
                neighbors = line_parts[1].split(',') #The rest

                graph[starting_city] = {} # Populates the main graph
                for neighbor in neighbors:
                    dest, dist = neighbor.split('(')
                    dist = float(dist.strip(')'))
                    graph[starting_city][dest] = dist

        return graph
    
    def haversine_distance(self, city1, city2):
        lat1, lon1 = self.coords[city1]
        lat2, lon2 = self.coords[city2]

        radius = 3958.8

        lat1, lon1, lat2, lon2 =  map(np.radians, [lat1, lon1, lat2, lon2]) # Switching them to radians

        distance_between_lat = lat2 - lat1
        distance_between_lon = lon2 - lon1

        A = np.sin(distance_between_lat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(distance_between_lon / 2) ** 2
        d = radius * 2 * np.arcsin(np.sqrt(A))

        return d

