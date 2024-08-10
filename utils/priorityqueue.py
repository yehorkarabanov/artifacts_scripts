from queue import PriorityQueue


class PQueue(PriorityQueue):
    def toJSON(self):
        elements = []
        temp_queue = PriorityQueue()
        while not self.empty():
            elements
