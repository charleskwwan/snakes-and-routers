import PodSixNet
from PodSixNet.Connection import ConnectionListener, connection
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
import GameState

class Player(object):
	# validTypes = ["input", "joinGame", "newSnake", "gameState", "removeSnake"]
	validTypes = \
	INPUT, JOIN_GAME, NEW_SNAKE, GAME_STATE, REMOVE_SNAKE, NEW_FOOD  = \
	["input", "joinGame", "newSnake", "gameState", "removeSnake", "newFood"]

	DATA_TAG = "data"

	# create a new player, which has its own ipaddr and port identity
	def __init__(self, ip, port):
		self.addr = (ip, port) # used as player's unique id
		self.game_state = GameState.GameState()

	def createMessage(self, ty, data):
		if ty in Player.validTypes:
			# package as sendable dictionary
			message = {"action": ty, Player.DATA_TAG: data}
			return message
		else:
			raise LookupError("Invalid message type")

	def getKey(self):
		return self.addr

	def addKeyPressed(self, addr, pressed):
		self.game_state.addKeyPressed(addr, pressed)

	def updateSnakes(self, screen): # keys_pressed = {addr, key}
		self.game_state.updateSnakes(screen)

	def updateFood(self, screen, host=None):
		self.game_state.updateFood(screen, host=host)

	def blit(self, screen):
		self.game_state.blit(screen)
