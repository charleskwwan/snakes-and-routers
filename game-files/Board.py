from Constants import *

# board (2D array):
#   - snake occupied has snake's id
#   - blank: 'B'
#   - food: 'F'

class Board(object):
    EMPTY_CELL = 'B'
    FOOD_CELL = 'F'

    def __init__(self, src=None, dim=(SCR_WID / CELL_LEN, SCR_HGT / CELL_LEN)):
        if src:
            self.decode(src)
        else:
            self.wid = dim[0]
            self.hgt = dim[1]
            self.board = [['B' for row in range(self.hgt)] \
                          for col in range(self.wid)]

    def encode(self):
        compressed = {} # only capture nonempty cells, save space
        for col in range(self.wid):
            for row in range(self.hgt):
                contents = self.board[col][row]
                if contents != Board.EMPTY_CELL:
                    compressed[(col, row)] = contents
        return {"wid": self.wid, "hgt": self.hgt, "board": compressed}

    def decode(self, encoded):
        self.wid = encoded["wid"]
        self.hgt = encoded["hgt"]
        self.board = [['B' for row in range(self.hgt)] \
                          for col in range(self.wid)]
        for (col, row), contents in encoded["board"].items():
            self.board[col][row] = contents

    # if given contents, will modify and return new element
    def at(self, cell, contents=None):
        col, row = cell
        if contents:
            self.board[col][row] = contents
            return contents
        else:
            return self.board[col][row]

    def isCellEmpty(self, cell):
        col, row = cell
        return self.board[col][row] == Board.EMPTY_CELL

    # gets a list of all the empty cells (col, row) that are empty on the board
    def getEmpties(self):
        empties = []
        for col in range(self.wid):
            for row in range(self.hgt):
                if self.board[col][row] == Board.EMPTY_CELL:
                    empties.append((col, row))
        return empties
