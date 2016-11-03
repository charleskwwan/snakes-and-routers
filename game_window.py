import pygame
from snake import *

class GameWindow(object):
    def __init__(self):
        pygame.init()

        self.size = width, height = 500, 500
        self.screen = pygame.display.set_mode(self.size)
        self.time = pygame.time.Clock()

    def run(self):
        snake = Snake((10, 10), 3, (255, 0, 0), (0, 255, 0), (0, +1))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            self.screen.fill((255, 255, 255))
            self.time.tick(10)
            snake.update(self.screen, [])
            pygame.display.update()

def main():
    app = GameWindow()
    app.run()

if __name__ == '__main__':
    main()
