import PodSixNet
from PodSixNet.Connection import ConnectionListener, connection
from GameState import *
from Messaging import *
from EventQueueHandler import *

class EndGame(Exception):
    pass

class Player(ConnectionListener):
    NOT_CONNECTED = 0
    JOINING = 1
    CONNECTED = 2

    def __init__(self):
        self.reset()
        self.offset = None # for timing

    def reset(self):
        self.status = Player.NOT_CONNECTED
        self.game_state = None
        self.events = None
        self.hostaddr = None
        self.addr = None # own id, query host
        self.lagbuffer = [] # temp hold messages until joined game

    def isConnected(self):
        return self.status != Player.NOT_CONNECTED

    ##### game state functions
    def getID(self):
        return self.addr

    def isReady(self):
        return self.events and self.game_state

    def addPlayer(self, timestamp, player_id, name, cell, direction):
        if not self.game_state.hasSnake(player_id):
            self.events.newQueue(player_id)
        action = name, (cell, direction)
        self.addEvent(player_id, timestamp, Messaging.NEW_SNAKE, action)

    def addMove(self, timestamp, player_id):
        self.addEvent(player_id, timestamp, Messaging.MOVE_SNAKE, None)

    def addRotate(self, timestamp, player_id, pressed):
        self.addEvent(player_id, timestamp, Messaging.INPUT, pressed)

    def addEvent(self, player_id, timestamp, ty, action):
        if not self.events or not self.events.hasQueue(player_id): # not yet joined game
            self.lagbuffer.append((player_id, timestamp, ty, action))
        elif self.lagbuffer:
            self.lagbuffer.sort() # ensure order by timestamp
            for e in self.lagbuffer:
                self.events.addEvent(e[0], e[1], e[2], e[3])
            self.lagbuffer = []
            self.events.addEvent(player_id, timestamp, ty, action)
        else:
            self.events.addEvent(player_id, timestamp, ty, action)

    def blit(self, screen):
        self.game_state.blit(screen)

    def updateEvents(self, screen):
        try:
            if self.events:
                self.events.execute()
        except UnsyncedQueue:
            pass
        except DeadSnake:
            pass
        if self.game_state:
            self.blit(screen) # todo: implement more robust behavior

    ##### network functions
    def Network_blank(self, message):
        timestamp = message[Messaging.TIMESTAMP_TAG]
        player_id = message[Messaging.DATA_TAG]
        self.addEvent(player_id, timestamp, Messaging.BLANK, None)

    def joinGame(self, hostaddr):
        self.hostaddr = hostaddr
        self.Connect(self.hostaddr)
        self.status = Player.JOINING
        self.offset = pygame.time.get_ticks() # store initial time in offset
        message = Messaging.createMessage(Messaging.JOIN_GAME, self.offset, "")
        self.Send(message)

    def exitGame(self, quit=False):
        ticks = pygame.time.get_ticks() + self.offset
        message = Messaging.createMessage(Messaging.REMOVE_SNAKE, ticks, self.addr)
        self.Send(message)
        self.updateConnection() # ensure send
        self.Network_disconnected({"action": "disconnected"}, quit)

    def Network_joinGame(self, message):
        self.status = Player.CONNECTED
        rtt = pygame.time.get_ticks() - self.offset # offset is initial time
        self.offset = message[Messaging.TIMESTAMP_TAG] - rtt
        self.addr = message[Messaging.DATA_TAG]

    def Network_gameState(self, message):
        encoded_game, encoded_qs = message[Messaging.DATA_TAG]
        self.game_state = GameState(src=encoded_game)
        self.events = EventQueueHandler(self.game_state, src=encoded_qs)

    def Network_newSnake(self, message):
        timestamp = message[Messaging.TIMESTAMP_TAG]
        new_snake = message[Messaging.DATA_TAG]
        self.addPlayer(timestamp, new_snake["addr"], new_snake["name"], 
                       new_snake["cell"], new_snake["direction"])

    def Network_removeSnake(self, message):
        timestamp = message[Messaging.TIMESTAMP_TAG]
        snake_id = message[Messaging.DATA_TAG]
        self.addEvent(snake_id, timestamp, Messaging.REMOVE_SNAKE, None)

    def sendInput(self, timestamp, pressed):
        timestamp += self.offset
        data = {"addr": self.addr, "pressed": pressed}
        message = Messaging.createMessage(Messaging.INPUT, timestamp, data)
        self.Send(message)
        self.addRotate(timestamp, self.addr, pressed)

    def Network_input(self, message):
        timestamp = message[Messaging.TIMESTAMP_TAG]
        data = message[Messaging.DATA_TAG]
        self.addRotate(timestamp, data["addr"], data["pressed"])

    def sendMove(self, timestamp):
        timestamp += self.offset
        message = Messaging.createMessage(Messaging.MOVE_SNAKE, timestamp, self.addr)
        self.Send(message)
        self.addMove(timestamp, self.addr)

    def Network_moveSnake(self, message):
        timestamp = message[Messaging.TIMESTAMP_TAG]
        player_id = message[Messaging.DATA_TAG]
        self.addMove(timestamp, player_id)

    def Network_newFood(self, message):
        timestamp = message[Messaging.TIMESTAMP_TAG]
        food_data = message[Messaging.DATA_TAG]
        self.addEvent(food_data["addr"], timestamp, Messaging.NEW_FOOD, food_data["fcell"])

    # any error message acquired - assume disconnection
    def Network_error(self, message):
        print "Error: disconnected from or not connected to server"
        self.Network_disconnected(message)

    def Network_disconnected(self, message, quit=False):
        # clear connection queue of all remaining msgs
        connect_q = connection.GetQueue()
        for i in range(len(connect_q)):
            del connect_q[i]

        # close everything
        self.reset()
        connection.close()
        if not quit:
            raise EndGame

    def updateConnection(self):
        connection.Pump()
        self.Pump()

if __name__ == "__main__":
    player = Player()
    pygame.init()
    player.joinGame(("localhost", 9999))
    while True:
        player.updateConnection()
        if player.events != None and player.game_state != None:
            player.sendMove(pygame.time.get_ticks())
