import numpy as np
from itertools import combinations
import os
from random import randint

from Data import Board, BoardUtils, Cell, Tests

class Solve:
    def __init__(self):
        self.digits = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    def hidden_single(self, board: Board) -> bool:
        """
        Implements the Hidden Single technique: when only one candidate for a digit appears in a unit, that candidate
        must be placed in that cell. A unit can be a row, column, or box.
        """

        changed = False
        for unit in board.row_list + board.col_list + board.box_list:
            for digit in self.digits:
                candidates = [cell for cell in unit if cell.has_candidate(digit)]
                if len(candidates) == 1:
                    cell = candidates[0]
                    if cell.num == 0:
                        cell.num = digit
                        changed = True
        return changed
    
    def unique_candidate(self, board: Board) -> bool:
        """
        Implements the Unique Candidate technique: when a digit can only be placed in one cell in a unit, that digit
        must be placed in that cell. A unit can be a row, column, or box.
        """


        changed = False
        for unit in board.row_list + board.col_list + board.box_list:
            for digit in self.digits:
                digit_places = [cell for cell in unit if cell.has_candidate(digit)]
                if len(digit_places) == 1:
                    cell = digit_places[0]
                    if cell.num == 0:
                        cell.num = digit
                        changed = True
        return changed
    def naked_single(self, board: Board) -> bool:
        """
        Implements the Naked Single technique: when a cell has only one candidate, that candidate must be placed in
        that cell.
        """
        changed = False
        for row in board:
            for cell in row:
                if cell.num == 0 and len(cell.candidates()) == 1:
                    cell.num = list(cell.candidates())[0]
                    changed = True
        return changed
    
    def hidden_pair(self, board: Board) -> bool:
        """
        Implements the Hidden Pair technique: if two cells in a unit have the same pair of candidates, then no other
        cells in that unit can have those candidates.
        """
        changed = False
        for unit in board.row_list + board.col_list + board.box_list:
            # Find pairs of cells that have the same two candidates
            pairs = [pair for pair in combinations(unit, 2) if pair[0].candidates() == pair[1].candidates() == 2]
            # If there are at least two pairs, try to remove the candidates from the other cells in the unit
            if len(pairs) > 1:
                for other_cell in unit:
                    if other_cell not in pairs:
                        old_candidates = other_cell.candidates()
                        new_candidates = old_candidates - set.union(*[set(cell.candidates()) for cell in pairs])  
                        if new_candidates != old_candidates:
                            other_cell.set_candidates(new_candidates)
                            changed = True
        return changed
    
    def hidden_triple(self, board: np.ndarray) -> bool:
        """
        Implements the Hidden Triple technique: if three cells in a unit have the same three candidates, then no other
        cells in that unit can have those candidates.
        """
        changed = False
        for unit in board.row_list + board.col_list + board.box_list:
            # Find triples of cells that have the same three candidates
            triples = [triple for triple in combinations(unit, 3) if triple[0].candidates() == triple[1].candidates() == triple[2].candidates() == 3]
            # If there are at least three triples, try to remove the candidates from the other cells in the unit
            if len(triples) > 2:
                for other_cell in unit:
                    if other_cell not in triples:
                        old_candidates = other_cell.candidates()
                        new_candidates = old_candidates - set.union(*[set(cell.candidates()) for cell in triples])  
                        if new_candidates != old_candidates:
                            other_cell.set_candidates(new_candidates)
                            changed = True
        return changed
    
    def hidden_quad(self, board: np.ndarray) -> bool:
        """
        Implements the Hidden Quad technique: if four cells in a unit have the same four candidates, then no other
        cells in that unit can have those candidates.
        """
        changed = False
        for unit in board.row_list + board.col_list + board.box_list:
            # Find quads of cells that have the same four candidates
            quads = [quad for quad in combinations(unit, 4) if quad[0].candidates() == quad[1].candidates() == quad[2].candidates() == quad[3].candidates() == 4]
            # If there are at least four quads, try to remove the candidates from the other cells in the unit
            if len(quads) > 3:
                for other_cell in unit:
                    if other_cell not in quads:
                        old_candidates = other_cell.candidates()
                        new_candidates = old_candidates - set.union(*[set(cell.candidates()) for cell in quads])  
                        if new_candidates != old_candidates:
                            other_cell.set_candidates(new_candidates)
                            changed = True
        return changed

    def num_allowed(self, board: Board, row: int, col: int, num: int) -> bool:
        """
        Determines if a given digit can be placed in a given cell without violating any of the rules of Sudoku.
        """
        # Check if the digit is in the same row or column
        if num in board.board[row, :]:
            return False
        if num in board.board[:, col]:
            return False

        # Check if the digit is in the same 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        if num in board.board[box_row:box_row+3, box_col:box_col+3]:
            return False

        return True
    
    def is_solved(self, board):
        # Check if all cells have a non-zero number
        if np.count_nonzero(board) < 81:
            return False

        # Check each row for duplicates
        for row in range(9):
            if len(set(board[row, :])) < 9:
                return False

        # Check each column for duplicates
        for col in range(9):
            if len(set(board[:, col])) < 9:
                return False

        # Check each box for duplicates
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = board[box_row:box_row+3, box_col:box_col+3].flatten()
                if len(set(box)) < 9:
                    return False

        return True

    def fill_board(self, row, col, board: Board):

        print(type(board))
        # Try the different techniques and continue until no changes can be made
        while self.unique_candidate(board.board) or self.hidden_single(board.board) or self.naked_single(board.board) or self.hidden_pair(board.board) or self.hidden_triple(board.board) or self.hidden_quad(board.board):
            pass

        # If the puzzle is solved, return True
        if self.is_solved(board.board):
            return True

        # Otherwise, try each number in the current cell
        for num in range(1, 10):
            if self.num_allowed(row, col, num):
                board.board[row, col].num = num
                new_row, new_col = self.get_next_cell(row, col)
                if self.fill_board(new_row, new_col, board):
                    return True

        # If no number works, reset the current cell and backtrack
        board.board[row, col].num = 0
        return False















    # def num_allowed(self, board: Board, row, col, num):

    #     for i in range(9):

    #         if board.board[row][i] == num:
    #             return False 
        
    #     for i in range(9):

    #         if board.board[i][col] == num:

    #             return False
            
    #     blockID = board.board[row][col].block

    #     blocks = board.blocks[blockID]

    #     for block in blocks:

    #         for val in block:

    #             if num == val:
    #                 return False
            
    #     return True

    # def fill_board(self, row, col, board: Board):

    #     if row == 8 and col == 9:
    #         return True
        
    #     if col == 9:
    #         row += 1
    #         col = 0

    #     if board.board[row][col] > 0:
    #         return self.fill_board(row, col+1, board)
        
    #     for i in range(1, 10, 1):

    #         if self.num_allowed(board, row, col, i):

    #             board.board[row][col].num = i

    #             if self.fill_board(row, col + 1, board):
    #                 return True

    #         board.board[row][col].num = 0

    #     return False
        
    # def generate_solvable(self):

        board = Board()
        test = Tests()
        util = BoardUtils()
        util.update(board)

        print(board.board)

        board.board[randint(0, 8)][randint(0, 8)].num = randint(1, 9)

        return board

        # for i in range(81):

        #     row = i%9
        #     col = randint(0, 8)

        #     number = randint(1, 9)

        #     if self.num_allowed(board, row, col, number):
            
        #         board.board[i%9][col].num = number

        #     else:
        #         continue

        # if self.fill_board(0, 0, board):

        #     return board
        
        # else:
        #     return self.generate_solvable()
        

                    

    

        
        


