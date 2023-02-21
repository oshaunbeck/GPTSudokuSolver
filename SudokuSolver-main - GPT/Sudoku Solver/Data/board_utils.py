import numpy as np
from random import randint

from .board import Board
from .cell import Cell

class BoardUtils:
    def __init__(self):

        self.BLOCK_COORDINATES = [
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)], 
            [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)], 
            [(0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)], 
            [(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)], 
            [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)], 
            [(3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)], 
            [(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)], 
            [(6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5)], 
            [(6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)]
            ]

    def generate_block_coordinates(self):
        
        block_list = [[] for i in range(9)]

        for row in range(0, 9):
            for col in range(0, 9):

                if row < 3:
                    if col < 3:
                        self.block_list[0].append((row, col))

                    if 2 < col < 6:
                        self.block_list[1].append((row, col))
                    
                    if 5 < col < 9:
                        self.block_list[2].append((row, col))


                if 2 < row < 6:
                    if col < 3:
                        self.block_list[3].append((row, col))

                    if 2 < col < 6:
                        self.block_list[4].append((row, col))

                    if 5 < col < 9:
                        self.block_list[5].append((row, col))

                if 5 < row < 9:
                    if col < 3:
                        self.block_list[6].append((row, col))

                    if 2 < col < 6:
                        self.block_list[7].append((row, col))

                    if 5 < col < 9:
                        self.block_list[8].append((row, col))

            
        print(block_list)
                
        for idx, block in enumerate(block_list):
            print(f"{idx}: {block}")

    def print_blocks(self, board: Board):

        board.block_array = []

        for block in board.blocks:
            board.block_array.append(block)

        return f"""
        
{board.block_array[0][0]} {board.block_array[1][0]} {board.block_array[2][0]}
{board.block_array[0][1]} {board.block_array[1][1]} {board.block_array[2][1]}
{board.block_array[0][2]} {board.block_array[1][2]} {board.block_array[2][2]}

{board.block_array[3][0]} {board.block_array[4][0]} {board.block_array[5][0]}
{board.block_array[3][1]} {board.block_array[4][1]} {board.block_array[5][1]}
{board.block_array[3][2]} {board.block_array[4][2]} {board.block_array[5][2]}

{board.block_array[6][0]} {board.block_array[7][0]} {board.block_array[8][0]}
{board.block_array[6][1]} {board.block_array[7][1]} {board.block_array[8][1]}
{board.block_array[6][2]} {board.block_array[7][2]} {board.block_array[8][2]}
        
        """

    def update(self, board: Board):
        
        board.rows = [board.board[i, :] for i in range(9)]

        board.columns = [board.board[:, i] for i in range(9)]

        board.blocks = np.zeros((9, 3, 3))

        board.blocks = [board.board[i:i+3, j:j+3] for i in range(0, 9, 3) for j in range(0, 9, 3)]

    def generate_cell(self, num, position):

        # Locate the block number for the cell that is being generated.
        # There must be a better way of doing this than looping over the whole
        # block coordinate list.
        for i in range(9):
            if position in self.BLOCK_COORDINATES[i]:
                block = i
        
        return Cell(num, block, position)

    def str_to_board(self, board: Board):
        
        sudoku_list = []
        print("Input sudoku array (9, 9x1 arrays)")
        for i in range(9):

            row = eval(input())

            sudoku_list.append(row)

        for idx, row in enumerate(board.board):

            for col in range(9):

                position = (idx, col)

                row[col] = self.generate_cell(sudoku_list[idx][col], position)

