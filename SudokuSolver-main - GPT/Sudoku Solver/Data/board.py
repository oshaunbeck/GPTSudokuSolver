import numpy as np

from .cell import Cell


class Board():
    def __init__(self):

        self.board_size = (9, 9)
        self.block_size = (3, 3)

        # Initialize a board with completely empty cells
        self.initial_cells = [[Cell(0) for i in range(9)] for i in range(9)]

        self.board = np.asarray(self.initial_cells)


        # Define row, column, and box lists
        self.row_list = [set(range(1, 10)) for i in range(9)]
        self.col_list = [set(range(1, 10)) for i in range(9)]
        self.box_list = [set(range(1, 10)) for i in range(9)]

        # Update the sets with the initial values in the board
        for i in range(9):
            for j in range(9):
                if self.board[i][j].num != 0:
                    self.row_list[i].discard(self.board[i][j].num)
                    self.col_list[j].discard(self.board[i][j].num)
                    self.box_list[(i // 3) * 3 + (j // 3)].discard(self.board[i][j].num)
    
    def display_board(self):
        # for row in self.board:
        #     print("+---+---+---+---+---+---+---+---+---+")
        #     row_str = "|"
        #     for cell in row:
        #         if cell.num == 0:
        #             row_str += "   |"
        #         else:
        #             row_str += f" {cell.num} |"
        #     print(row_str)
        # print("+---+---+---+---+---+---+---+---+---+")
        print(self.board)