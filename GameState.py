import json
import jsonpickle
from Snake import Snake
from FoodHandler import FoodHandler
from constants import *
import random

class GameState(FoodHandler):
    CELL_LEN = 10

    def __init__(self, keys_pressed={}, json="", id_snakes={}, foods=[], 
        dim=(500, 500)):
        # initialize foodhandler, default maxfoods = 10
        super(GameState, self).__init__()

        if json:
            src = jsonpickle.decode(json, keys=True)
            self.keys_pressed = src.keys_pressed
            self.id_snakes = src.id_snakes
            self.foods = src.foods
            self.dim = src.dim
        else:
            self.keys_pressed = keys_pressed
            self.id_snakes = id_snakes
            self.foods = foods # overrides food handlers if necessary
            self.dim = dim

    def stringify(self): 
        return jsonpickle.encode(self, keys=True)

    def addSnake(self, snake_id, cell, direction):
        self.id_snakes[snake_id] = Snake(cell=cell, direction=direction)

    def removeSnake(self, snake_id):
        del self.id_snakes[snake_id]

    class CollisionException(Exception):
        pass

    def getEmptyInitialPosition(self):
        random.seed()
        is_empty = False
        while not is_empty: # todo: refactor to be deterministic, otherwise could loop forever
            # generate initial cell
            init_col = random.randint(10, (self.dim[0] / CELL_LEN) - 10)
            init_row = random.randint(10, (self.dim[1] / CELL_LEN) - 10)
            dir_col = random.randint(-1, +1)
            dir_row = 0
            if dir_col == 0:
                dir_row = random.choice([-1, 1])

            # check if space for snake is empty
            col = init_col
            row = init_row
            cells = []
            for i in range(Snake.DEFAULT_LEN): # create positions of new snake
                cells.append((col, row))
            try:
                for k in self.id_snakes:
                    for c in cells:
                        if self.id_snakes[k].collidesWith(c):
                            raise GameState.CollisionException
            except GameState.CollisionException:
                continue # reloop if doesnt work

            return (init_col, init_row), (dir_col, dir_row)

    def addKeyPressed(self, snake_id, pressed):
        self.keys_pressed[snake_id] = pressed

    def updateSnakes(self, screen):
        # move snakes

        for k in self.id_snakes:
            pressed = self.keys_pressed[k] if k in self.keys_pressed else None 
            self.id_snakes[k].update(screen, pressed)

        snakes = [self.id_snakes[k] for k in self.id_snakes]
        # check collisions
        for k in self.id_snakes:
            if self.id_snakes[k].collideSnake(snakes):
                self.id_snakes[k] = None # should kill game, for now
            # todo: respawn snake
        # check eat food
        super(GameState, self).eatFood(snakes)

    def updateFood(self, screen):
        snakes = [self.id_snakes[k] for k in self.id_snakes]
        super(GameState, self).update(snakes, screen) # call foodhandler's

    def blit(self, screen):
        super(GameState, self).blit(screen)
        for k in self.id_snakes:
            self.id_snakes[k].blit(screen)
