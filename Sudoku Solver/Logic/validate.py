import numpy as np

from Data import Board
from .solve import Solve

class Validate():
    def __init__(self, board: Board):
        self.solve = Solve()

    def is_solved(self, board: Board):

        # If there is a 0 in the board then we can save calculation

        # Check if all cells have a non-zero number
        if np.count_nonzero(board.board) < 81:
            return False
        
        # If there are no zeros then check validity of solution

        for row in board.board:
            for col in range(9):

                # Fill the cells blacklist

                self.solve.fill_blacklist(row[col], board)

                # If this blacklist isnt exactly 9 then it contains a duplicate number

                if len(row[col].blacklist) != 9:
                    return False
                
        return True