class Cell():

    def __init__(self, num: int, block: int = 0, position: tuple = (0, 0)):

        self.num = num

        self.position = position

        self.block = block

        self.row = self.position[0]

        self.col = self.position[1]

        self.possible_values = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        self.blacklist = set()


    @property
    def candidates(self):
        return self.possible_values - self.blacklist
    
    @property
    def info(self):

        return f"""
        Num:   {self.num}
        Position: {self.position}
        Row:    {self.row}
        Column: {self.col}
        Block:  {self.block}
        Blacklist:  {self.blacklist}
        Candidates: {self.candidates}
        """


    def __repr__(self):

        return f"{self.num}"

    def __eq__(self, other):
        return self.num == other
    
    def __hash__(self):
        return hash((self.row, self.col))

    def __gt__(self, other):
        return self.num > other
    



