import heapq
import numpy as np
from cities_graph import CitiesGraph

class AStarAlgo(CitiesGraph):
    # Will take the cities graph and do a search on it
    # Initializes the super CitiesGraph into A CitiesGraph object
    def __init__(self, coords_file, map_file):
        super().__init__(coords_file, map_file)

    def calculate_haversine_distance(self, city1, city2):
        lat1, lon1 = self.coords[city1]
        lat2, lon2 = self.coords[city2]

        radius = 3958.8

        lat1, lon1, lat2, lon2 =  map(np.radians, [lat1, lon1, lat2, lon2]) # Switching them to radians

        distance_between_lat = lat2 - lat1
        distance_between_lon = lon2 - lon1

        A = np.sin(distance_between_lat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(distance_between_lon / 2) ** 2
        d = radius * 2 * np.arcsin(np.sqrt(A))

        return d
    
    def search(self, start, goal):
        # Prio queue that stores (score, city, path)
        # Uses heaps to calculate
        queue = []
        heapq.heappush(queue, (0 + self.calculate_haversine_distance(start, goal), 0, start, [start]))

        # How much does it cost to go from city to next city
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
                if temp_score < score[neighbor]:
                    score[neighbor] = temp_score
                    f_score = temp_score + self.calculate_haversine_distance(neighbor, goal)
                    heapq.heappush(queue, (f_score, temp_score, neighbor, path + [neighbor]))

        return None, float('inf')  # If no path found



