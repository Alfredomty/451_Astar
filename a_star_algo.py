import heapq
from city_graph import CityGraph

class AStarAlgo(CityGraph):
    # Will take the city graph and do a search on it
    def __init__(self, coords_file, map_file):
        super().__init__(coords_file, map_file)

    
    def search(self, start, goal):
        # Prio queue that stores (score, city, path)
        queue = []
        heapq.heappush(queue, (0 + self.haversine_distance(start, goal), 0, start, [start]))

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
                if neighbor in visited:
                    continue

                temp_score = current_score + dist
                if temp_score < score[neighbor]:
                    score[neighbor] = temp_score
                    f_score = temp_score + self.haversine_distance(neighbor, goal)
                    heapq.heappush(queue, (f_score, temp_score, neighbor, path + [neighbor]))

        return None, float('inf')  # If no path foun



