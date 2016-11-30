import pygame
import socket
import random
import re
from Constants import *
from TrackerHandler import *
from button import *
from Player import *
from Host import *
from GameBar import *
from InputBox import *

IP_REG = r"[0-9][0-9]?[0-9]?.[0-9][0-9]?[0-9]?.[0-9][0-9]?[0-9]?.[0-9][0-9]?[0-9]?"
PORT_REG = r"[0-9][0-9]?[0-9]?[0-9]?[0-9]?"

def getOwnIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 53))
    ip = s.getsockname()[0]
    s.close()
    return ip

class InvalidAddress(Exception):
    pass

class GameWindow(object):
    # GameWindow constants
    FPS = 100
    SCR_BG_COLOR = 255, 255, 255 # white
    # event constants
    FOOD_TIMER = FPS * 25
    CREATE_FOOD = pygame.USEREVENT + 1
    MOVE_TIMER = int(FPS * 0.80)
    MOVE_SNAKE = pygame.USEREVENT + 2
    BLANK_TIMER = MOVE_TIMER / 2
    SEND_BLANK = pygame.USEREVENT + 3

    def __init__(self):
        pygame.init() # pygame initialization

        # time-based details
        self.time = pygame.time.Clock() # keep track of time
        self.fps = GameWindow.FPS

        # screen-based details
        self.size = self.width, self.height = SCR_WID + BAR_WID, SCR_HGT
        self.screen = pygame.display.set_mode(self.size) # pygame create screen

    ##### for menu
    def showMenu(self):
        # fill screen
        self.screen.fill(GameWindow.SCR_BG_COLOR)
        try:
            button("Host!", 250 - 50, 250 - 50, 100, 50, (0, 120, 0), (0, 255, 0), self.screen, self.runHost)
            button("Connect!", 250 - 50, 250 + 50, 100, 50, (0, 120, 0), (0, 255, 0), self.screen, self.runClient)
        except RequestException:
            pass
        pygame.display.update()

    ##### for game
    def getInfo(self, w, h, prompt):
        info = None
        in_box = InputBox(self.width / 2 - w / 2, self.height / 2 - h / 2, w, h, prompt=prompt)
        while not info:
            self.time.tick(self.fps)
            self.screen.fill(GameWindow.SCR_BG_COLOR)
            events = pygame.event.get()

            for e in events:
                if e.type == pygame.QUIT:
                    exit()
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    info = in_box.getInput()

            in_box.update(events)
            in_box.blit(self.screen)
            pygame.display.update()
        return info

    def runHost(self):
        # ip, port = addGame()
        hostport = self.getInfo(self.width, 70, "Host port:")
        if re.match(PORT_REG, hostport):
            hostport = int(hostport)
            try:
                # host = Host(ip, port)
                host = Host(getOwnIP(), hostport)
            except socket.error:
                # removeGame((ip, port))
                return
            self.runClient(host)
        else:
            print "Error: Not a valid host port"

    def runClient(self, host=None):
        # ip, port = host.getID() if host else findGame()
        player = Player()
        # player.joinGame((ip, port))
        hostaddr = None
        try:
            if host:
                hostaddr = host.getID()
            else:
                ip = self.getInfo(self.width, 70, "Host ip:")
                port = self.getInfo(self.width, 70, "Host port:")
                if re.match(IP_REG, ip) and re.match(PORT_REG, port):
                    hostaddr = ip, int(port)
                else:
                    raise InvalidAddress
            player.joinGame(hostaddr)
            self.runGame(player, host)
        except InvalidAddress:
            print "Error: Not a valid host address"

    def runGame(self, player, host=None):
        # wait until player is ready - lag
        while not player.isReady():
            try:
                if host:
                    host.updateConnection()
                player.updateConnection()
            except EndGame: # should bypass isConnected anyway
                break

        # set timers
        pygame.time.set_timer(GameWindow.MOVE_SNAKE, GameWindow.MOVE_TIMER)
        if host:
            pygame.time.set_timer(GameWindow.SEND_BLANK, GameWindow.BLANK_TIMER)
            pygame.time.set_timer(GameWindow.CREATE_FOOD, GameWindow.FOOD_TIMER)

        # create bottom bar
        bar = GameBar(player.exitGame, player.getID(), player.game_state.id_snakes)

        while player.isConnected:
            self.time.tick(self.fps)
            self.screen.fill(GameWindow.SCR_BG_COLOR)

            # check for connection changes
            try:
                if host:
                    host.updateConnection()
                player.updateConnection()
            except EndGame: # in the event of a disconnect
                break

            # handle input
            for event in pygame.event.get([pygame.KEYDOWN]):
                if event.key != pygame.K_UP and event.key != pygame.K_DOWN and \
                   event.key != pygame.K_LEFT and event.key != pygame.K_RIGHT:
                    continue
                elif player.isReady():
                    player.sendInput(pygame.time.get_ticks(), event.key)

            # handle other events like moving
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    player.exitGame(quit=True)
                    if host:
                        host.shutdown()
                        removeGame(host.getID())
                    exit()
                elif event.type == GameWindow.CREATE_FOOD:
                    host.makeFood()
                elif event.type == GameWindow.SEND_BLANK:
                    host.sendBlanks()
                elif player.isReady() and event.type == GameWindow.MOVE_SNAKE:
                    player.sendMove(pygame.time.get_ticks())

            # work on display
            player.updateEvents(self.screen)
            if host:
                host.updateEvents()
            try:
                bar.blit(self.screen)
            except EndGame: # could be triggered by quit button click
                break
            pygame.display.update()

        # cleanup
        if host:
            host.shutdown()
            # removeGame(host.getID())
            pygame.time.set_timer(GameWindow.SEND_BLANK, 0) # disable
            pygame.time.set_timer(GameWindow.CREATE_FOOD, 0)
        pygame.time.set_timer(GameWindow.MOVE_SNAKE, 0)


    ##### for general
    def run(self):
        while True:
            self.time.tick(self.fps) # time moving

            for event in pygame.event.get(): # process events
                if event.type == pygame.QUIT:
                    exit()

            self.showMenu()

##### client
def main():
    app = GameWindow()
    app.run()

# run game if not used for module
if __name__ == "__main__":
    main()
