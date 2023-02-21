class Cell():

    def __init__(self, num: int, block: int = 0, position: tuple = (0, 0)):

        self.num = num

        self.position = position

        self.block = block

        self.row = self.position[0]

        self.col = self.position[1]

        self.blacklist = set()

        self.candidates = set(range(1, 10)) if self.num == 0 else set()

    def has_candidate(self, digit):
        return digit in self.candidates

    def __repr__(self):

        return f"{self.num}"

    def __eq__(self, other):
        return self.num == other
    
    def __hash__(self):
        return hash((self.row, self.col))

    def __gt__(self, other):
        return self.num > other

    def info(self):

        return f"""
        
        Num:   {self.num}
        Position: {self.position}
        Row:    {self.row}
        Column: {self.col}
        Block:  {self.block}
        Blacklist:  {self.blacklist}

        """

