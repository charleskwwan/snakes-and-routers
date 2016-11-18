# Module for creating messages

# valid types of messages
validTypes = \
INPUT, JOIN_GAME, NEW_SNAKE, GAME_STATE, REMOVE_SNAKE, NEW_FOOD  = \
["input", "joinGame", "newSnake", "gameState", "removeSnake", "newFood"]
DATA_TAG = "data"

# create a valid image ofr podsixnet
def createMessage(ty, data):
	if ty in validTypes:
		# package as sendable dictionary
		message = {"action": ty, DATA_TAG: data}
		return message
	else:
		raise LookupError("Invalid message type")
