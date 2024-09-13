import sys
import heapq
import numpy as np

# Originally, I had the two classes in two different files. I have added them to one single file for easier submission
class CitiesGraph:
    """
    A class to represent a graph of cities based on their geographical coordinates and distances between them.
    This class provides functionality to read city coordinates and connections from input files and stores them

    Attr:
        coords(dict) : Contains the cities' names as KEYS and coords (latitude, longitude) as VALUES.
        graph(dict): Represents the graph of cities, where each KEY is a city and the VALUE is another dictionary
            containing neighboring cities and the distance to them.

    """

    def __init__(self, coords_file, map_file):
        """
        Initializes the CitiesGraph object by reading the cities' coordinates and the connections (map) from the input files.

        Params:
            coords_file(str): The path to the file that contains the city coordinates in the format:
                City:(Latitude,Longitude)
            map_file(str): The path to the file that contains the map of city connections in the format:
                City1-City2(Distance),City3(Distance)
        """
        self.coords = self.read_coords(coords_file)
        self.graph = self.read_map(map_file)
    
    def read_coords(self, filename):
        """
        Reads the city coordinates from a file and stores them in a dictionary.

        Params:
            filename(str): The path to the file containing the city coordinates in the format:
                City:(Latitude,Longitude)

        Returns:
            coords(dict): Contains city names as KEYS and TUPLES of latitude and longitude as VALUES.
        """
        coords = {}

        with open(filename, 'r') as file:
            for line in file:
                city, coord = line.strip().split(':')
                latitude, longitude = map(float, coord.strip('()').split(','))
                coords[city] = (latitude,longitude)
        
        return coords

    def read_map(self, filename):
        """
        Reads the map of cities and their connections (neighbors and distances) from a file.

        Params:
            filename(str): The path to the file containing the map of city connections in the format:
                City1-City2(Distance),City3(Distance)

        Returns:
            graph(dict): Contains cities as KEYS , and the VALUE is another dictionary containing 
            neighboring cities and the distance to them.
        """
        graph = {}

        with open(filename, 'r') as file:
            for line in file:
                # Splitting at the dash to get the starting city and neighbors

                line_parts = line.strip().split('-') #['SanJose', 'SanFrancisco(48.4),Monterey(71.7),Fresno(149),SantaCruz(32.7)']
                starting_city = line_parts[0] #['SanJose']
                neighbors = line_parts[1].split(',') #The rest

                graph[starting_city] = {} 
                # Populates the main graph
                for neighbor in neighbors:
                    dest, dist = neighbor.split('(')
                    dist = float(dist.strip(')'))
                    graph[starting_city][dest] = dist

        return graph

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

        # Haversine Formula from the Assignment description
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

        # Adapted from https://www.geeksforgeeks.org/a-search-algorithm/
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

def main(start_city, goal_city):
    astar = AStarAlgo("coordinates.txt", "map.txt")

    path, distance = astar.search(start_city, goal_city)

    # Print statements
    print(f"From city: {start_city}\nTo city: {goal_city}")

    if path:
        print(f"Best Route: {start_city} to {goal_city}: {' -> '.join(path)}")
        print(f"Total distance: {distance:.2f} miles")
    else:
        print(f"No path found from {start_city} to {goal_city}")

if __name__ == "__main__":

    # Error check for args
    if len(sys.argv) != 3:
        print("Not enough arguments (expected 3)")
        print("Usage: python a_star.py <start_city> <goal_city>")
        sys.exit(1)
    
    start_city = sys.argv[1]
    goal_city = sys.argv[2]

    main(start_city, goal_city)