import json

from utils.singleton import Singleton


class ActionQueue(metaclass=Singleton):
    def __init__(self, character_list):
        self.queues = {}
        for character in character_list:
            self.queues[character.data["name"]] = PriorityQueue()
            self.queues[character.data["name"]].put((2, "move"))
            self.queues[character.data["name"]].put((1, "craft"))
        print(json.dumps(self.queues))
