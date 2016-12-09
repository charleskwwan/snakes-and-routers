import PodSixNet
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from Constants import *
from Messaging import *
from GameState import *
from EventQueueHandler import *

class ChannelTimeout(ConnectionException): # ConnectionException from Messaging
    pass

# timestamps for clients and host:
#   - clients send only ticks to host
#   - host sends tick AND priority to everyone else

# class for open channel with client
class ClientChannel(Channel):
    # workaround so that channel is aware of host and its client's address
    def setExtra(self, host, addr):
        self.host = host
        self.addr = addr

    def Network_joinGame(self, message):
        ticks = pygame.time.get_ticks()

        # acknowledge message, send back new client's id and time offset
        player_time = message[Messaging.TIMESTAMP_TAG]
        offset = ticks - player_time
        join_msg = Messaging.createMessage(Messaging.JOIN_GAME, offset, self.addr)
        self.Send(join_msg)

        # add new player to game state, and send full state to client
        encoded_state = self.host.encodeState()
        state_msg = Messaging.createMessage(Messaging.GAME_STATE, ticks, encoded_state)
        self.Send(state_msg)

        # send new snakes to everyone
        name = self.host.generateName()
        cell, direction = self.host.addPlayer(ticks, self.addr, name)
        self.host.sendSnake(ticks, self.addr, name, cell, direction)

    def Network_input(self, message):
        # receive, update own game state first
        timestamp = message[Messaging.TIMESTAMP_TAG]
        data = message[Messaging.DATA_TAG]
        self.host.addRotate(timestamp, data["addr"], data["pressed"])
        # broadcast input to everyone
        self.host.broadcast(message, [self.addr]) # dont send back to self

    def Network_moveSnake(self, message):
        # receive, update self first
        timestamp = message[Messaging.TIMESTAMP_TAG]
        addr = message[Messaging.DATA_TAG]
        self.host.addMove(timestamp, addr)
        # broadcast move to everyone
        self.host.broadcast(message, [self.addr]) # dont send back to self

    def Network_removeSnake(self, message):
        timestamp = message[Messaging.TIMESTAMP_TAG]
        self.host.broadcast(message, [self.addr])
        self.host.addEvent(self.addr, timestamp, Messaging.REMOVE_SNAKE, None)
        self.host.closeChannel(self.addr)

    def Network_disconnected(self, message):
        ticks = pygame.time.get_ticks()
        rm_msg = Messaging.createMessage(Messaging.REMOVE_SNAKE, ticks, self.addr)
        Network_removeSnake(rm_msg)

    def Network(self, message):
        self.host.setLast(self.addr)

class Host(Server):
    TIMEOUT = CLI_TIMEOUT

    def __init__(self, ip, port):
        # initialize state information for host
        # network stuff
        self.addr = ip, port # external address
        self.clients = {} # for open channels
        self.lasts = {} # last time msg received for channel

        # game state stuff
        self.game_state = GameState()
        self.events = EventQueueHandler(self.game_state)
        self.events.newQueue(self.addr) # for self
        self.seen = 0 # number of snakes every connected to host

        # initialize super, must used localhost
        Server.__init__(self, channelClass=ClientChannel, localaddr=self.addr)

    def getID(self):
        return self.addr

    ##### server/network methods
    # when new connection established
    def Connected(self, channel, addr):
        if addr not in self.clients:
            channel.setExtra(self, addr)
            self.clients[addr] = channel
            self.lasts[addr] = None

    # sends a mesage to ALL clients; can exclude some
    def broadcast(self, message, exclude=[]):
        for addr, channel in self.clients.items():
            if addr not in exclude:
                channel.Send(message)

    # sets the last time value for a msg received
    def setLast(self, addr, last=None):
        if not last:
            last = pygame.time.get_ticks()
        self.lasts[addr] = last

    def closeChannel(self, addr):
        self.clients[addr].close()
        del self.clients[addr]
        del self.lasts[addr]

    # broadcast blank msgs to keep queues moving for everyone
    def sendBlanks(self):
        ticks = pygame.time.get_ticks()
        blank_msg = Messaging.createMessage(Messaging.BLANK, ticks, self.addr)
        self.broadcast(blank_msg)
        self.events.addEvent(self.addr, ticks, Messaging.BLANK, None)

    def sendSnake(self, timestamp, addr, name, cell, direction):
        new_snake = {"addr": addr, "name": name, "cell": cell, 
                     "direction": direction}
        new_snake_msg = Messaging.createMessage(Messaging.NEW_SNAKE, timestamp, new_snake)
        self.broadcast(new_snake_msg)

    def shutdown(self):
        for chnl in self.clients.values():
            chnl.close()
        self.close()

    def updateConnection(self):
        self.Pump()
        # check current time against lasts; if any are late, raise
        # ChannelTimeout with all waiting channel addrs
        ticks = pygame.time.get_ticks()
        lates = [] # late channel addrs
        for addr, last in self.lasts.items():
            if last and ticks - last >= Host.TIMEOUT:
                lates.append(addr)
        if lates:
            raise ChannelTimeout(lates)

    ##### state methods
    def encodeState(self):
        encoded_game = self.game_state.encode()
        encoded_qs = self.events.encode()
        return encoded_game, encoded_qs

    def generateName(self):
        name = "s" + str(self.seen)
        self.seen += 1
        return name

    def makeFood(self):
        ticks = pygame.time.get_ticks()
        fcell = self.game_state.makeFoodCell() # does not make actual food
        if not fcell: # no fcell, none generated
            return
        food_data = {"addr": self.addr, "fcell": fcell}
        food_msg = Messaging.createMessage(Messaging.NEW_FOOD, ticks, food_data)
        self.broadcast(food_msg)
        self.events.addEvent(self.addr, ticks, Messaging.NEW_FOOD, fcell)

    def addPlayer(self, timestamp, player_id, name):
        # initialize new queue for player
        self.events.newQueue(player_id)

        # add snake creation to queue
        pos = self.game_state.getEmptyInitialPosition()
        self.events.addEvent(player_id, timestamp, Messaging.NEW_SNAKE, (name, pos))

        return pos

    def addMove(self, timestamp, player_id):
        self.events.addEvent(player_id, timestamp, Messaging.MOVE_SNAKE, None)

    def addRotate(self, timestamp, player_id, pressed):
        self.events.addEvent(player_id, timestamp, Messaging.INPUT, pressed)

    def addEvent(self, player_id, timestamp, ty, action):
        self.events.addEvent(player_id, timestamp, ty, action)

    def updateEvents(self):
        try:
            self.events.execute()
        except UnsyncedQueue:
            pass # todo: implement more robust behavior
        except DeadSnake as err:
            ticks = pygame.time.get_ticks()
            snake_id = err.args[0]
            name = err.args[1]
            pos = (cell, direction) = self.game_state.getEmptyInitialPosition()
            self.sendSnake(ticks, snake_id, name, cell, direction)
            self.events.addEvent(snake_id, ticks, Messaging.NEW_SNAKE, (name, pos))

    def blit(self, screen): #temp
        for food in self.game_state.foods:
            food.blit(screen)

if __name__ == "__main__":
    host = Host("localhost", 9999)
    while True:
        host.updateConnection()
