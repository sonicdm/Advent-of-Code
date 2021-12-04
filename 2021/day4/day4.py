"""
Advent of code 2021: Day 4 - Part 1
Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. Numbers are chosen at random, 
and the chosen number is marked on all boards on which it appears. (Numbers may not appear on all boards.) 
If all numbers in any row or any column of a board are marked, that board wins. (Diagonals don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass the time. 
It automatically generates a random order in which to draw numbers and a random set of boards (your puzzle input).

The score of the winning board can now be calculated. Start by finding the sum of all unmarked numbers on that board; 
Then, multiply that sum by the number that was just called when the board won to get the final score.

What is the score of the winning board?

Advent of code 2021: Day 4 - Part 2
On the other hand, it might be wise to try a different strategy: let the giant squid win.

You aren't sure how many bingo boards a giant squid could play at once, so rather than waste 
time counting its arms, the safe thing to do is to figure out which board will win last and 
choose that one. That way, no matter which boards it picks, it will win for sure.

Figure out which board will win last. Once it wins, what would its final score be?
"""

import itertools

def main():
    call_order, boards = load_bingo("input.txt")
    # test part 1
    test_example_bingo()
    # test part 2
    test_example_bingo(last_win=True)
    # playing to win
    print("Playing to win")
    play_bingo(call_order, boards, last_win=False)
    # playing to lose
    print("Playing to lose")
    play_bingo(call_order, boards, last_win=True)


def test_example_bingo(last_win=False):
    call_order, boards = load_bingo("example.txt")
    winner_score = play_bingo(call_order, boards, last_win=last_win)
    if not last_win:
        assert winner_score == 4512
    else:
        assert winner_score == 1924

def play_bingo(call_order: list, boards: list, diagonal=False, last_win = False) -> int:
    called_numbers = []
    winner: int = None
    winners = []
    bingo_boards = []
    bingo_board_numbers = []
    for i in call_order:
        called_numbers.append(i)
        last_called = i
        for board_number, board in enumerate(boards):
            if board in bingo_boards:
                continue
            bingo = check_bingo(board, called_numbers, diagonal=diagonal)
            if bingo:
                winner = (board, last_called, [n for n in called_numbers])
                winners.append(winner)
                bingo_boards.append(board)
                bingo_board_numbers.append(board_number)
                # print(f"BINGO! Board {board_number}")
                # display_board(board)
    if last_win:
        winner_board = winners[-1]
        winner_number = bingo_board_numbers[-1]
        name = "Loser"
    else:
        winner_board = winners[0]
        winner_number = bingo_board_numbers[0]
        name = "Winner"
    board_score = score_board(*winner_board)
    print(f"{name}: Board Number {winner_number} with score {board_score}")
    display_board(winner_board[0])
    return board_score

def score_board(board: list, last_called: int, called_numbers: list) -> int:
    """
    Start by finding the sum of all unmarked numbers.
    multiply un-marked numbers by the last called number.
    """
    board_vals = list(itertools.chain.from_iterable(board))
    unmarked_score = 0
    for x in board_vals:
        if x not in called_numbers:
            unmarked_score += x
    return last_called * unmarked_score




   
def load_bingo(filename: str) -> list:
    """
    Loads the bingo board
    :param filename:
    :return:
    """
    
    data = read_input(filename)
    call_order, boards = parse_board_data(data)
    return call_order, boards

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

def parse_board_data(data: list) -> list:
    """
    Parses the board data into a list of lists
    :param data:
    :return:
    """

    call_order = [int(i) for i in data.pop(0).split(",")]
    boards = read_boards_into_arrays(data)
    return call_order, boards

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
    if board:
        boards.append(board)
    return boards

def display_board(board: list, end="\n") -> None:
    """
    Displays the board
    :param board:
    :return:
    """
    for row in board:
        print(row)
    print(end=end)






def check_cross_bingo(board: list, called_numbers) -> bool:
    """
    Checks if the all values are in the diagonal of a 5x5 grid
    :param board:
    :param value:
    :return:
    """
    down_left_to_right_coordinates = [(0,0), (1,1), (2,2), (3,3), (4,4)]
    down_right_to_left_coordinates = [(0,4), (1,3), (2,2), (3,1), (4,0)]
    down_left_to_right_values = [get_board_coordinate_value(board, x, y) for x, y in down_left_to_right_coordinates]
    down_right_to_left_values = [get_board_coordinate_value(board, x, y) for x, y in down_right_to_left_coordinates]
    down_left = all(i in called_numbers for i in down_left_to_right_values)
    down_right = all(i in called_numbers for i in down_right_to_left_values)
    bingo = down_left or down_right
    return bingo

def check_bingo(board: list, called_numbers, diagonal=False) -> bool:
    """
    Checks if the value is in the row, column or diagonal of a 5x5 grid
    :param board:
    :param value:
    :return:
    """
    # check rows for bingo
    for row in board:
        if all(i in called_numbers for i in row):
            return True
    # check columns for bingo
    for x in range(5):
        col = [get_board_coordinate_value(board, x, y) for y in range(5)]
        if all(i in called_numbers for i in col):
            return True
    # check diagonals for bingo
    if diagonal:
        return check_cross_bingo(board, called_numbers)
    
    else:
        return False
        

def get_board_coordinate_value(board: list, x, y) -> str:
    """
    Inspects the board and returns the coordinates of the value
    :param board:
    :param value:
    :return:
    """
    return board[y][x]


def test_check_bingo():
    """
    Tests the check_cross_bingo function
    """
    test_check_cross_bingo_board = \
        """
        14 21 17 24  4
        10 16 15  9 19
        18  8 23 26 20
        22 11 13  6  5
        2  0 12  3  7
        """
    l_to_r_called_numbers = [14,16,23,6,7]
    r_to_l_called_numbers = [4,9,23,11,2]
    test_check_cross_bingo_board = [i.split() for i in test_check_cross_bingo_board.split("\n") if i.split()]
    test_check_cross_bingo_board = [list(map(int, i)) for i in test_check_cross_bingo_board]
    l_to_r_bingo = check_cross_bingo(test_check_cross_bingo_board, l_to_r_called_numbers)
    r_to_l_bingo = check_cross_bingo(test_check_cross_bingo_board, r_to_l_called_numbers)
    col_2_bingo_called_numbers = [21,16,8,11,0]
    col_2_bingo = check_bingo(test_check_cross_bingo_board, col_2_bingo_called_numbers)
    row_3_bingo_called_numbers = [18,8,23,26,20]
    row_3_bingo = check_bingo(test_check_cross_bingo_board, row_3_bingo_called_numbers)
    pass
    # test_check_cross_bingo_board = [i.split() for i in test_check_cross_bingo_board if i.split()]

if __name__ == "__main__":
    main()