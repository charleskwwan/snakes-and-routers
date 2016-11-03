#!/etc/python

import pygame
from food import *
from FoodHandler import * 


class GameWindow(object):
    def __init__(self):
        pygame.init()
        self.time = pygame.time.Clock()
        self.fps = 1
        self.size = self.width, self.height = 500, 500
        self.screen = pygame.display.set_mode(self.size)

    def runGame(self):
        foodHandler = FoodHandler()
        while True:
            self.time.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            self.screen.fill((255, 255, 255))
            foodHandler.update([], self.screen)
            pygame.display.update()
    def runMenu(self):
        while True:
            self.time.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            self.screen.fill((255, 255, 255))
            text = pygame.font.SysFont('Times New Roman', 40).render("Snakes and routers", True, 
                                    (0, 0, 0))
            self.screen.blit(text, (250, 250))
            pygame.display.update()
             
        


    def run(self):
        inGame = False
        inMenu = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            if inGame:
                self.runGame()
            elif inMenu:
                self.runMenu()




def main():
    app = GameWindow()
    app.run()



if __name__ == '__main__':
    main()
