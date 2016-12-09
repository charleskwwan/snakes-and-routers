import random
from copy import deepcopy
from Messaging import *
from Board import *
from Food import *
from Snake import *

class CollisionFound(Exception):
    pass

class DeadSnake(Exception):
    pass

class GameState(object):
    MAX_FOODS = 10

    def __init__(self, src=None, board=None, id_snakes=None, foods=None):
        if src:
            self.decode(src)
        else:
            self.board = deepcopy(board) if board else Board()
            self.id_snakes = id_snakes.copy() if id_snakes else {}
            self.foods = foods.copy() if foods else {}

    # for network export
    def encode(self):
        board = self.board.encode()
        snakes = {sid: s.encode() for sid, s in self.id_snakes.items()}
        return {"board": board, "snakes": snakes, "foods": self.foods.keys()}

    def decode(self, encoded):
        self.board = Board(src=encoded["board"])
        self.id_snakes = {sid: Snake(src=s) for sid, s in encoded["snakes"].items()}
        self.foods = {fcell: Food(fcell) for fcell in encoded["foods"]}

    ##### food methods
    def makeFoodCell(self):
        empties = self.board.getEmpties()
        if len(self.foods) < GameState.MAX_FOODS:
            fcell = empties[random.randint(0, len(empties) - 1)]
            return fcell
        else: # no empties OR max number already reached
            return None

    def addFood(self, fcell):
        self.foods[fcell] = Food(fcell)
        self.board.at(fcell, Board.FOOD_CELL)

    def removeFood(self, fcell, replace=None):
        del self.foods[fcell]
        if replace:
            self.board.at(fcell, replace)

    ##### snake methods
    def getSnakes(self):
        return self.id_snakes.values()

    def addSnake(self, snake_id, name, cell, direction):
        # add record of snake
        new_snake = Snake(cell=cell, direction=direction, name=name)
        self.id_snakes[snake_id] = new_snake
        # add snake to board
        if new_snake.isVulnerable():
            for c in new_snake.getCells():
                self.board.at(c, snake_id)

    def removeSnake(self, snake_id):
        if snake_id not in self.id_snakes:
            return
        snake = self.id_snakes[snake_id]
        # remove all cells on board, then delete
        for c in snake.getCells():
            self.board.at(c, Board.EMPTY_CELL)
        del self.id_snakes[snake_id]

    def respawnSnake(self, snake_id, cell, direction):
        self.id_snakes[snake_id].respawn(cell, direction)

    def moveSnake(self, snake_id):
        snake = self.id_snakes[snake_id]
        if snake.isDead(): # dont move if dead
            return

        initial_last = lcol, lrow = snake.getLast()
        snake.move()
        if not snake.isVulnerable(): # if not vulnerable, dont add to board yet
            return

        # check for collision, no need to move all snakes since timestamped
        hcell = snake.getHead()
        if self.board.isCellEmpty(hcell):
            pass
        elif self.board.at(hcell) == Board.FOOD_CELL:
            snake.grow()
            self.removeFood(hcell)
        else: # a snake's id found
            snake.die()
            for c in snake.getCells()[1:] + [initial_last]:
                self.board.at(c, Board.EMPTY_CELL) # clear out original cells
            raise DeadSnake(snake_id, snake.getName())
        
        # shift snake's position on board
        for c in snake.getCells():
            self.board.at(c, snake_id)
        if initial_last != snake.getLast(): # not true in case of grow
            self.board.at(initial_last, Board.EMPTY_CELL)

    def rotateSnake(self, snake_id, pressed):
        snake = self.id_snakes[snake_id]
        if snake.isDead(): # dont rotate if dead
            return
        self.id_snakes[snake_id].rotate(pressed)

    ##### general
    def hasSnake(self, snake_id):
        return snake_id in self.id_snakes

    # gets a random position on the board
    # deterministic - gets a random position from the board
    # if none work, then none is returned
    def getEmptyInitialPosition(self):
        # get list of all empty spaces in board, rare operation worth doing
        empties = self.board.getEmpties()
        if len(empties) == 0: # no empty positions, board completely filled
            return None

        # loop: randomly select a space and a direction; if empty return it
        random.seed()
        directions = [(+1, 0), (-1, 0), (0, +1), (0, -1)]

        while len(empties) > 0:
            random.shuffle(directions)
            hidx = random.randint(0, len(empties) - 1)
            hcell = empties[hidx]
            
            for d in directions:
                # create cells of new snake
                cells = Snake.constructBodyCells(hcell, d)
                cells.insert(0, hcell)

                # test cells for collisions
                try:
                    for c in cells:
                        if c not in empties:
                            raise CollisionFound
                except CollisionFound:
                    continue # try next direction

                # if no collision exception, all cells are empty
                return hcell, d

            empties.pop(hidx) # no valid directions found, invalid cell

        return None # all empties tried, none valid

    def blit(self, screen):
        for food in self.foods.values():
            food.blit(screen)
        for snake in self.id_snakes.values():
            if not snake.isDead():
                snake.blit(screen)
