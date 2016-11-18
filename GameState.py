import json
import jsonpickle
from Snake import Snake
from Food import Food
from constants import *
import random

class CollisionException(Exception):
        pass

class GameState(object):
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

    def getSnakes(self):
        return self.id_snakes.values()

    def getFoods(self):
        return self.foods

    def addSnake(self, snake_id, cell, direction):
        self.id_snakes[snake_id] = Snake(cell=cell, direction=direction)

    def removeSnake(self, snake_id):
        del self.id_snakes[snake_id]

    def addFood(self, food_cell):
        self.foods.append(Food(food_cell))

    def eatFoods(self):
        for snake in self.id_snakes.values():
            for food in self.foods:
                if snake.collidesWith((food.grid_x, food.grid_y)):
                    self.foods.remove(food)
                    snake.increaseLength()

    # gets a random position
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

    def updateSnakes(self):
        # move snakes
        for k in self.id_snakes:
            pressed = self.keys_pressed[k] if k in self.keys_pressed else None
            self.id_snakes[k].move(pressed)

        snakes = [self.id_snakes[k] for k in self.id_snakes]
        # check collisions
        for k in self.id_snakes:
            if self.id_snakes[k].collideSnake(snakes):
                self.id_snakes[k] = None # should kill game, for now
            # todo: respawn snake
        # check eat food
        self.eatFoods()

    def blit(self, screen):
        for f in self.foods:
            f.blit(screen)
        for k in self.id_snakes:
            self.id_snakes[k].blit(screen)
