import PodSixNet
from PodSixNet.Connection import ConnectionListener, connection
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
# import GameState

class Player(ConnectionListener, Channel):
	validTypes = ["input", "newSnake", "gameState", "removeSnake"]

	# create a new player, which has its own ipaddr and port identity
	def __init__(ip, port):
		self.addr = (ip, port) # used as player's unique id
		# self.game_state = GameState.GameState()

	def sendMessage(dstaddr, ty, msg): # via connection listener
		self.Connect(dstaddr)
		data = {"action": ty, "msg": msg} # package as sendable dictionary
		self.Send(message)

	def Network_input(self, data):
		print data

	def Network_newSnake(self, data):
		print data

	def Network_gameState(self, data):
		print data

	def Network_removeSnake(self, data):
		print data