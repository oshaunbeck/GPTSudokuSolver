from Data import Board, BoardUtils, Tests
from Logic import Solve

sudoku = Board()
util = BoardUtils()
solve = Solve()
test = Tests()

while True:

    response = input("1: Generate New Board\t2: Solve existing Board\n3:Check preloaded")

    if eval(response) == 1:

        generated_board = solve.generate_solvable()
        print(f"\nIncomplete Board:\n{generated_board.board}\n")

        input("Enter to solve.")

        solve.fill_board(0, 0, generated_board)

        print(print(f"\nSolution:\n\n{sudoku.board}"))

    if eval(response) == 2:

        sudoku = Board()

        util.str_to_board(sudoku)

        util.update(sudoku)

        print(f"\nInputted Board:\n\n{sudoku.board}")

        solve.fill_board(0, 0, sudoku)

        if solve.is_solved(sudoku):

            print(f"\n\nSolution:\n\n{sudoku.board}")
            print(f"\nBlocks{util.print_blocks(sudoku)}")

        else:

            print("\nNo solutions found")

    if eval(response) == 3:

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
        sudoku = Board.from_list(board_list)

        print(f"\nInputted Board:\n\n{sudoku.board}")

        solve.fill_board(0, 0, sudoku)

        if solve.is_solved(sudoku):

            print(f"\n\nSolution:\n\n{sudoku.board}")
            print(f"\nBlocks{util.print_blocks(sudoku)}")

        else:

            print("\nNo solutions found")


    if input("exit? y/n") == 'y':
        break