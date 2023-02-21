from Data import Board, BoardUtils, Tests
from Logic import Solve

sudoku = Board()
util = BoardUtils()
solve = Solve()
test = Tests()

while True:

    response = input("1: Generate New Board\t2: Solve existing Board\n")

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

        if test.validity(sudoku):

            print(f"\n\nSolution:\n\n{sudoku.board}")
            print(f"\nBlocks{util.print_blocks(sudoku)}")

        else:

            print("\nNo solutions found")

    if input("exit? y/n") == 'y':
        break