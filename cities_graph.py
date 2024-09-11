
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

                graph[starting_city] = {} # Populates the main graph
                for neighbor in neighbors:
                    dest, dist = neighbor.split('(')
                    dist = float(dist.strip(')'))
                    graph[starting_city][dest] = dist

        return graph
    
    

