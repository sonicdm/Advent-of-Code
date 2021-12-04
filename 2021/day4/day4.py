import random
import numpy as np
example_call_order = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1"""
example_call_order_list = [int(i) for i in example_call_order.split(",")]

example = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
 """
 
example_data = example.split("\n")

call_order = [int(i) for i in example_data.pop(0).split(",")]
 


def read_boards_into_arrays(example_boards: list) -> list:
    """
    Reads the example boards into a list of arrays
    :param example_boards:
    :return:
    """
    boards = []
    board = []
    for line in example_boards:
        line: list[str] = line.split()
        if not line:
            if board:
                boards.append(board)
                board = []
                continue
        else:   
            board.append([int(i) for i in line])
    return boards
boards = read_boards_into_arrays(example_data)

def display_board(board: list, end="\n") -> None:
    """
    Displays the board
    :param board:
    :return:
    """
    for row in board:
        print(row)
    print(end=end)
for board in boards:
    display_board(board)


def find_value_in_board(board: list, value: int) -> list[int,int]:
    """
    Finds the x,y coordinates of the value in the board
    :param board:
    :param value:
    :return:
    """
    for y, row in enumerate(board):
        for x, col in enumerate(row):
            if col == value:
                return [x, y]
    return None
    
 
# generate a 5x5 grid of unique random numbers between 0 and 26

# def make_board(n, min, max, unique=True):
#     board = np.zeros((n,n))
#     for i in range(n):
#         for j in range(n):
#             random_int = random.randint(min, max)
#             while random_int in board[:,j] or random_int in board[i,:]:
#                 random_int = random.randint(min, max)
#             board[i,j] = random_int
#     return board
# print(make_board(5, 0, 26))
# board_1 = make_board(5, 0, 26)
# board_2 = make_board(5, 0, 26)
# board_3 = make_board(5, 0, 26)
# print(grid)