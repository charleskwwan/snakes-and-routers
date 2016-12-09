import pygame
from Constants import *

class Food(object):
    FOOD_COLOR = 255, 0, 0

    def __init__(self, cell, color=FOOD_COLOR):
        self.col = cell[0]
        self.row = cell[1]
        self.x =  cell[0] * CELL_LEN # actual pixel positions
        self.y = cell[1] * CELL_LEN
        self.color = color

    # draw food on screen
    def blit(self, screen):
        rect = pygame.Rect(self.x, self.y, CELL_LEN, CELL_LEN)
        pygame.draw.rect(screen, self.color, rect)
