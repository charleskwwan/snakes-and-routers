# Module for creating network messages in snake

class ConnectionException(Exception):
    pass

class InvalidMessageType(Exception):
    pass

# abstract class, do not instantiate
class Messaging(object):
    validTypes = \
    JOIN_GAME, NEW_SNAKE, GAME_STATE, INPUT, MOVE_SNAKE, REMOVE_SNAKE, NEW_FOOD, BLANK = \
    ["joinGame", "newSnake", "gameState", "input", "moveSnake", "removeSnake", "newFood", "blank"]
    DATA_TAG = "data"
    TIMESTAMP_TAG = "timestamp"

    # create a valid message for podsixnet
    @classmethod
    def createMessage(self, ty, timestamp, data):
        if ty in Messaging.validTypes:
            # package in sendable dictionary
            message = {"action": ty, Messaging.TIMESTAMP_TAG: timestamp, Messaging.DATA_TAG: data}
            return message
        else:
            raise InvalidMessageType  
