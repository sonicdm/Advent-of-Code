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
from unicodedata import decomposition, name
from tqdm import tqdm
from tqdm.std import trange
import statistics
THREADED = False

def main():
    """
    given a set of horizontal positions, find the minimum fuel required to align them
    :return:
    """
    data = data_to_int(read_input('input.txt'))
    example_data = data_to_int(read_input('example.txt'))
    # index, fuel = align_coords(example_data)
    print("Calculating minimum fuel usage for example data")
    index, fuel = align_coords(example_data, increment=False)
    print(f'Calculated minimum fuel usage for example data: {fuel} at index: {index}')
    
    print("Calculating minimum fuel usage for example data with increment")
    index, fuel = align_coords(example_data, increment=True)
    print(f'Calculated minimum fuel usage for example data: {fuel} at index: {index}')
    
    print("Calculating minimum fuel usage for real data")
    index, fuel = align_coords(data, increment=False)
    print(f'Calculated minimum fuel usage for real data: {fuel} at index: {index}')
    
    print("Calculating minimum fuel usage for real data with increment")
    index, fuel = align_coords(data, increment=True)
    print(f'Calculated minimum fuel usage for real data: {fuel} at index: {index}')
     

def cost(start, end):
    return sum(range(abs(end - start)+1))

        
def align_coords(data: list, increment=False) -> tuple[int,int]:
    """
    Aligns the coordinates using the least amount of moves possible
    each move costs 1 fuel.
    16,1,2,0,4,2,7,1,2,14 = move to position 2
    :param data:
    :return:
    """
    # data = sorted(data)
    max_value = max(data)
    min_value = min(data)
    median = int(statistics.median(data))
    coordinate_range = list(range(min_value, max_value))
    fuel_min = None
    fuel_min_index = None
    fuel_usage = {}
    
    if not increment:
        # thanks /u/lianadelcongo i thought about median and then forgot to follow through. This solution was much better than brute force. 
        fuel = sum([abs(median-x) for x in data])
        return median, fuel

    with tqdm(total=len(coordinate_range), leave=True, desc=f'Finding minimum fuel: Destination: {min_value}') as pbar:
        # thanks /u/lianadelcongo for how to sum the cost with increment and not use a convoluted nesting of for loop. I failed to solve this one myself. 
        for i in range(min_value, max_value+1):
            fuel_usage[i] = sum([cost(i, x) for x in data])
            if fuel_min is None or fuel_usage[i] < fuel_min:
                fuel_min = fuel_usage[i]
                fuel_min_index = i
            pbar.set_description(f'Minimum fuel: {fuel_min}, Destination: {fuel_min_index}')
            pbar.update()
    # with tqdm(total=len(coordinate_range), desc="Destination: ") as pbar:
    # # with tqdm(total=len(coordinate_range), desc="Destination: ", position=0) as pbar:
    #     def check_value_fuel(value):
    #         """
    #         Checks the fuel usage for a given value
    #         :param value:
    #         :return:
    #         """
    #         pbar.set_description(f'Destination: {value} Fuel: 0')
    #         fuel = calculate_fuel_usage(data, value)
    #         pbar.update(1)
    #         pbar.set_description(f'Destination: {value} Fuel: {fuel}')
    #         return value,fuel
    #     if THREADED:
    #         with ThreadPoolExecutor(max_workers=1) as executor:
    #             futures = [executor.submit(check_value_fuel, value) for value  in coordinate_range]

    #         for future in as_completed(futures):
    #             value, fuel = future.result()
    #             # print(f'Value: {value} Fuel: {fuel}')
    #             fuel_usage[value] = fuel
    #             pbar.update(1)
    #             pbar.set_description(f'Destination: {value} Fuel: {fuel}')
    #     else:
    #         for value in coordinate_range:
    #             pbar.set_description(f'Destination: {value}')
    #             fuel = calculate_fuel_usage(data, value)
    #             fuel_usage[value] = fuel
    
    if not increment:
        fuel = sum([abs(median-x) for x in data])
        return median, fuel

    with tqdm(total=len(coordinate_range), leave=False, desc=f'Finding minimum fuel: Destination: {min_value}') as pbar:
        # thanks /u/lianadelcongo for how to sum the cost with increment
        for i in range(min_value, max_value+increment):
            fuel_usage[i] = sum([cost(i, x) for x in data])
            if fuel_min is None or fuel_usage[i] < fuel_min:
                fuel_min = fuel_usage[i]
                fuel_min_index = i
            pbar.set_description(f'Minimum fuel: {fuel_min}, Destination: {fuel_min_index}')
            pbar.update()
    # with tqdm(total=len(coordinate_range), desc="Destination: ") as pbar:
    # # with tqdm(total=len(coordinate_range), desc="Destination: ", position=0) as pbar:
    #     def check_value_fuel(value):
    #         """
    #         Checks the fuel usage for a given value
    #         :param value:
    #         :return:
    #         """
    #         pbar.set_description(f'Destination: {value} Fuel: 0')
    #         fuel = calculate_fuel_usage(data, value)
    #         pbar.update(1)
    #         pbar.set_description(f'Destination: {value} Fuel: {fuel}')
    #         return value,fuel
    #     if THREADED:
    #         with ThreadPoolExecutor(max_workers=1) as executor:
    #             futures = [executor.submit(check_value_fuel, value) for value  in coordinate_range]

    #         for future in as_completed(futures):
    #             value, fuel = future.result()
    #             # print(f'Value: {value} Fuel: {fuel}')
    #             fuel_usage[value] = fuel
    #             pbar.update(1)
    #             pbar.set_description(f'Destination: {value} Fuel: {fuel}')
    #     else:
    #         for value in coordinate_range:
    #             pbar.set_description(f'Destination: {value}')
    #             fuel = calculate_fuel_usage(data, value)
    #             fuel_usage[value] = fuel
    
    # for k,v in fuel_usage.items():
    #     if fuel_min is None or fuel_min > v:
    #         fuel_min = v
    #         fuel_min_index = k
    
    return fuel_min_index, fuel_min 
        
        

