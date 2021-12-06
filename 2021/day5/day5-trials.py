from __future__ import annotations
from dataclasses import dataclass, field

"""
Advent of Code 2021 - Day 5


Part 1:
Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 
are the coordinates of one end the line segment and x2,y2 are the coordinates of the other end.
These line segments include the points at both ends. 
In other words:
An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.
"""

import itertools

def main():
    # test_long_lines_overlap()
    data = read_input("input.txt")
    example_data = read_input("example.txt")
    # lines: list[Line] = parse_data_into_line_coordinate_pairs(data)
    # straight_lines = find_straight_lines(lines)
    coordinates =  text_to_coordinate_pairs(data)
    lines_array = make_array_from_coordinates(coordinates, diagonal=True)
    # display_array(lines_array, pad=1)
       
    number_of_overlaps = count_overlaps(lines_array)
    print(f"The number of overlaps is: {number_of_overlaps}")
    pass


def display_array(array: list[list[int]], pad=0):
    """
    Displays the array with a nice border and dots instead of 0s
    :param array:
    :return:
    """
    padding =  " " * pad
    top_border = "-" * (len(array[0]) + 2 + (pad*2))  
    bottom_border = top_border
    side_border = "|"
    print(top_border)
    for y in array:
        print(padding + side_border, end="")
        for x in y:
            print(padding, end="")
            if x == 0:
                print(".", end="")  # print a dot
                    
            else:
                print(x, end="")
            print(padding, end="")
            print(side_border, end="")
        print()
    pass

def count_overlaps(array: list[list[int]]) -> int:
    # return number of coordinates with a value of 2 or more
    total_overlaps = 0
    for y in array:
        for x in y:
            if x > 1:
                total_overlaps += 1
    return total_overlaps
    

def make_array_from_coordinates(coordinates: list[(Coordinate,Coordinate)], diagonal=False) -> list[list[int]]:
    
    # get the max bounds of the array:
    max_x = max([max([coordinate.x for coordinate in coordinate_pair]) for coordinate_pair in coordinates])
    max_y = max([max([coordinate.y for coordinate in coordinate_pair]) for coordinate_pair in coordinates])
    
    # create an array of coordinates. setting each coordinate to 1 if set and increasing the count if set
    
    array = [[0 for x in range(max_x + 1)] for y in range(max_y + 1)]
    for coord1,coord2 in coordinates:
        start,end = sort_coordinates([coord1,coord2])
        print(f"setting coordinates: {start} to {end}")
        # fill in the array with the coordinates between the start and end
        if start.x == end.x:
            # vertical line
            #interpolate the coordinates between the start and end
            full_line_coordinates = [Coordinate(x, start.y) for x in range(start.x, end.x + 1)]
            for y in range(start.y, end.y + 1):
                array[y][start.x] += 1
        elif start.y == end.y:
            # horizontal line
            full_line_coordinates = [Coordinate(x, start.y) for x in range(start.x, end.x + 1)]
            for x in range(start.x, end.x + 1):
                array[start.y][x] += 1
        # elif line is diagonal
        elif abs(calculate_slope(start,end)) == 1:
            # diagonal line
            # interpolate the coordinates between the start and end
            #sort start and end by x
            start,end = sorted([start,end], key=lambda x: x.x)
            # plot the slope of the line
            slope = calculate_slope(start,end)
            # plot the line
            for x in range(start.x, end.x + 1):
                y = int(start.y + slope * (x - start.x))
                array[y][x] += 1
                
        else:
            print(f"Line is not horizontal, vertical, or 45 degree: {start} to {end}")
                     
                
                
                
            for coordinate in full_line_coordinates:
                array[coordinate.y][coordinate.x] += 1
            
    
    return array

def sort_coordinates(coordinates: list[Coordinate]) -> list[Coordinate]:
    # sort coordinate pairs so the lowest x and y are first
    c1,c2 = sorted(coordinates, key=lambda x: x.x)  # sort by x
    c1,c2 = sorted([c1,c2], key=lambda x: x.y)  # sort by y
    return [c1,c2]
    

def calculate_slope(coord1: Coordinate, coord2: Coordinate) -> float:
    """
    Calculates the slope between two coordinates
    :param coord1:
    :param coord2:
    :return:
    """
    return (coord2.y - coord1.y) / (coord2.x - coord1.x)

def make_array_from_lines(lines: list[Line]) -> list[list[Coordinate]]:
    """
    Makes an array of coordinates from a list of lines
    :param lines:
    :return:
    """
    # get the max bounds of the array:
    max_x = max([max([line.end.x, line.start.x]) for line in lines])
    max_y = max([max([line.end.y, line.start.y]) for line in lines])
    
    # create an array of coordinates. setting each coordinate to 1 if set and increasing the count if set
    
    array = [[0 for x in range(max_x + 1)] for y in range(max_y + 1)]
    for line in lines:
        for coordinate in line.coordinates:
            print("setting coordinate: ", coordinate)
            array[coordinate.y][coordinate.x] += 1  # increase the count of the coordinate
    
    return array
    
    ...



