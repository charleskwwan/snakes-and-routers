import pygame
import random
from Food import *
from constants import *

class FoodHandler(object):
    def __init__(self, maxfoods = 10):
        self.maxFoods = maxfoods

    def createFood(self, snakes, foods, foodcnt):
        if foodcnt > self.maxFoods:
            return None
        isValidLoc = False
        while not isValidLoc:
            # Picking random coordinates 
            food_x = random.randint(0, SCR_WIDTH / CELL_LEN)
            food_y = random.randint(0, SCR_HEIGHT / CELL_LEN)

            # Making sure there are no collisions with ingame objs
            for snake in snakes:
                if snake.collidesWith((food_x, food_y)):
                    continue
            for food in foods:
                if food.grid_x == food_x or food.grid_y == food_y:
                    continue
            isValidLoc = True
        return food_x, food_y     
