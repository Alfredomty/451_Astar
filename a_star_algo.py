import heapq
import numpy as np
from cities_graph import CitiesGraph

class AStarAlgo(CitiesGraph):
    """
    Class that extends the CitiesGraph Class and implements the A* algorithm 
    for searching the shortest path between cities
    Attr: 
        coords(dict): holds the coordinates (latitude, longitude) of cities.
        graph(dict) : holds the city connections and distances between them.
    """
    def __init__(self, coords_file, map_file):
        """
        Initializes the AStarAlgo object by loading city coordinates and the map of distances between them.
        Inherits from the CitiesGraph class.

        Params:
            coords_file(str) : File name containing the cities' coordinates (latitude, longitude).
            map_file(str) : File name containing the map of city connections and distances.
        Returns:
            None
        """
        super().__init__(coords_file, map_file)

    def calculate_haversine_distance(self, city1, city2) -> float: 
        """
        Calculates the Haversine distance between two cities using their latitude and longitude.
        
        Params:
            city1(str): Name of the first city
            city2(str): Name of the second city
        Returns:
            d(float): Haversine distance between the two cities in miles
        """
        lat1, lon1 = self.coords[city1]
        lat2, lon2 = self.coords[city2]

        radius = 3958.8

        lat1, lon1, lat2, lon2 =  map(np.radians, [lat1, lon1, lat2, lon2]) # Switching them to radians

        distance_between_lat = lat2 - lat1
        distance_between_lon = lon2 - lon1

        A = np.sin(distance_between_lat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(distance_between_lon / 2) ** 2
        d = radius * 2 * np.arcsin(np.sqrt(A))

        return d
    
    def search(self, start, goal) -> tuple:
        """
        Performs an A* search to find the shortest path between the start city and the goal city.

        Params: 
            start(str): name of the starting city
            goal(str): name of the goal city
        Returns:
            A tuple containing:
                - path: A list of city names that represent the shortest path from start to goal
                - current_score: The total distance from the shortest path
            
        """
        # Prio queue that stores (score, city, path)
        # Uses heaps to calculate
        queue = []
        heapq.heappush(queue, (0 + self.calculate_haversine_distance(start, goal), 0, start, [start]))

        # How much does it cost to go from city to next city (distance)
        score = {city: float('inf') for city in self.graph}
        score[start] = 0
        visited = set()

        while queue:
            _, current_score, current_city, path = heapq.heappop(queue)

            # Goal reached
            if current_city == goal:
                return path, current_score

            visited.add(current_city)

            for neighbor, dist in self.graph[current_city].items():

                # Ignore
                if neighbor in visited:
                    continue
                    
                temp_score = current_score + dist
                # Update if better score
                if temp_score < score[neighbor]:
                    score[neighbor] = temp_score
                    f_score = temp_score + self.calculate_haversine_distance(neighbor, goal)
                    heapq.heappush(queue, (f_score, temp_score, neighbor, path + [neighbor]))

        return None, float('inf')  # If no path found



