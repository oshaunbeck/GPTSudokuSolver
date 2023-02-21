import numpy as np

from .cell import Cell
from typing import List


class Board():
    def __init__(self, values=None):
        self.board_size = (9, 9)
        self.block_size = (3, 3)

        if values is None:
            # Initialize a board with completely empty cells
            self.initial_cells = [[Cell(0) for i in range(9)] for i in range(9)]
        else:
            # Initialize a board with the provided values
            self.initial_cells = [[Cell(values[i][j]) for j in range(9)] for i in range(9)]
        
        self.board = np.asarray(self.initial_cells)

        # Define row, column, and box lists
        self.row_list = [set([self.board[i][j] for j in range(9)]) for i in range(9)]
        self.col_list = [set([self.board[i][j] for i in range(9)]) for j in range(9)]
        self.box_list = [set([self.board[i][j] for i in range(box_i * 3, (box_i + 1) * 3)
                                          for j in range(box_j * 3, (box_j + 1) * 3)])
                                          for box_i in range(3) for box_j in range(3)]
        
        self.unit_list = [self.board[i, :] for i in range(9)] + [self.board[:, j] for j in range(9)]
        self.unit_list += [self.board[i:i+3, j:j+3].flatten() for i in range(0, 9, 3) for j in range(0, 9, 3)]

        # Update the sets with the initial values in the board
        for i in range(9):
            for j in range(9):
                if self.board[i][j].num != 0:
                    self.row_list[i].discard(self.board[i][j])
                    self.col_list[j].discard(self.board[i][j])
                    self.box_list[(i // 3) * 3 + (j // 3)].discard(self.board[i][j])
    
    @staticmethod
    def from_list(lst):
        return Board(lst)