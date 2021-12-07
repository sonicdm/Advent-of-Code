"""
The crab submarines all need to be aligned before they'll have enough power to blast a large enough hole for your submarine to get through. However, it doesn't look like they'll be aligned before the whale catches you! Maybe you can help?

There's one major catch - crab submarines can only move horizontally.

You quickly make a list of the horizontal position of each crab (your puzzle input). Crab submarines have limited fuel, so you need to find a way to make all of their horizontal positions match while requiring them to spend as little fuel as possible.

For example, consider the following horizontal positions:

16,1,2,0,4,2,7,1,2,14
This means there's a crab with horizontal position 16, a crab with horizontal position 1, and so on.

Each change of 1 step in horizontal position of a single crab costs 1 fuel. You could choose any horizontal position to align them all on, but the one that costs the least fuel is horizontal position 2:

Move from 16 to 2: 14 fuel
Move from 1 to 2: 1 fuel
Move from 2 to 2: 0 fuel
Move from 0 to 2: 2 fuel
Move from 4 to 2: 2 fuel
Move from 2 to 2: 0 fuel
Move from 7 to 2: 5 fuel
Move from 1 to 2: 1 fuel
Move from 2 to 2: 0 fuel
Move from 14 to 2: 12 fuel
This costs a total of 37 fuel. This is the cheapest possible outcome; more expensive outcomes include aligning at position 1 (41 fuel), position 3 (39 fuel), or position 10 (71 fuel).

Determine the horizontal position that the crabs can align to using the least fuel possible. How much fuel must they spend to align to that position?
    """
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


def main():
    """
    given a set of horizontal positions, find the minimum fuel required to align them
    :return:
    """
    data = data_to_int(read_input('input.txt'))
    example_data = data_to_int(read_input('example.txt'))
    # index, fuel = align_coords(example_data)
    index, fuel = align_coords(data)
    
    
    print(f'Used Fuel: {fuel}, Moved to {index}')
    
def align_coords(data: list) -> tuple[int,int]:
    """
    Aligns the coordinates using the least amount of moves possible
    each move costs 1 fuel.
    16,1,2,0,4,2,7,1,2,14 = move to position 2
    :param data:
    :return:
    """
    threaded = True
    # data = sorted(data)
    max_value = max(data)
    min_value = min(data)
    most_common_value = max(set(data), key=data.count)
    largest_difference = max_value - min_value
    smallest_difference_for_all_values = max_value - most_common_value
    unique_values = set(data)
    coordinate_range = list(range(min_value, max_value+1))
    fuel_min = None
    fuel_min_index = None
    fuel_usage = {}
    with tqdm(total=len(unique_values)) as pbar:
        def check_value_fuel(value):
            """
            Checks the fuel usage for a given value
            :param value:
            :return:
            """
            fuel = calculate_fuel_usage(data, value)
            pbar.update(1)
            return value,fuel
        if threaded:
            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = [executor.submit(check_value_fuel, value) for value  in unique_values]

            for future in as_completed(futures):
                value, fuel = future.result()
                print(f'Value: {value} Fuel: {fuel}')
                fuel_usage[value] = fuel
        else:
            for value in coordinate_range:
                fuel = calculate_fuel_usage(data, value)
                fuel_usage[value] = fuel
    
    
    for k,v in fuel_usage.items():
        if fuel_min is None or fuel_min > v:
            fuel_min = v
            fuel_min_index = k
    
    return fuel_min_index, fuel_min 
        
        

def calculate_fuel_usage(data:list[int], destination: int, inc: int=1) -> int:
    
    """
    Calculates the fuel usage for a given position. One fuel unit is used for each move.
    """
    # remove the destination value from the list and remove the duplicates
    # origins = [x for x in data if x != destination]
    origin_set = set(data)
    data_min = min(origin_set)
    data_max = max(origin_set)
    cost = 1
    fuel = 0
    coordinates = list(range(data_min, data_max+1))
    for coordinate in coordinates:
        # print(f'Distance: {distance} Instance Count: {instance_count}')
        # occurences = [o for o in data if o == i]
        # print(f'Occurences: {occurences} Number of occurences: {len(occurences)}')
        distance = abs(destination - coordinate)
        instance_count = data.count(coordinate)
        move_fuel = 0
        # for each step of distance we need to increment cost and increase move_fuel
        for instance in range(instance_count):
            move_cost = cost
            for step in range(distance):
                step_distance = abs(distance - step)
                move_fuel += move_cost
                move_cost += inc
  
        fuel += move_fuel
        # print(f'Moved {instance_count} occurences of {coordinate} to {destination}, Using {move_fuel} units of fuel. ')
        # print(f'Moved {i} to {destination}. Costing {distance} fuel. Total used fuel: {fuel}')
    # print(f'Destination {destination} Total fuel: {fuel}')
    return fuel
    
    
def data_to_int(data: list[list[str]]) -> list:
    """
    Converts the data to integers
    :param data:
    :return:
    """
    output = []
    for line in data:
        line = [int(x) for x in line.split(',')]
        output.extend(line)
    
    return output


def read_input(filename: str) -> list:
    """
    Reads the input into a list
    :param filename:
    :return:
    """
    from pathlib import Path

    input_path = Path(__file__).parent.absolute() / filename
    with input_path.open() as f:
        data = list(f.read().splitlines())
    return data



if __name__ == '__main__':
    main()