def test_long_lines_overlap():
    """
    Test the long lines overlap
    :return:
    """
    # create 2 lines that intersect
    vertical_line = Line(Coordinate(0, 9), Coordinate(5, 9))
    # intersecting horizontal line
    horizontal_line = Line(Coordinate(0, 9), Coordinate(2, 9))

    print(f"The lines overlap: {vertical_line.intersects(horizontal_line)}")
    print(f"The lines overlap at coordinate: {vertical_line.intersection(horizontal_line)}")
    pass


def find_line_overlaps(lines: list[Line]) -> list[Line]:
    """
    Finds the line segments that overlap
    :param lines:
    :return:
    """
    
    horizontal_lines: list[Line] = [line for line in lines if line.is_horizontal]
    vertical_lines: list[Line] = [line for line in lines if line.is_vertical]
    
    horizontal_line_coordinates: list[Coordinate] = []
    for line in horizontal_lines:
        horizontal_line_coordinates.extend(line.coordinates)
    
    
    
    vertical_line_coordinates: list[Coordinate] = []
    for line in vertical_lines:
        vertical_line_coordinates.extend(line.coordinates)
    
    # find all horizontal lines that overlap_with other lines
    horizontal_line_overlaps: list[tuple[Line,Line]] = []
    for line in horizontal_lines:
        for other_line in vertical_lines:
            if line.overlaps(other_line):
                print(line.intersection(other_line))
                horizontal_line_overlaps.append((line, other_line))
    
    vertical_line_overlaps: list[tuple[Line,Line]] = []
    for line in vertical_lines:
        for other_line in horizontal_lines:
            if line.overlaps(other_line):
                vertical_line_overlaps.append((line, other_line))
    
    intersections: list[Coordinate] = []
    for line_pair in horizontal_line_overlaps:
        intersection = line_pair[0].intersection(line_pair[1])
        intersections.extend(intersection)
        
    for line_pair in vertical_line_overlaps:
        intersection = line_pair[0].intersection(line_pair[1])
        intersections.extend(intersection)
        
        
    
    
    horizontal_line_duplicates = sorted(find_duplicates(horizontal_line_coordinates), key=lambda x: x.x)
    vertical_line_duplicates = sorted(find_duplicates(vertical_line_coordinates), key=lambda coordinate: coordinate.y)
    overlap_coordinates = horizontal_line_duplicates + vertical_line_duplicates
    return overlap_coordinates

def text_to_coordinate_pairs(data: list[str]) -> list[Line]:
    """
    returns a list of coordinates that are start and end points of a single line
    """
    split_char = " -> "
    coordinates = []
    for line in data:
        pair_strings = line.split(split_char)
        start_string = pair_strings[0]
        end_string = pair_strings[1]
        start_coord = tuple([int(i) for i in start_string.split(",")])
        end_coord = tuple([int(i) for i in end_string.split(",")])
        # lines.append(Line(Coordinate(*start_coord), Coordinate(*end_coord)))
        coordinates.append((Coordinate(*start_coord), Coordinate(*end_coord)))    
    return coordinates

def find_duplicates(coordinates: list[Coordinate]) -> list[Coordinate]:
    """
    Finds the duplicates in a list of coordinates
    :param coordinates:
    :return:
    """
    duplicates: list[Coordinate] = []
    for coordinate in coordinates:
        if coordinates.count(coordinate) > 1:
            duplicates.append(coordinate)
    return duplicates


def count_coordinate_occurences(lines: list[Line]) -> dict:
    """
    Counts the occurences of coordinates
    :param coordinates:
    :param occurences:
    :return:
    """
    occurences: dict[Coordinate, int] = {}
    coordinates: list[Coordinate] = []
    for line in lines:
        print(line.coordinates)
        for coordinate in line.coordinates:
            coordinates.append(coordinate)
            
    for coordinate in coordinates:
        if coordinate in occurences:
            occurences[coordinate] += 1
        else:
            occurences[coordinate] = 1

    return occurences


@dataclass
class Coordinate:
    x: int
    y: int

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Coordinate):
            return self.x == __o.x and self.y == __o.y
        else:
            return False

    def __hash__(self) -> int:
        return hash(str(self))

    def _lt__(self, __o: Coordinate) -> bool:
        if self.x > __o.x and self.y > __o.y:
            return False

    def __gt__(self, __o: Coordinate) -> bool:
        if self.x > __o.x:
            return True
        elif self.x == __o.x and self.y > __o.y:
            return True
        else:
            return False


