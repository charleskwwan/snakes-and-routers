import pygame
from snake import *

# Lowest possible user event ID (generally 24)
USEREVENT = pygame.USEREVENT
CREATE_FOOD = USEREVENT + 1
MOVE_SNAKE = USEREVENT + 2

class GameWindow(object):
    def __init__(self):
        pygame.init()         

        self.time = pygame.time.Clock()
        self.fps = 60
        self.size = self.width, self.height = 500, 500
        self.screen = pygame.display.set_mode(self.size)

    def runGame(self):
        # init player's snake and move-snake timer
        snake = Snake((10, 10), 5, (0, 0, 255), (0, 255, 0), (0, +1))
        pygame.time.set_timer(MOVE_SNAKE, 200)

        while True:
            self.time.tick(self.fps)
            self.screen.fill((255, 255, 255))
            snake.blit(self.screen)
            for event in pygame.event.get([pygame.QUIT, MOVE_SNAKE]):
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == MOVE_SNAKE:
                    snake.update(self.screen)
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

def main():
    app = GameWindow()
    app.run()

if __name__ == '__main__':
    main()
