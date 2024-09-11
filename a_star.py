import sys
from a_star_algo import AStarAlgo

# I know that I want to pass the args to main
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