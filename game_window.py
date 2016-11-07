import pygame
from snake import *
from constants import *

class GameWindow(object):
    def __init__(self):
        pygame.init()         

        self.time = pygame.time.Clock()
        self.fps = FPS
        self.size = self.width, self.height = SCR_WIDTH, SCR_HEIGHT
        self.screen = pygame.display.set_mode(self.size)

    def runGame(self):
        # init player's snake and move-snake timer
        snake = Snake((10, 10), SNAKE_LENGTH, SNAKE_HD_COLOR, SNAKE_BD_COLOR, (0, +1))
        pygame.time.set_timer(MOVE_SNAKE, SNAKE_TIMER)

        while True:
            self.time.tick(self.fps)
            self.screen.fill(SCR_BG_COLOR)
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
