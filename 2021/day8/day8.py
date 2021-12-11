from concurrent.futures import thread
from functools import reduce
import string


zero = "abcefg"
one = "cf"
two = "acdeg"
three = "acdfg"
four = "bcdf"
five = "abdfg"
six = "abdefg"
seven = "acf"
eight = "abcdefg"
nine = "abcdfg"



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


long_example_input = read_input("example.txt")
data = read_input("input.txt")
single_line_example = [
    f"acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
]

unscrambled_example = [
    f"{' '.join([zero, one, two, three, four, five, six, seven, eight, nine])} | {zero} {five} {seven} {eight}"
]

def main():
    combined = []
    combined.extend(single_line_example)
    combined.extend(unscrambled_example)
    signal_input = list(split_signal_and_number(data))  
    step_1 = count_1_4_7_8([num[1] for num in signal_input])
    print(f"There are {step_1} 1, 4, 7, 8 in the signal")
    numbers = []
    for signal in signal_input:
        print(f"{signal[0]} | {signal[1]}")
        unscrambled = descramble(signal)
        # decoded_number = decode_patterns(signal[1], unscrambled)
        numbers.append(unscrambled)
        print(f"decoded: {signal[1]} to {unscrambled}")
        
    print(f"The numbers are {numbers}")
    print(f"The sum of the numbers is {sum(numbers)}")
    
    
def decode_patterns(number, unscrambled_positions)-> int:
    zero = "abcefg"
    one = "cf"
    two = "acdeg"
    three = "acdfg"
    four = "bcdf"
    five = "abdfg"
    six = "abdefg"
    seven = "acf"
    eight = "abcdefg"
    nine = "abcdfg"
    
    real_number_patterns = {
        zero: 0,
        one: 1,
        two: 2,
        three: 3,
        four: 4,
        five: 5,
        six: 6,
        seven: 7,
        eight: 8,
        nine: 9
    }
    
    decoded_number = ""
    for digit in number:
        decoded_digit = ""
        for letter in digit:
            decoded_digit += unscrambled_positions[letter]
        decoded_digit = "".join(sorted(decoded_digit))
        decoded_number += str(real_number_patterns[decoded_digit])
    
    return int(decoded_number)
        


def count_1_4_7_8(data: list[list[str]]) -> int:
    total = 0
    for signal in data:
        signal_lengths = list(map(lambda x: len(x), signal))
        total += sum(signal_lengths.count(x) for x in [2, 4, 3, 7])
    return total


def descramble(signal: list[list[str,str]]) -> str:
    known_numbers = {k: "" for k in range(10)}
    number_keys, number_value = signal
    known_numbers.update(get_known_number_patterns(signal[0]))
    # patterns = sorted([set(pattern) for pattern in number_keys if pattern not in known_numbers.values()], key=len)
    patterns = sorted([set(pattern) for pattern in number_keys], key=len)
    p_copy = patterns.copy()
    seven = patterns[1]
    four = patterns[2]
    eight = patterns[9]
    one = patterns[0]
    def sort1(x):
        nonlocal patterns, four, seven
        s1 = seven.issubset(x)
        s2 = len(four & x)
        return (s1,s2)
    
    def sort2(x):
        nonlocal patterns, four, seven
        s1 = four.issubset(x)
        s2 = seven.issubset(x)
        return (s1,s2)
    
    
    p_copy[3:6] = sorted(p_copy[3:6], key=lambda x: (p_copy[1].issubset(x), len(p_copy[2] & x)))
    # p_copy[6:9] = sorted(patterns[6:9], key=sort1)
    p_copy[6:9] = sorted(p_copy[6:9], key=lambda x: (p_copy[2].issubset(x), p_copy[1].issubset(x)))
    # p_copy[6:9] = sorted(patterns[6:9], key=sort2)
    decoded_patterns = [p_copy[idx] for idx in (7, 0, 3, 5, 2, 4, 6, 1, 9, 8)]
    # for idx in (7, 0, 3, 5, 2, 4, 6, 1, 9, 8):
    #     decoded_patterns[idx] = p_copy[idx]
    
    digits = ""
    
    for digit in number_value:
        digit = set(digit)
        for idx,pattern in enumerate(decoded_patterns):
            if set(digit) == set(pattern):
                digits += str(idx)
                break
    return int(digits)
    
    
    


