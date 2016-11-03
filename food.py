import pygame

class Food(object):
    def __init__(self, pos, color = (255, 0, 0)):
        self.dim = 10
        self.grid_x = pos[0]
        self.grid_y = pos[1]
        self.screen_x = pos[0] * self.dim
        self.screen_y = pos[1] * self.dim
        self.color = color

    def blit(self, screen):
        """ Draws food on screen """
        rect = pygame.Rect(self.screen_x, self.screen_y, self.dim, self.dim)
        pygame.draw.rect(screen, self.color, rect)

