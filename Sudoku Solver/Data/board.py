import numpy as np

from .cell import Cell
from typing import List, Optional, Tuple, Set


class Board():
    def __init__(self, values=None):
        self.board_size = (9, 9)
        self.block_size = (3, 3)

        # if values is None:
        #     # Initialize a board with completely empty cells
        #     self.initial_cells = [[Cell(0) for i in range(9)] for i in range(9)]
        # else:
        #     # Initialize a board with the provided values
        #     self.initial_cells = [[Cell(values[i][j]) for j in range(9)] for i in range(9)]
        self.initial_cells = [[Cell(0) for i in range(9)] for i in range(9)]
        self.board = np.asarray(self.initial_cells)

        self.blacklist_update_count = 0
        self.blacklist_zero_count = 0


    def __repr__(self):
        s = ""
        for i in range(self.board.shape[0]):
            if i % 3 == 0 and i != 0:
                s += "------+-------+------\n"
            for j in range(self.board.shape[1]):
                if j % 3 == 0 and j != 0:
                    s += "| "
                if self.board[i, j] == 0:
                    s += ". "
                else:
                    s += str(self.board[i, j]) + " "
            s += "\n"
        return s

    
    def set_num(self, cell: Cell, value: int):

        cell.num = value

        # update blacklists.
        # fill_blacklist will fill all the blacklists of a corresponding cell
        # that is why it must be called each time cell.num is updated.

        self.fill_blacklist(cell)

    def get_potential_hidden_single(self, cells: List[Cell]) -> Optional[Tuple[Cell, int]]:
        
        """
        Finds a potential hidden single by comparing each candidate to candidates provided in a list. 
        This list should have cells with a num property equal to 0 in any row, column or block.

        """
        for cell in cells:

            # Iterate over each candidate in cell

            for candidate in cell.candidates:

                # We have not found any matching candidates yet - it is a unique candidate (We haven't searched yet either)
                unique_candidate = True

                # A second iteration for each cell
                for other_cell in cells:

                    # We want to see if this candidate is in the list of the candidates from other cells

                    # 1: If the candidate is found in the other_cell.candidates, then the candidate is not unique.
                    # We can break to the next candidate

                    # 2: If it is not found, the candidate is unique and we must 
                    # return the candidate and the cell it belongs to.


                    if other_cell is not cell and candidate in other_cell.candidates:
                        unique_candidate = False
                        break

                if unique_candidate:
                    return cell, candidate
                
        return None

    def is_unique_candidate(self, cells: List[Cell], potential_cell: Cell, candidate: int) -> Optional[Tuple[Cell, int]]:
        """
        Once a cell with a potential unique candidate is found, it must be compared to candidates in its remaining row, column and/or block.

        cells: List[Cell] Should NOT contain the potential_cell in it.
        
        This method compares a potential unique candidate to see if it is found in other candidate lists. 
        If it is unique in this list it will return True, other it will return False.

        """

        unique_candidate = True
        
        for cell in cells:

            if candidate in cell.candidates:

                unique_candidate = False
                break

        return unique_candidate

    def find_empty_cell(self, verbose = True) -> tuple[int, int]:
        """
        Finds the first empty cell in the board and returns its row and column indices.
        """
        for row in self.board:
            for cell in row:
                if cell == 0:
                    if verbose: print(f"Found empty cell! ({cell.row}, {cell.col})\nCandidates{cell.candidates}\n{self}")
                    return cell.row, cell.col
        return None

    # BLACKLIST METHODS:
    # These all have the same idea - iterate through the row, column or block
    # that a cell belongs to, find non-zero values in these iterations and add them
    # to the cells blacklist property.

    # fill_blacklist() wll simply call all row, col and block blacklist methods.

    def row_blacklist(self, cell: Cell):

        # Because row_blacklist is called first from fill_blacklist, we will initialise
        # iter_count

        self.blacklist_update_count = 0
        self.blacklist_zero_count = 0

        # Iterate through the row, find any non-zero values and add them to the blacklist.

        for c in self.board[cell.row, :]:
            if c.num == 0:
                self.blacklist_zero_count += 1

            else:
                cell.blacklist.add(c.num)

                self.blacklist_update_count += 1

    def col_blacklist(self, cell: Cell):

        for c in self.board[:, cell.col]:
            if c.num == 0:
                self.blacklist_zero_count += 1
            else:
                cell.blacklist.add(c.num)

                self.blacklist_update_count += 1

    def block_blacklist(self, cell: Cell):

        block = self.blocks[cell.block]

        for c in block.flatten():

            if c == 0:
                self.blacklist_zero_count += 1

            else:
                cell.blacklist.add(c.num)

                self.blacklist_update_count += 1

    def fill_blacklist(self, cell: Cell):
        """
        Updates blacklists for all cells in the same unit as the one provided in the arg.
        """

        # Iterate through the row, find any non-zero values and add them to all the non-zero value cells blacklists.

        for c in self.board[cell.row, :]:

            if c == 0:  continue

            else:

                for other_cell in self.board[cell.row, :]:

                    if other_cell == 0:

                        other_cell.blacklist.add(c.num)

        # Iterate through the column, find any non-zero values and add them to the blacklist.

        for c in self.board[:, cell.col]:

            if c == 0:  continue

            else:
                for other_cell in self.board[:, cell.col]:

                    if other_cell == 0:

                        other_cell.blacklist.add(c.num)

        # Iterate through block

        block = self.blocks[cell.block]

        for c in block.flatten():

            if c == 0:  continue

            else:
                for other_cell in block.flatten():

                    if other_cell == 0:

                        other_cell.blacklist.add(c.num)