def calculate_fuel_usage(data:list[int], destination: int, inc: int=1) -> int:
    
    """
    Calculates the fuel usage for a given position. One fuel unit is used for each move.
    incrementing cost by inc per step
    """
    # remove the destination value from the list and remove the duplicates
    # origins = [x for x in data if x != destination]
    origin_set = set(data)
    data_min = min(origin_set)
    data_max = max(origin_set)
    cost = 1
    fuel = 0
    
    # coordinates = list(range(data_min, data_max+1))
    

    
    fuel_by_origin = {}
    
    with tqdm(total=len(data), leave=False, desc=f"Destination: {destination} Fuel: {sum(fuel_by_origin.values())}") as pbar:
        if False:
            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = [executor.submit(lambda: cost(origin,destination)) for origin in data]
                for future in as_completed(futures):
                    origin_cost = future.result()
                    pbar.set_description(f"Destination: {destination} Total Fuel: {sum(fuel_by_origin.values())}")
                    fuel_by_origin[origin] = origin_fuel
                    pbar.update()
        else:    
            for origin in data:
                # for instance of source coordinate                 
                pbar.set_description(f"Destination: {destination} Total Fuel: {sum(fuel_by_origin.values())}")
                origin_fuel, origin_cost, origin = origin_to_destination_usage(origin, destination, cost, inc, pbar)
                fuel_by_origin[origin] = origin_fuel
                pbar.update()
        pbar.set_description(f"Destination: {destination} Fuel: {fuel}")
        # print(f'Moved {origin} to {destination}, Using {origin_fuel} units of fuel. Final Move Cost: {origin_cost}')
    # print(f'Moved {i} to {destination}. Costing {distance} fuel. Total used fuel: {fuel}')
    # print(f'Destination {destination} Total fuel: {fuel}')
    
    return fuel


def origin_to_destination_usage(origin: int, destination: int, cost, inc, parent_pbar) -> tuple[int,int,int]:
    """
    Calculates the fuel usage for a given origin and destination
    :param origin:
    :param destination:
    :return:
    """
    origin_fuel = 0
    origin_cost = cost
    distance = abs(origin - destination)
    
    with tqdm(total=distance, desc="Fuel: Cost: ", leave=False) as pbar2:
        for step in range(distance):
            pbar2.set_description(f"Source: {origin} Destination: {destination} Fuel: {origin_fuel} Cost: {origin_cost}")
            remaining_distance = abs(distance - (step))
            origin_fuel += origin_cost
            origin_cost += inc
            pbar2.update(1)
    return origin_fuel, origin_cost, origin
    
def data_to_int(data: list[list[str]]) -> list:
    """
    Converts the data to integers
    :param data:
    :return:
    """
    output = []
    for line in data:
        # line = 
        output.extend(list(map(int, line.split(','))))
    
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