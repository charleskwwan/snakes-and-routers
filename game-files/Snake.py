import pygame
import math
from Constants import *

# snakes are made of multiple blocks. this is one.
class SnakePart(object):
    # snakepart constants
    COLOR = 0, 255, 0

    def __init__(self, cell, color=COLOR):
        self.col = cell[0]
        self.row = cell[1]
        self.x = cell[0] * CELL_LEN
        self.y = cell[1] * CELL_LEN
        self.color = color

    def getCell(self):
        return self.col, self.row

    # function to draw on screen
    def blit(self, screen, alpha=255):
        part = pygame.Surface((CELL_LEN, CELL_LEN))
        part.set_alpha(alpha)
        part.fill(self.color)
        screen.blit(part, (self.x, self.y))

class Snake(object):
    # snake constants
    LEN = 10
    HD_COLOR = 0, 150, 0
    BD_COLOR = 0, 255, 0
    VULN_MULTIPLIER = 5
    DEATH_PRICE = 10
    NAME_FONT_SIZE = 20
    NAME_FONT_COLOR = 0, 0, 0 # black

    def __init__(self, src=None, cell=(0, 0), length=LEN, hd_color=HD_COLOR, 
        bd_color=BD_COLOR, direction=(+1, 0), name=""):
        if src:
            self.decode(src)
        else:
            # positioning
            self.col = cell[0]
            self.row = cell[1]
            self.x = cell[0] * CELL_LEN
            self.y = cell[1] * CELL_LEN

            # head
            self.hd_color = hd_color
            self.head = SnakePart(cell, hd_color)

            # movement
            self.dir_col = direction[0]
            self.dir_row = direction[1]

            # body
            self.init_length = length
            self.length = length
            bcells = Snake.constructBodyCells(cell, direction, length - 1)
            self.bd_color = bd_color
            self.body = [SnakePart(c, bd_color) for c in bcells]

            # overall
            self.score = 0
            self.is_dead = False
            self.vulnerable_in = length * Snake.VULN_MULTIPLIER
            self.next_rotate = None
            self.name = name

    def encode(self):
        return {"cells": self.getCells(), "hd_color": self.hd_color, 
                "bd_color": self.bd_color, "score": self.score,
                "init_len": self.init_length, "is_dead": self.is_dead,
                "direction": (self.dir_col, self.dir_row),
                "vulnerable_in": self.vulnerable_in,
                "next_rotate": self.next_rotate, "name": self.name}

    def decode(self, encoded):
        cells = encoded["cells"]
        hcell = cells[0]
        # positioning
        self.col = hcell[0]
        self.row = hcell[1]
        self.x = hcell[0] * CELL_LEN
        self.y = hcell[0] * CELL_LEN

        # head
        self.hd_color = encoded["hd_color"]
        self.head = SnakePart(hcell, self.hd_color)

        # movement
        self.dir_col = encoded["direction"][0]
        self.dir_row = encoded["direction"][1]

        # body
        self.init_length = encoded["init_len"]
        self.length = len(cells)
        self.bd_color = encoded["bd_color"]
        self.body = [SnakePart(c, self.bd_color) for c in cells[1:]]

        # overall
        self.score = encoded["score"]
        self.is_dead = encoded["is_dead"]
        self.vulnerable_in = encoded["vulnerable_in"]
        self.next_rotate = encoded["next_rotate"]
        self.name = encoded["name"]

    # constructs the cells required for the body
    @classmethod
    def constructBodyCells(self, hcell, direction, length=LEN - 1):
        cells = []
        dir_col, dir_row = direction
        col = hcell[0]
        row = hcell[1]
        for i in range(0, length):
            col = (col - dir_col) % (SCR_WID / CELL_LEN)
            row = (row - dir_row) % (SCR_HGT / CELL_LEN)
            cells.append((col, row))
        return cells

    def getHead(self): # get the cell occupied by the snake's head
        return self.col, self.row

    def getCells(self): # get the cells occupied by the snake
        cells = [(self.col, self.row)] # head
        for t in self.body:
            cells.append(t.getCell())
        return cells

    def getLast(self): # gets the last cell occupied by the snake
        return self.body[len(self.body) - 1].getCell()

    def getScore(self):
        return self.score

    def getName(self):
        return self.name

    def isVulnerable(self):
        return self.vulnerable_in <= 0

    def grow(self): # next move will take care of growing body
        self.length += 1
        self.score += 1

    def isDead(self):
        return self.is_dead

    def die(self):
        self.score = max(self.score - Snake.DEATH_PRICE, 0)
        self.is_dead = True

    def respawn(self, cell, direction, length=None):
        # positioning
        self.col = cell[0]
        self.row = cell[1]
        self.x = cell[0] * CELL_LEN
        self.y = cell[1] * CELL_LEN

        # head
        self.head = SnakePart(cell, self.hd_color)

        # movement
        self.dir_col = direction[0]
        self.dir_row = direction[1]

        # body
        if length:
            self.init_length = length
        self.length = self.init_length
        bcells = Snake.constructBodyCells(cell, direction, self.length - 1)
        self.body = [SnakePart(c, self.bd_color) for c in bcells]

        # overall
        self.is_dead = False
        self.vulnerable_in = self.length * 5

    # change direction of snake based on input
    # queue up next rotate to avoid rotate badly before next move
    def rotate(self, key_pressed):
        if (key_pressed == pygame.K_UP and self.dir_row != +1) or \
           (key_pressed == pygame.K_DOWN and self.dir_row != -1) or \
           (key_pressed == pygame.K_LEFT and self.dir_col != +1) or \
           (key_pressed == pygame.K_RIGHT and self.dir_col != -1):
            self.next_rotate = key_pressed

    # move snake forward based on current direction
    def move(self):
        # rotate based on latest rotate stored
        if self.next_rotate:
            if self.next_rotate == pygame.K_UP:
                self.dir_col = 0
                self.dir_row = -1
            elif self.next_rotate == pygame.K_DOWN:
                self.dir_col = 0
                self.dir_row = +1
            elif self.next_rotate == pygame.K_LEFT:
                self.dir_col = -1
                self.dir_row = 0
            elif self.next_rotate == pygame.K_RIGHT:
                self.dir_col = +1
                self.dir_row = 0
            self.next_rotate = None

        # shift body forward by one cell
        self.body.insert(0, SnakePart((self.col, self.row), self.bd_color))
        self.col = (self.col + self.dir_col) % (SCR_WID / CELL_LEN)
        self.row = (self.row + self.dir_row) % (SCR_HGT / CELL_LEN)
        self.x = self.col * CELL_LEN
        self.y = self.row * CELL_LEN
        self.head = SnakePart((self.col, self.row), self.hd_color) # head
        if len(self.body) >= self.length:
            self.body.pop(len(self.body) - 1) # remove last part in body
        if self.vulnerable_in > 0:
            self.vulnerable_in -= 1

    # function to draw on screen
    def blit(self, screen):
        alpha = None
        # setting alpha, normally full 255, but want blinking to indicate coming
        #   out of invulnerability
        if self.vulnerable_in <= 0:
            alpha = 255
        elif self.vulnerable_in <= 21 and \
             math.ceil(self.vulnerable_in / 3.0) % 2 == 0:
            alpha = 150
        else:
            alpha = 50

        for part in self.body:
            part.blit(screen, alpha)
        self.head.blit(screen, alpha)

        # show name next to head
        font = pygame.font.Font(None, Snake.NAME_FONT_SIZE)
        name_text = font.render(self.name, 1, Snake.NAME_FONT_COLOR)
        name_x = self.x + CELL_LEN / 2
        name_y = self.y - int(Snake.NAME_FONT_SIZE * 0.7)   # for gapping
        screen.blit(name_text, (name_x, name_y))

    # for update every frame
    def update(self, screen, key_pressed):
        self.rotate(key_pressed)
        self.move()
        self.blit(screen)
