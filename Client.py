from Player import Player
from PodSixNet.Connection import ConnectionListener, connection
import jsonpickle

class Client(Player, ConnectionListener):
	def __init__(self):
		self.hostaddr = None

		# init player address and game state
		super(Client, self).__init__("", 0) # dont know own addr until connect

	def joinGame(self, hostaddr):
                print "attempting to join game"
		self.hostaddr = hostaddr
		self.Connect(self.hostaddr)
		message = self.createMessage(Player.JOIN_GAME, "")
		self.Send(message)

	def Network_joinGame(self, message):
		self.addr = message[Player.DATA_TAG]

	def Network_gameState(self, message):
		encoded_state = message[Player.DATA_TAG]
		self.game_state = jsonpickle.decode(encoded_state)
                print "connected"

	def sendInput(self, key_pressed):
		message = self.createMessage(Player.INPUT, key_pressed)
		self.Send(message)

	def Network_input(self, message):
		data = message[Player.DATA_TAG]
		self.game_state.addKeyPressed(data["addr"], data["key_pressed"])

	def update(self):
		connection.Pump()
		self.Pump()

if __name__ == "__main__":
	client = Client()
	client.joinGame(("localhost", 9999))
	while True:
		client.update()
