import json
import jsonpickle
from Snake import Snake
from constants import *

class GameState(object):
    def __init__(self, json="", id_snakes={}, foods=[], dim=(500, 500)):
        if json:
            gamestate = jsonpickle.decode(json)
            id_snakes = gamestate.id_snakes
            foods = gamestate.foods
            dim = gamestate.dim
        self.id_snakes = id_snakes
        self.foods = foods
        self.dim = dim

    def stringify(self): 
        return jsonpickle.encode(self)

    def addSnake(self, snake_id, cell, direction):
        self.id_snakes[snake_id] = Snake(cell=cell, direction=direction)
