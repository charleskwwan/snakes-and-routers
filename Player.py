import PodSixNet
from PodSixNet.Connection import ConnectionListener, connection
import GameState
import Messaging

class ConnectionException(Exception):
	pass

class Player(ConnectionListener):
	# create a new player, which has its own ipaddr and port identity
	def __init__(self):
		self.game_state = GameState.GameState()
		self.hostaddr = None # created when join game
		self.addr = None # used as own id, need to query host for it

	def getKey(self):
		return self.addr

	# game state functions, mainly wrappers
	def addKeyPressed(self, addr, pressed):
		self.game_state.addKeyPressed(addr, pressed)

	def updateSnakes(self, screen): # keys_pressed = {addr, key}
		self.game_state.updateSnakes(screen)

	def updateFood(self, screen, host=None):
		self.game_state.updateFood(screen, host=host)

	def blit(self, screen):
		self.game_state.blit(screen)

	# networking functions
	def joinGame(self, hostaddr):
		self.hostaddr = hostaddr
		self.Connect(self.hostaddr)
		message = Messaging.createMessage(Messaging.JOIN_GAME, "")
		self.Send(message)

	def Network_joinGame(self, message):
		self.addr = message[Messaging.DATA_TAG] # only thing in message is addr

	def Network_gameState(self, message):
		encoded_state = message[Messaging.DATA_TAG]
		self.game_state = GameState(json=encoded_state)

	def sendInput(self, key_pressed):
		if self.hostaddr == None:
			raise ConnectionException("Player not connected to host")
		else:
			message = Messaging.createMessage(Messaging.INPUT, key_pressed)
			self.Send(message)

	def Network_input(self, message):
		data = message[Messaging.DATA_TAG]
		self.game_state.addKeyPressed(data["addr"], data["key_pressed"])

	def Network_newFood(self, message):
		food_cell = message[Messaging.DATA_TAG]
		self.game_state.addFood(food_cell)

	def updateConnection(self):
		connection.Pump()
		self.Pump()

if __name__ == "main":
	player = Player()
	player,joinGame(("localhost", 9999))
	while True:
		player.updateConnection()