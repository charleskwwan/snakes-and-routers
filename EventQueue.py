from HeapWrap import *
from GameState import *
from Messaging import *

class DeadQueue(Exception):
    pass

# event repreentation: 
#   - (timestamp, type, values)
#   - e.g. (3424, "input", pygame.K_UP)
class EventQueue(Heap):
    def __init__(self, game_state, queue_id=None, q=[]):
        self.game_state = game_state # for pushing events to
        self.queue_id = queue_id # optional, for non-hosts
        Heap.__init__(self, q, key=lambda e: e[0]) # use timestamp as key

    def toList(self):
        items = [e[1] for e in self.getItems()]
        return items

    # executes the highest priority event, pushing it to the game state
    # input/moveSnake should only be executed by clients - have queue_ids
    def execute(self):
        timestamp, ty, action  = self.pop() # raises Empty if nothing in queue
        if ty == Messaging.NEW_SNAKE: # action: name, (cell, direction)
            name, (cell, direction) = action
            if self.game_state.hasSnake(self.queue_id):
                self.game_state.respawnSnake(self.queue_id, cell, direction)
            else:
                self.game_state.addSnake(self.queue_id, name, cell, direction)
        elif ty == Messaging.REMOVE_SNAKE: # action: none
            self.game_state.removeSnake(self.queue_id)
            raise DeadQueue(self.queue_id)
        elif ty == Messaging.INPUT: # action: key pressed
            self.game_state.rotateSnake(self.queue_id, action)
        elif ty == Messaging.MOVE_SNAKE:
            self.game_state.moveSnake(self.queue_id)
        elif ty == Messaging.NEW_FOOD: # action = fcell
            self.game_state.addFood(action)
        elif ty == Messaging.BLANK: # maintain connection, do nothing
            pass