def descramble_signal(signal: list[list[str], list[str]]) -> list[str]:
    """
    expected output:
    0:      1:      2:      3:      4:
     aaaa    ....    aaaa    aaaa    ....
    b    c  .    c  .    c  .    c  b    c
    b    c  .    c  .    c  .    c  b    c
     ....    ....    dddd    dddd    dddd
    e    f  .    f  e    .  .    f  .    f
    e    f  .    f  e    .  .    f  .    f
     gggg    ....    gggg    gggg    ....

    5:      6:      7:      8:      9:
     aaaa    aaaa    aaaa    aaaa    a  a 
    b    .  b    .  .    c  b    c  b    c
    b    .  b    .  .    c  b    c  b    c
     dddd    dddd    ....    dddd    dd d
    .    f  e    f  .    f  e    f  .    f
    .    f  e    f  .    f  e    f  .    f
     gggg    gggg    ....    gggg    gg g
    """

    known_numbers = {k: "" for k in range(10)}
    scrambled_positions = {k: "" for k in string.ascii_lowercase[:7]}
    all_numbers, value = signal
    print(f"{all_numbers=}")
    print(f"{value=}")
    known_numbers.update(get_known_number_patterns(all_numbers))
    for known_number in known_numbers.values():
        if known_number:
            all_numbers.remove(known_number)
    print(f"{known_numbers=}")
    one_pattern = list(known_numbers[1])
    four_pattern = list(known_numbers[4])
    seven_pattern = list(known_numbers[7])
    eight_pattern = list(known_numbers[8])
    # compare 1 and 7 to get the right side and top of the number
    right_side = [p for p in seven_pattern if p in one_pattern]
    a = set(seven_pattern).difference(one_pattern).pop()
    scrambled_positions["a"] = a
    cf = set(one_pattern)
    bd = set(four_pattern).difference(cf)
    eg = set(eight_pattern).difference(set(list(bd)+list(cf)+[a]))
    g, nine = narrow_set(all_numbers, set.union(bd, [a],cf), known_positions=list(scrambled_positions.values()))
    known_numbers[9] = nine
    nine_pattern = list(nine)
    e = eg.difference(g).pop()
    scrambled_positions["e"] = e
    scrambled_positions['g'] = g
    b, zero = narrow_set(all_numbers, set.union(set([a,g,e]),cf), known_positions=list(scrambled_positions.values()))
    scrambled_positions["b"] = b
    known_numbers[0] = zero
    d = set(eight_pattern).difference(set(zero)).pop()
    scrambled_positions["d"] = d
    c, two = narrow_set(all_numbers, set.union(set([a,d,e,g])), known_positions=list(scrambled_positions.values()))
    scrambled_positions["c"] = c
    known_numbers[2] = two
    f = cf.difference(set(c)).pop()
    scrambled_positions["f"] = f

    print(f"{scrambled_positions=}")
    positions = {v: k for k, v in scrambled_positions.items()}

    pass
    return positions


def narrow_set(patterns, reference_pattern_set: set, known_positions: set) -> set:
    """
    take a list of patterns find the pattern that is not in the known patterns
    and is different from the reference pattern set by 1 letter
    
    acedgfb: 8    dddd
    cdfbe: 5     e    a
    gcdfa: 2     e    a
    fbcad: 3      ffff
    dab: 7       g    b
    cefabd: 9    g    b
    cdfgeb: 6     cccc
    eafb: 4
    cagedb: 0
    ab: 1
    """
    # cefabd
    for pattern in patterns:
        # if pattern in known_patterns:
        #     continue
        set_a, set_b = sorted([set(pattern), reference_pattern_set], key=len)
        if all(x in set_a for x in set_b):
            continue
        difference = set(pattern).difference(reference_pattern_set)
        intersection = set(pattern).intersection(reference_pattern_set)
        if len(reference_pattern_set.difference(intersection)) == 0:
            return difference.pop(), pattern


    return None, None

class Signal:
    def __init__(self, signal: str):
        self.signal, self.number = self.signal.split(" | ")
        self.number = self.number.split(" ")
        self.signal = self.signal.split(" ")


class Number:
    """Track positions that are found for this number. from a, b, c, d, e, f, g"""

    def __init__(self, number: str):
        self.number = number
        self.a = ""
        self.b = ""
        self.c = ""
        self.d = ""
        self.e = ""
        self.f = ""
        self.g = ""

    def print_number(self):
        print(f" {self.a*4} ")
        print(f"{self.b} {' '*4} {self.c}")
        print(f"{self.b} {' '*4} {self.c}")
        print(f" {self.d*4} ")
        print(f"{self.e} {' '*4} {self.f}")
        print(f"{self.e} {' '*4} {self.f}")
        print(f" {self.g*4} ")


def get_known_number_patterns(signal: list[str]) -> dict[int, str]:
    seven = ""
    one = ""
    four = ""
    eight = ""
    for pattern in signal:
        if len(pattern) == 3:
            seven = pattern
        elif len(pattern) == 2:
            one = pattern
        elif len(pattern) == 4:
            four = pattern
        elif len(pattern) == 7:
            eight = pattern
        if all([seven, one, four, eight]):
            return {7: seven, 1: one, 4: four, 8: eight}
    return {7: seven, 1: one, 4: four, 8: eight}


def split_signal_and_number(data: list[str]) -> list[list[str]]:
    for signal, number in map(lambda x: x.split(" | "), data):
        yield [signal.split(" "), number.split(" ")]


if __name__ == "__main__":
    main()
