import pygame
from Food import *
from FoodHandler import *
from Snake import *
from constants import *
from Host import Host
from Player import Player
from button import *
import threading


# Lowest possible user event ID (generally 24)
USEREVENT = pygame.USEREVENT
CREATE_FOOD = USEREVENT + 1
HOST_MOVE_SNAKE = USEREVENT + 2
CLIENT_MOVE_SNAKE = USEREVENT + 3

class EndGame(Exception):
    pass

class GameWindow(object):
    def __init__(self):
        pygame.init()
        self.time = pygame.time.Clock()
        self.fps = FPS
        self.size = self.width, self.height = SCR_WIDTH, SCR_HEIGHT
        self.screen = pygame.display.set_mode(self.size)
        self.state = "Menu"        

    def runHostClient(self):
        host = Host("localhost", 9999) # actual, should be decided already
        host.running = True
        t = threading.Thread(target=self.runHost, args=[host,])
        t.start() # start runhost thread
        self.runClient(host)

    def runHost(self, host):
        # set timers
        pygame.time.set_timer(CREATE_FOOD, FOOD_TIMER)
        pygame.time.set_timer(HOST_MOVE_SNAKE, SNAKE_TIMER)

        while host.running:
            host.updateConnection()

            # handle events
            for event in pygame.event.get([CREATE_FOOD, HOST_MOVE_SNAKE]):
                if event.type == CREATE_FOOD:
                    host.updateFood()
                elif event.type == HOST_MOVE_SNAKE:
                    host.updateSnakes()

    def runClient(self, host=None):
        player = Player()
        player.joinGame(("localhost", 9999)) # temp
        # set timers
        pygame.time.set_timer(CLIENT_MOVE_SNAKE, SNAKE_TIMER)

        while True:
            self.time.tick(self.fps)
            self.screen.fill(SCR_BG_COLOR)
            player.updateConnection()

            # handle input
            for event in pygame.event.get([pygame.KEYDOWN]):
                if event.key != pygame.K_UP and event.key != pygame.K_DOWN and \
                   event.key != pygame.K_LEFT and event.key != pygame.K_RIGHT:
                    continue
                else:
                    player.sendInput(event.key)

            try:
                # move snake basd on user input
                for event in pygame.event.get([pygame.QUIT, CLIENT_MOVE_SNAKE]):
                    if event.type == pygame.QUIT:
                        if host:
                            host.running = False
                        raise EndGame
                    elif event.type == CLIENT_MOVE_SNAKE:
                        player.updateSnakes()
            except EndGame:
                break

            # work on display
            player.blit(self.screen)
            pygame.display.update()

        exit()


    def runMenu(self):
        while self.state == "Menu":
            self.time.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            self.screen.fill(SCR_BG_COLOR)
            #text = pygame.font.SysFont('Times New Roman', 40).render("Snakes and routers", True, 
            #                        (0, 0, 0))
            #self.screen.blit(text, (250, 250))
            button("Host!", 250 - 50, 250 - 50, 100, 50, (0, 120, 0), (0, 255, 0), self.screen, self.runHostClient)
            button("Connect!", 250 - 50, 250 + 50, 100, 50, (0, 120, 0), (0, 255, 0), self.screen, self.runClient)

            pygame.display.update()
             
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            if self.state == "Game":
                self.runGame()
            elif self.state == "Menu":
                self.runMenu()


def main():
    app = GameWindow()
    app.run()

if __name__ == '__main__':
    main()
