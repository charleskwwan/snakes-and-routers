from EventQueue import *

# to be raised when an event queue has no events available
# to execute any event, every queue must have at least one available
class UnsyncedQueue(Exception):
    pass

# to be raised when there are no queues
class NoQueues(Exception):
    pass

class EventQueueHandler(object):
    def __init__(self, game_state, src=None):
        self.game_state = game_state
        if src: 
            self.decode(src)
        else:
            self.qcounts = {}
            self.events = Heap(key=lambda e: e[0])

    def encode(self):
        return {"qcounts": self.qcounts, "events": self.events.getItems()}

    def decode(self, src):
        self.qcounts = src["qcounts"]
        self.events = Heap(src=src["events"], key=lambda e: e[0])

    def newQueue(self, queue_id):
        self.qcounts[queue_id] = 0

    def deleteQueue(self, queue_id):
        if queue_id in self.qcounts:
            del self.qcounts[queue_id] 
        # let execute take care of deletion in self events

    def hasQueue(self, queue_id):
        return queue_id in self.qcounts

    def addEvent(self, queue_id, timestamp, ty, action):
        self.qcounts[queue_id] += 1
        self.events.push((timestamp, ty, action, queue_id))

    def process(self, queue_id, (timestamp, ty, action)):
        if ty == Messaging.NEW_SNAKE: # action: name, (cell, direction)
            name, (cell, direction) = action
            if self.game_state.hasSnake(queue_id):
                self.game_state.respawnSnake(queue_id, cell, direction)
            else:
                self.game_state.addSnake(queue_id, name, cell, direction)
        elif ty == Messaging.REMOVE_SNAKE: # action: none
            self.game_state.removeSnake(queue_id)
            raise DeadQueue(queue_id)
        elif ty == Messaging.INPUT: # action: key pressed
            self.game_state.rotateSnake(queue_id, action)
        elif ty == Messaging.MOVE_SNAKE:
            self.game_state.moveSnake(queue_id)
        elif ty == Messaging.NEW_FOOD: # action = fcell
            self.game_state.addFood(action)
        elif ty == Messaging.BLANK: # maintain connection, do nothing
            pass

    def execute(self):
        if len(self.qcounts) == 0:
            raise NoQueues

        for c in self.qcounts.values():
            if c <= 0:
                raise UnsyncedQueue

        # delete events that are not part of any queue
        while self.events.peek()[3] not in self.qcounts:
            self.events.pop()

        # get all evetns with the same gvt
        gvt = None
        nxts = []
        while not self.events.empty() and (not gvt or self.events.peek()[0] == gvt):
            timestamp, ty, action, queue_id = self.events.pop()
            if not gvt:
                gvt = timestamp
            nxts.append((queue_id, (timestamp, ty, action)))

        # process all
        for qid, event in nxts:
            try:
                self.process(qid, event)
                self.qcounts[qid] -= 1
            except DeadQueue as err:
                self.deleteQueue(qid)