@dataclass
class Line:
    start: Coordinate
    end: Coordinate

    @property
    def length(self):
        return len(self.coordinates)

    @property
    def is_vertical(self):
        return self.start.x == self.end.x

    @property
    def is_horizontal(self):
        return self.start.y == self.end.y

    @property
    def is_diagonal(self):
        return self.start.x != self.end.x and self.start.y != self.end.y

    @property
    def coordinates(self):
        coordinates = []
        # sort the coordinates end is not always lower than start
        if self.is_vertical:
            coordinates.append(Coordinate(self.start.x, self.start.y))
            coordinates.append(Coordinate(self.end.x, self.end.y))
            start, end = sorted([self.start, self.end], key=lambda coordinate: coordinate.y)
        
        x2, y2 = sorted([self.end.y, self.end.y])
        if self.is_vertical:
            start, end = sorted([self.start, self.end], key=lambda coordinate: coordinate.y)
            vertical_range = range(start.y, end.y + 1)
            for y in vertical_range:
                coordinates.append(Coordinate(start.x, y))
        elif self.is_horizontal:
            start, end = sorted([self.start, self.end], key=lambda coordinate: coordinate.x)
            hor_range = range(start.x, end.x + 1)
            for x in hor_range:
                coordinates.append(Coordinate(x, start.y))
        elif self.is_diagonal:
            start,end = sorted([self.start, self.end], key=lambda coordinate: [coordinate.x, coordinate.y])
            diagonal_range = range(start.x, end.x + 1)
            for x in range(start.x, end.x + 1):
                for y in range(start.y, end.y + 1):
                    coordinates.append(Coordinate(x, y))
        else:
            raise Exception("Line is not vertical, horizontal or diagonal..somehow")

        return coordinates

    def intersects(self, other: Line):
        """
        Check if the line intersects with another line
        :param other:
        :return:
        """
        # get the coordinates of the lines
        coordinate_strings = [str(coordinate) for coordinate in self.coordinates]
        other_coordinate_strings = [str(coordinate) for coordinate in other.coordinates]
        return any(
            [
                coordinate_string in other_coordinate_strings
                for coordinate_string in coordinate_strings
            ]
        )

    def intersection(self, other: Line) -> list[Coordinate]:
        """
        Find the intersection point of two lines
        :param other:
        :return:
        """
        # get the coordinates of the lines
        coordinate_strings = [str(coordinate) for coordinate in self.coordinates]
        other_coordinate_strings = [str(coordinate) for coordinate in other.coordinates]
        intersection = set(self.coordinates).intersection(set(other.coordinates))
        return list(intersection)
    
    def overlaps(self, other: Line) -> bool:
        """
        Check if the line overlaps with another line
        :param other:
        :return:
        """
        # get the coordinates of the lines
        coordinate_strings = [str(coordinate) for coordinate in self.coordinates]
        other_coordinate_strings = [str(coordinate) for coordinate in other.coordinates]
        intersection = set(self.coordinates).intersection(set(other.coordinates))
        return len(intersection) > 1
    
    def overlap_points(self, other: Line) -> list[Coordinate]:
        """
        Returns list of common coordinates between two lines
        """
        if not self.overlaps(other):
            return []
        
        return list(set(self.coordinates).intersection(set(other.coordinates)))
        
            

    def __iter__(self):
        return iter(self.coordinates())

    def __eq__(self, other: Line):
        return self.start == other.start and self.end == other.end

    def __str__(self):
        return f"{self.start.x},{self.start.y} -> {self.end.x},{self.end.y}"

    def __hash__(self):
        return hash(self.start) + hash(self.end)


def parse_data_into_line_coordinate_pairs(data: list[str]) -> list[Line]:
    """
    returns a list of coordinates that are start and end points of a single line
    """
    split_char = " -> "
    lines = []
    for line in data:
        pair_strings = line.split(split_char)
        start_string = pair_strings[0]
        end_string = pair_strings[1]
        start_coord = tuple([int(i) for i in start_string.split(",")])
        end_coord = tuple([int(i) for i in end_string.split(",")])
        lines.append(Line(Coordinate(*start_coord), Coordinate(*end_coord)))
    return lines


def find_straight_lines(lines: list[Line]) -> list[tuple]:
    """
    find only lines that are horizonal or vertical
    :param lines:
    :return:
    """
    straight_lines: list[Line] = []
    for line in lines:
        if line.is_vertical or line.is_horizontal:
            straight_lines.append(line)
        else:
            continue
    return straight_lines


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


if __name__ == "__main__":
    main()
