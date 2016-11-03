#!/etc/python

import pygame



class GameWindow(object):
    def __init__(self):
        pygame.init()

        self.size = width, height = 500, 500
        self.screen = pygame.display.set_mode(self.size)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()


def main():
    app = GameWindow()
    app.run()



if __name__ == '__main__':
    main()
