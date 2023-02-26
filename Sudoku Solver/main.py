import numpy as np

from Logic import Solve
from Data import Board, BoardUtils, Tests


test = Tests()

while True:

    response = input("1: Generate New Board\t2: Solve existing Board\n3:Check preloaded\t4: Generate String")

    if eval(response) == 1:

        print("Coming soon..")

    if eval(response) == 2:
        solve = Solve()
        util = BoardUtils()

        sudoku = Board()

        util.update(sudoku)

        util.str_to_board(sudoku)

        print(f"\nInputted Board:\n\n{sudoku.board}")

        solve.solve_board(sudoku)

        if solve.is_solved(sudoku):

            print(f"\nBlocks{util.print_blocks(sudoku)}")
            solve.display_counters()

        else:

            print("\nNo solutions found")

        # Re-initialize sudoku to the original board
        sudoku = Board()

    if eval(response) == 3:
        solve = Solve()

        util = BoardUtils()
        sudoku = Board()

        util.update(sudoku)

        board_list = [
    [3, 0, 6, 5, 0, 8, 4, 0, 0],
    [5, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 7, 0, 0, 0, 0, 3, 1],
    [0, 0, 3, 0, 1, 0, 0, 8, 0],
    [9, 0, 0, 8, 6, 3, 0, 0, 5],
    [0, 5, 0, 0, 9, 0, 6, 0, 0], 
    [1, 3, 0, 0, 0, 0, 2, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 7, 4],
    [0, 0, 5, 2, 0, 6, 3, 0, 0]
]
        util.str_to_board(sudoku, board_list)

        print(f"\nInputted Board:\n\n{sudoku.board}")

        solve.solve_board(sudoku)

        if solve.is_solved(sudoku):

            print(f"\n\nSolution:\n\n{sudoku.board}")
            print(f"\nBlocks{util.print_blocks(sudoku)}")
            solve.display_counters()

            if np.all(sudoku.board == test.TEST_SOLUTION_1):

                print("solution matches test solution")

            else:

                print("solution does not match test")

        else:

            print("\nNo solutions found")

        # Re-initialize sudoku to the original board
        sudoku = Board()

    if eval(response) == 4:
        solve = Solve()

        util = BoardUtils()
        sudoku = Board()

        util.update(sudoku)
        board_list = util.get_board_from_input()

        if input("Solve this puzzle? y/n") == 'y':
            sudoku = Board()

            util.str_to_board(sudoku, board_list)

            solve.solve_board(sudoku)

    if input("exit program? y/n") == 'y':
        break