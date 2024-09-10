

def main():
    text = "SanJose-SanFrancisco(48.4),Monterey(71.7),Fresno(149),SantaCruz(32.7)"
    line_parts = text.strip().split('-')
    starting_city = line_parts[0] # ['SanJose']
    neighbors = line_parts[1].split(',')
    print(line_parts)
    print(starting_city)
    print(neighbors)
if __name__ == "__main__":
    main()