from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
import Messaging
import GameState
from FoodHandler import FoodHandler

# class for open channel with a client
class ClientChannel(Channel):
    def setExtra(self, host, addr):
        self.host = host
        self.addr = addr
 
    def Network_joinGame(self, message):
        print "Message received..."
        join_msg = Messaging.createMessage(Messaging.JOIN_GAME, self.addr)
        self.Send(join_msg)

        # add new player to game state
        cell, direction = self.host.game_state.getEmptyInitialPosition()
        self.host.game_state.addSnake(self.addr, cell, direction)
        state_msg = Messaging.createMessage(Messaging.GAME_STATE,
            self.host.game_state.stringify())
        self.Send(state_msg)

        # send new snakes to everyone
        new_snake = {"addr": self.addr, "cell": cell, "direction": direction}
        new_snake_msg = Messaging.createMessage(Messaging.NEW_SNAKE, new_snake)
        for client in self.host.clients.values():
            if client.addr != self.addr:
                client.Send(new_snake_msg)

    def Network_input(self, message):
        # key pressed is at data tag
        self.host.game_state.addKeyPressed(self.addr, message[Messaging.DATA_TAG])
        self.host.sendKeypress(self.addr, message[Messaging.DATA_TAG])
        self.host.game_state.addKeyPressed(self.addr, message[Messaging.DATA_TAG])

    # todo: send to EVERYONE, not just one person
    def sendNewSnake(self, addr):
        snake_msg = Messaging.createMessage(Messaging.NEW_SNAKE, addr)
        self.Send(snake_msg)

class Host(Server, FoodHandler):
    def __init__(self, ip, port):
        print "Initializing host...\n"
        # initialize super vars
        # inits address and game state in player
        self.addr = (ip, port)
        self.game_state = GameState.GameState()
        # inits server with local address
        Server.__init__(self, channelClass=ClientChannel, localaddr=(ip, port))
        FoodHandler.__init__(self)

        # set up dict to store open channels
        self.clients = {}

        self.running = False

    def Connected(self, channel, addr):
        print addr
        if addr not in self.channels:
            channel.setExtra(self, addr)
            self.clients[addr] = channel

    def sendKeypress(self, addr, keypress):
        data = {"addr" : addr, "key_pressed": keypress}
        msg = Messaging.createMessage(Messaging.INPUT, data)
        for client in self.clients.values():
            client.Send(msg)

    def sendNewFood(self, food_cell):
        food_msg = Messaging.createMessage(Messaging.NEW_FOOD, \
            food_cell)
        for client in self.clients.values():
            client.Send(food_msg)

    def updateSnakes(self):
        self.game_state.updateSnakes()

    def updateFood(self):
        snakes = self.game_state.getSnakes()
        foods = self.game_state.getFoods()
        food_cell = self.createFood(snakes, foods, len(foods))
        if food_cell != None:
            self.sendNewFood(food_cell)

    def updateConnection(self):
        self.Pump()

if __name__ == "__main__":
    host = Host("localhost", 9999)
    while True:
        host.update()

