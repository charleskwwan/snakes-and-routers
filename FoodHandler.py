import pygame
import random
from food import *
from constants import *

class FoodHandler(object):
    def __init__(self, maxfoods = 10):
        self.maxFoods = maxfoods
        self.foodTime = pygame.time.get_ticks()
        self.foods = []
        
    def createFood(self, snakes, screen):
        if len(self.foods) > self.maxFoods:
            return
        isValidLoc = False
        while not isValidLoc:
            # Picking random coordinates 
            food_x = random.randint(0, SCR_WIDTH / CELL_LEN)
            food_y = random.randint(0, SCR_HEIGHT / CELL_LEN)

            # Making sure there are no collisions with ingame objs
            for snake in snakes:
                """
                if collision:
                    pick again!11!!!!1

                """
            for food in self.foods:
                if food.grid_x == food_x or food.grid_y == food_y:
                    continue
            isValidLoc = True
        self.foods.append(Food((food_x, food_y)))


         
    def deleteFood(self, food):
        self.foods.remove(food)
         
    def eatFood(self, snakes): 
        #If collision with food, remove food, snakes grows
        """
        for snake in snakes:
            for food in self.foods:
                if collision:
                    deleteFood(food)
                    snake.increaseLength()
        """

    def blit(self, screen):
        for food in self.foods:
            food.blit(screen)
    def update(self, snakes, screen):
        """
        print self.foodTime
        time = pygame.time.get_ticks()
        print time
        if time - self.foodTime > 5000:     
            self.createFood(snakes, screen)
            self.foodTime = time
        """
        self.createFood(snakes, screen)
        self.eatFood(snakes)
        self.blit(screen)
 
     
