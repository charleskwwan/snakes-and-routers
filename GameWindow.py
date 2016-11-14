import pygame
from Food import *
from FoodHandler import *
from Snake import *
from constants import *
from Host import Host
from Client import Client
from button import *


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
        self.state = "Menu"        

    def runGame(self):
        # #init foodhandler and its timer
        self.state = "Game"
        pygame.time.set_timer(CREATE_FOOD, FOOD_TIMER)
        pygame.time.set_timer(MOVE_SNAKE, SNAKE_TIMER)
        self.player = Host("localhost", 9999) # in actual, should be decided already

        while True and not self.player == None:
            self.time.tick(self.fps)
            self.screen.fill(SCR_BG_COLOR)
            self.player.update()
 
            # get keys pressed for everyone
            for event in pygame.event.get([pygame.KEYDOWN]):
                if event.key != pygame.K_UP and event.key != pygame.K_DOWN and \
                   event.key != pygame.K_LEFT and event.key != pygame.K_RIGHT:
                    continue
                elif type(self.player) == Host:
                    self.player.addKeyPressed(self.player.getKey(), event.key)
                    self.player.sendKeypress(self.player.getKey(), event.key)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == CREATE_FOOD:
                    # foodHandler.update(snakes, self.screen)
                    self.player.updateFood(self.screen, host=self.player)
                elif event.type == MOVE_SNAKE:
                    self.player.updateSnakes(self.screen)

            # blit in case not updated in event for loop
            self.player.blit(self.screen)

            pygame.display.update()

    def runClient(self):
        self.player = Client()
        self.player.joinGame(("localhost", 9999))
        pygame.time.set_timer(MOVE_SNAKE, SNAKE_TIMER)
        while True and not self.player == None:
            self.time.tick(self.fps)
            self.screen.fill(SCR_BG_COLOR)
            self.player.update()

            # get input and send to host
            for event in pygame.event.get([pygame.KEYDOWN]):
                if event.key != pygame.K_UP and event.key != pygame.K_DOWN and \
                   event.key != pygame.K_LEFT and event.key != pygame.K_RIGHT:
                    continue
                elif type(self.player) == Client:
                    self.player.sendInput(event.key)

            # move snake based on user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == MOVE_SNAKE:
                    self.player.updateSnakes(self.screen)

            self.player.blit(self.screen)
            pygame.display.update()

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
            button("Host!", 250 - 50, 250 - 50, 100, 50, (0, 120, 0), (0, 255, 0), self.screen, self.runGame)
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
