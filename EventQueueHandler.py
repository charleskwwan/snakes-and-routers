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
            self.qs = {}

    # for network export
    def encode(self):
        qlists = [q.toList() for q in self.qs.values()]
        return dict(zip(self.qs.keys(), qlists))

    def decode(self, encoded):
        self.qs = {qid: EventQueue(self.game_state, qid, q) for qid, q in encoded.items()}

    def newQueue(self, queue_id): # queue_id = snake_id
        self.qs[queue_id] = EventQueue(self.game_state, queue_id)

    def deleteQueue(self, queue_id):
        del self.qs[queue_id]

    def hasQueue(self, queue_id):
        return queue_id in self.qs

    def addEvent(self, queue_id, timestamp, ty, action):
        q = self.qs[queue_id]
        q.put((timestamp, ty, action))

    # executes the earliest events available
    # for execution to happen, every queue must not be empty, so that the
    #   handler can tell if everyone is synced or not
    def execute(self):
        if len(self.qs) == 0:
            raise NoQueues
        # get global virtual time - earliest time on any queues
        gvt = None
        for q in self.qs.values():
            try:
                timestamp, ty, action = q.peek()
                gvt = timestamp if gvt == None else min(gvt, timestamp)
            except IndexError: # at least one queue does not have an event
                raise UnsyncedQueue

        # get all queues which should execute now based on gvt, and execute
        gvt_qs = [q for q in self.qs.values() if q.peek()[0] == gvt]
        for q in gvt_qs:
            try:
                q.execute()
            except DeadQueue as err:
                queue_id = err.args[0]
                self.deleteQueue(queue_id)
