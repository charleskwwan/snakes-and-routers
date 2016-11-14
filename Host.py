from Player import Player
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

# class for open channel with a client
class ClientChannel(Channel):
	def setExtra(self, host, addr):
		self.host = host
		self.addr = addr
 
	def Network_joinGame(self, message):
		join_msg = self.host.createMessage(Player.JOIN_GAME, self.addr)
		self.Send(join_msg)

		# add new player to game state
		cell, direction = self.host.game_state.getEmptyInitialPosition()
		self.host.game_state.addSnake(self.addr, cell, direction)
		state_msg = self.host.createMessage(Player.GAME_STATE,
			self.host.game_state.stringify())
		self.Send(state_msg)

	def Network_input(self, message):
		# key pressed is at data tag
		self.host.game_state.addKeyPressed(self.addr, message[Player.DATA_TAG])
		self.host.sendKeypress(self.addr, message[Player.DATA_TAG])
		self.host.game_state.addKeyPressed(self.addr, message[Player.DATA_TAG])

	def sendNewSnake(self, addr):
		snake_msg = self.host.createMessage(Player.NEW_SNAKE, addr)
		self.Send(snake_msg)

class Host(Player, Server):
	def __init__(self, ip, port):
		# initialize super vars
		# inits address and game state in player
		Player.__init__(self, ip=ip, port=port)
		# inits server with local address
		Server.__init__(self, channelClass=ClientChannel, localaddr=(ip, port))

		# set up dict to store open channels
		self.clients = {}

		# create snake for host
		cell, direction = self.game_state.getEmptyInitialPosition()
		self.game_state.addSnake((ip, port), cell, direction)

	def Connected(self, channel, addr):
		print addr
		if addr not in self.channels:
			channel.setExtra(self, addr)
			self.clients[addr] = channel

	def sendKeypress(self, addr, keypress):
		data = {"addr" : addr, "key_pressed": keypress}
		msg = self.createMessage(Player.INPUT, data)
		for client in self.clients.values():
			client.Send(msg)

	def sendNewFood(self, food_cell):
		food_msg = self.createMessage(Player.NEW_FOOD, food_cell)
		for client in self.clients.values():
			client.Send(food_msg)

	def update(self):
		self.Pump()

if __name__ == "__main__":
	host = Host("localhost", 9999)
	while True:
		host.update()

