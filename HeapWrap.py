from heapq import *

# wrapper for heapq to allow oop and custom comparison function
class Heap(object):
    def __init__(self, init=None, key=lambda x: x):
        self.key = key
        if init:
            self._data = [(key(item), item) for item in init]
            heapify(self._data)
        else:
            self._data = []

    def getItems(self):
        return self._data[:]

    def empty(self):
        return len(self._data) == 0

    def push(self, item):
        heappush(self._data, (self.key(item), item))

    def pop(self):
        return heappop(self._data)[1] # [1] for item in tuple

    def peek(self):
        return self._data[0][1]

    def remove(self, item):
        self._data.remove((self.key(item), item))
        heapify(self._data) # reorganize necessary
    def __len__(self):
        return len(self._data)
