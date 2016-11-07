import pygame
from Food import *
from FoodHandler import *
from snake import *
from constants import *

# Lowest possible user event ID (generally 24)
USEREVENT = pygame.USEREVENT
CREATE_FOOD = USEREVENT + 1
MOVE_SNAKE = USEREVENT + 2

class GameWindow(object):
    def __init__(self):
        pygame.init()         

        self.time = pygame.time.Clock()
        self.fps = FPS
        self.size = self.width, self.height = SCR_WIDTH, SCR_HEIGHT
        self.screen = pygame.display.set_mode(self.size)

    def runGame(self):
        #init foodhandler and its timer
        foodHandler = FoodHandler()
        pygame.time.set_timer(CREATE_FOOD, FOOD_TIMER)

        # init player's snake and move-snake timer
        s = Snake((10, 10), SNAKE_LENGTH, SNAKE_HD_COLOR, SNAKE_BD_COLOR, (0, +1))
        pygame.time.set_timer(MOVE_SNAKE, SNAKE_TIMER)
        snakes = [s]

        while True:
            self.time.tick(self.fps)
            self.screen.fill(SCR_BG_COLOR)
 
            for event in pygame.event.get([pygame.QUIT, CREATE_FOOD, MOVE_SNAKE]):
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == CREATE_FOOD:
                    foodHandler.update(snakes, self.screen) 
                elif event.type == MOVE_SNAKE:
                    for snake in snakes:
                        snake.update(self.screen)
                    for snake in snakes: # temp, check if snakes collide
                        if snake.collideSnake(snakes):
                            snakes.remove(snake)
                    foodHandler.eatFood(snakes)

            # blit in case not updated in event for loop
            foodHandler.blit(self.screen)
            for snake in snakes:
                snake.blit(self.screen)

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
        inGame = True
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
