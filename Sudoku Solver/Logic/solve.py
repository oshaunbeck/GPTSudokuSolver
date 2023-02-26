import sys, os

from Data import Board

class Solve:
    def __init__(self):

        # How many iterations before the puzzle is solved.
        self.possible_values = {i for i in range(1, 10)}
        self.recursive_counter = 0
        self.hidden_singles_counter = 0
        self.naked_singles_counter = 0
        self.locked_candidates_counter = 0


        self.changed_cells = []
        self.invalid = False

        self.max_recursions = 100_000
    
    @property
    def total_counter(self):
        return self.recursive_counter + self.naked_singles_counter + self.hidden_singles_counter + self.locked_candidates_counter
    def blockPrint(self):
        sys.stdout = open(os.devnull, 'w')

    def enablePrint(self):
        sys.stdout = sys.__stdout__

    def display_counters(self):
        print(f"Number of recursions: {self.recursive_counter}")
        print(f"Number of naked singles: {self.naked_singles_counter}")
        print(f"Number of hidden singles: {self.hidden_singles_counter}")
        print(f"Number of locked candidates found: {self.locked_candidates_counter}")
        print(f"Total iterations: {self.total_counter}")

    def hidden_single(self, board: Board) -> bool:

        """
        Implements the Hidden Single technique: when a row, col or box has a cell with only one candidate, it will be filled.

        We want this method to look through the candidates of each row, column and block. If it finds a value in a candidates set that is unique,
        it changes the value of the cell t
        """

        
        changed = False

        print("going into hidden_single")

        # candidate_list = [cell.candidates for cell in board.board[empty_cell[0] if cell != 0 or cell is empty_cell]]

        next_empty_pos = board.find_empty_cell()
        row = board.board[next_empty_pos[0], :]


        # Check row for hidden single

        candidate_list = []

        for cell in row:

            if cell == 0:
                candidate_list.append(cell)

        if board.get_potential_hidden_single(candidate_list) is not None:

            hidden_single, candidate = board.get_potential_hidden_single(candidate_list)

            print(f"Found potential hidden single: {candidate} {hidden_single.info}")

        else:

            # If there are no potential hidden singles in the row then 
            # it won't matter if we find them in the columns or blocks.
            # lets leave.
            print("No hidden single found")
            return False

        candidate_list = []

        # fill candidate list amongst column and blocks

        # Column first.

        for cell in board.board[:, next_empty_pos[1]]:
            if cell == 0 and cell is not hidden_single:
                candidate_list.append(cell)

        block = board.blocks[hidden_single.block]

        for cell in block.flatten():
            if cell == 0 and cell is not hidden_single:
                candidate_list.append(cell)

        print(f"Comparing to: {[cell.candidates for cell in candidate_list]}")
        # Compare candidates in row and block to see if the potential candidate is truly unique amongst its unit.

        if board.is_unique_candidate(candidate_list, hidden_single, candidate):
            print(f"Hidden Single Found!\n{hidden_single.info}")
            print(f"Assigning value: {candidate}")

            
            board.set_num(hidden_single, candidate)

            if self.check_candidate_lengths(board):
                print("Board found to be invalid!")
                board.set_num(cell, 0)
                
                
            else:
                self.changed_cells.append(hidden_single)
                changed = True

        if not changed:
            print("Candidate was not unique")

        return changed
                    
    def naked_single(self, board: Board) -> bool:

        """
        Implements the Naked Single technique: when a cell has only one candidate, that candidate must be placed in
        that cell.
        """
        changed = False

        print("Checking for naked singles")
        for idx, row in enumerate(board.board):

            if self.invalid or changed:
                    break
            print(f"row: {idx} (naked single)")

            # Go through each row to find an empty cell with only one candidate.
            
            board.fill_blacklist(row[0])

            for cell in row:

                if cell == 0 and len(cell.candidates) == 1:

                    candidate = list(cell.candidates)[0]

                    print(f"Naked Single found: {candidate} {cell.info}")
                    print(f"Setting value {candidate}")

                    board.set_num(cell, candidate)

                    # If we have set the number and an empty cell on the board loses all its candidates then this is the wrong number.
                    
                    # im pretty sure this also means that we should backtrack in the recursion because the value placed by
                    # naked_single will only lead to an invalid board if the board was invalid before naked_single placed the value.
                    # This is because naked_single must find the only potential value for an empty cell and if that leads to an 
                    # invalid board then the board was invalid already.

                    if self.check_candidate_lengths(board):
                        print("Board found to be invalid!")
                        self.invalid = True
                        board.set_num(cell, 0)
                        break
                        
                    else:

                        self.changed_cells.append(cell)
                        changed = True

                        self.naked_singles_counter +=1
                        break

        if not changed: print("No naked Singles found.")
                    
        return changed

    def locked_candidates(self, board: Board) -> bool:
        """
        Implements the Locked Candidates technique: if a candidate value is restricted to one row or column within a
        particular block, then that candidate can be removed from the candidates of all other cells in that row or column.
        """
        changed = False
        
        return changed

    def num_allowed(self, board: Board, row: int, col: int, num: int) -> bool:
        """
        Determines if a given digit can be placed in a given cell without violating any of the rules of Sudoku.
        """

        NOT_ALLOWED_STRING = f"num_allowed did not approve of the number {num} for cell ({row}, {col})"
        # Check if the digit is in the same row or column
        if num in board.board[row, :]:
            print(NOT_ALLOWED_STRING + "(Same number in row)")
            return False
            
        if num in board.board[:, col]:
            print(NOT_ALLOWED_STRING + "(Same number in column)")
            return False

        blockID = board.board[row][col].block

        block = board.blocks[blockID]

        if num in block.flatten():
            print(NOT_ALLOWED_STRING + "(Same number in block)")
            return False
            
        print(f"{num} is allowed for cell ({row}, {col}) (num_allowed)")
        print(board)

        return True
    
    def is_solved(self, board: Board):
        # Check if all cells have a non-zero number
        for row in board.board:
            for cell in row:
                if cell == 0:
                    return False

        # Check each row for duplicates
        for row in range(9):
            if len(set(board.board[row, :])) < 9:
                return False

        # Check each column for duplicates
        for col in range(9):
            if len(set(board.board[:, col])) < 9:
                return False

        # Check each box for duplicates
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = board.board[box_row:box_row+3, box_col:box_col+3].flatten()
                if len(set(box)) < 9:
                    return False

        return True
    def check_candidate_lengths(self, board: Board):

        """
        This method checks every empty cell on the board to see if it has any candidates.
        If it has no candidates then self.invalid = True.
        """
        
        for row in board.board:
            for cell in row:

                # If cell is empty and has no candidates then the board is invalid.
                if cell == 0 and len(cell.candidates) == 0:
                    print(f"Found an invalid board with cell ({cell.row}, {cell.col}): {cell.candidates}")
                    print(board)
                    self.invalid = True
                    return self.invalid
                
        self.invalid = False

        return self.invalid

    def recursive_solve(self, board: Board):

        self.recursive_counter += 1

        for cell in board.board.flatten():
            print(f"Updating blacklist for ({cell.row}, {cell.col})")
            board.fill_blacklist(cell)

        self.enablePrint()
        print(f"\r\nRecursion number: {self.recursive_counter}\nnaked singles: {self.naked_singles_counter}\n\r{board}", end='\r')
        self.blockPrint()
        
        while self.naked_single(board):
            pass

        if self.invalid:
            self.invalid = False
            return False
        
        if board.find_empty_cell(False) is None:
            return True

        row, col = board.find_empty_cell()
        examine_cell = board.board[row][col]
        
        for i in examine_cell.candidates:
            print(f"Trying number {i} cell ({row}, {col})")
            print(board)

            if self.num_allowed(board, row, col, i):
                board.set_num(board.board[row][col], i)

                if self.recursive_solve(board):
                    return True
                    
                print("that search failed. backtracking..")
                board.set_num(board.board[row][col], 0)

                # we set the number and update blacklists but because this is done cell by cell
                # the first cells to be checked have an out of date blacklist so we run this twice before
                # clearing just to ensure blacklists are up to date before backtracking.

                for cell in self.changed_cells:
                    print(f"Setting ({cell.row}, {cell.col}) to 0")
                    board.set_num(cell, 0)

                self.changed_cells.clear()

                if self.invalid:
                    self.invalid = False
                    return False
                
                break

        return False
        

    def solve_board(self, board: Board):

        while True:

            # Attempt to solve recursively
            if self.recursive_solve(board):
                break
        
        self.enablePrint()
        print(f"\n\nSolution:\n\n{board}")

    

        
        


