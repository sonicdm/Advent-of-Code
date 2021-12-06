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


def main():
    data = read_input("input.txt")
    example_data = read_input("example.txt")
    coordinates =  text_to_coordinate_pairs(data)
    lines_array = make_array_from_coordinates(coordinates, diagonal=True)
    number_of_overlaps = count_overlaps(lines_array)
    print(f"The number of overlaps is: {number_of_overlaps}")

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
    
    # fill the array with 0s
    array = [[0 for x in range(max_x + 1)] for y in range(max_y + 1)]
    
    # create an array of coordinates. setting each coordinate to 1 if set and increasing the count if set
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
            for x in range(start.x, end.x + 1):
                array[start.y][x] += 1
        # elif line is diagonal
        elif abs(calculate_slope(start,end)) == 1: # 45 degrees line
            # diagonal line
            #sort start and end by x
            start,end = sorted([start,end], key=lambda x: x.x)
            # calculate the slope of the line
            slope = calculate_slope(start,end)
            # plot the line
            for x in range(start.x, end.x + 1):
                y = int(start.y + slope * (x - start.x))
                array[y][x] += 1
                
        else:
            print(f"Line is not horizontal, vertical, or 45 degree: {start} to {end}")
                     
                      
            
    
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
        elif abs(self.slope) > 0:
            start,end = sorted([self.start, self.end], key=lambda coordinate: [coordinate.x, coordinate.y])
            slope = self.slope
            for x in range(start.x, end.x + 1):
                y = int(start.y + slope * (x - start.x))
                coordinates.append(Coordinate(x, y))
        else:
            raise Exception("Line is not vertical, horizontal or diagonal..somehow")

        return coordinates
    
    def slope(self):
        return (self.end.y - self.start.y) / (self.end.x - self.start.x)

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
