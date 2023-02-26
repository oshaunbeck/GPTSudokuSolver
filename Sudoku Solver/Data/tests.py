import numpy as np

from .board import Board
from .cell import Cell

class Tests():
    def __init__(self):

        self.TEST_BOARD_1 = np.array([
[3, 0, 6, 5, 0, 8, 4, 0, 0],
[5, 2, 0, 0, 0, 0, 0, 0, 0],
[0, 8, 7, 0, 0, 0, 0, 3, 1],
[0, 0, 3, 0, 1, 0, 0, 8, 0],
[9, 0, 0, 8, 6, 3, 0, 0, 5],
[0, 5, 0, 0, 9, 0, 6, 0, 0], 
[1, 3, 0, 0, 0, 0, 2, 5, 0],
[0, 0, 0, 0, 0, 0, 0, 7, 4],
[0, 0, 5, 2, 0, 6, 3, 0, 0]
])
        
        #self.TEST_BOARD_2 = np.array()
        self.TEST_SOLUTION_1 = np.array([
[3, 1, 6, 5, 7, 8, 4, 9, 2],
[5, 2, 9, 1, 3, 4, 7, 6, 8],
[4, 8, 7, 6, 2, 9, 5, 3, 1],
[2, 6, 3, 4, 1, 5, 9, 8, 7],
[9, 7, 4, 8, 6, 3, 1, 2, 5],
[8, 5, 1, 7, 9, 2, 6, 4, 3],
[1, 3, 8, 9, 4, 7, 2, 5, 6],
[6, 9, 2, 3, 5, 1, 8, 7, 4],
[7, 4, 5, 2, 8, 6, 3, 1, 9]])

    def load_test_board(self, board: Board):

        board.board = self.TEST_BOARD_1

    def run_test(self, board: Board):

        if np.array_equal(board.board, self.TEST_SOLUTION_1):   return True
            
        else:    return False

    def validity(self, board: Board):

        # If there is a 0 in the board then we can save calculation

        if 0 in board.board:
            return False
        
        # If there are no zeros then check validity of solution

        for row in board.board:
            for col in range(9):

                # Fill the cells blacklist

                self.fill_blacklist(row[col], board)

                # If this blacklist isnt exactly 9 then it contains a duplicate number

                if len(row[col].blacklist) != 9:
                    return False
                
        return True




                

