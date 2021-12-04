from pathlib import Path

input_path = Path(__file__).parent.absolute() / "input.txt"
with input_path.open() as f:
    numbers = list(f.read().splitlines())
example_input = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""
example_input = example_input.split('\n')

# numbers = [list(l) for l in example_input.split('\n')]
def calculate_power_consumption(numbers):
    epsilon = ""
    gamma = ""
    for bit in range(max(len(number) for number in numbers)):
        bits = [n[bit] for n in numbers]
        bit_gamma = max(set(bits), key=bits.count)
        bit_epsilon = min(set(bits), key=bits.count)
        epsilon += str(bit_epsilon)
        gamma += str(bit_gamma)

    print("Epsilon: ", epsilon)
    print("Gamma: ", gamma)
    print("Epsilon Int: ", int(epsilon, 2))
    print("Gamma Int: ", int(gamma, 2))
    power_consumption = int(epsilon, 2) * int(gamma, 2)
    print("Power Consumption: ", power_consumption)


def calculate_oxygen_generator_rating(numbers: list):
    data = numbers.copy()
    oxygen_generator_rating_binary = filter_bits(data, common=True)
    oxygen_generator_rating = int(oxygen_generator_rating_binary, 2)
    return oxygen_generator_rating


def calculate_c02_scrubber_rating(numbers: list) -> int:
    data = numbers.copy()
    oxygen_generator_rating_binary = filter_bits(data, common=False)
    oxygen_generator_rating = int(oxygen_generator_rating_binary, 2)
    return oxygen_generator_rating


def most_common_value(numbers: list) -> int:
    """
    find most common value in list
    """
    return max(set(numbers), key=numbers.count)


def least_common_value(numbers: list) -> int:
    """
    find least common value in list
    """
    return min(set(numbers), key=numbers.count)


def filter_bits(numbers: list, common=True) -> list:
    """
    filter list of numbers by bit
    determine the most common value (0 or 1) in the current bit position, and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 1 in the position being considered.
    """
    bit_count = max(len(number) for number in numbers)
    numbers = numbers.copy()
    
    for bit in range(bit_count):
        if len(numbers) == 1:
            break
        most_common = most_common_value([n[bit] for n in numbers])
        least_common = least_common_value([n[bit] for n in numbers])
        if most_common == least_common:
            common_bit = "1" if common else "0"
        else:
            common_bit = most_common if common else least_common
        numbers = [n for n in numbers if n[bit] == common_bit]
    return numbers[0]


print("Part1:")
calculate_power_consumption(numbers)

co2_scrubber_rating = calculate_c02_scrubber_rating(numbers)
print("C02 Scrubber Rating: ", co2_scrubber_rating)
oxygen_generator_rating = calculate_oxygen_generator_rating(numbers)
print("Oxygen Generator Rating: ", oxygen_generator_rating)
life_support_rating = oxygen_generator_rating * co2_scrubber_rating
print("Life Support Rating: ", life_support_rating) 
