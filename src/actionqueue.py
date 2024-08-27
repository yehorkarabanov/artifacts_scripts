import json
from utils.singleton import Singleton
from loguru import logger


class ActionQueue(metaclass=Singleton):
    def __init__(self, character_list):
        try:
            try:
                data = {}
                with open("actions.json", "r") as file:
                    data = json.loads(file.read())
            except FileNotFoundError:
                logger.error("actions.json file not found")

            self.queues = {}
            for character in character_list:
                if character.data["name"] not in data:
                    self.queues[character.data["name"]] = []
                else:
                    self.queues[character.data["name"]] = data[character.data["name"]]

            logger.info(
                f"Initializing action queue with {len(character_list)} characters"
            )

        except Exception as e:
            logger.error(f"Exception while initializing action queue: {e}")
            raise Exception(f"Exception while initializing action queue: {e}")

    def save(self):
        try:
            with open("actions.json", "w") as file:
                file.write(json.dumps(self.queues))
            logger.info("Actions saved")
        except Exception as e:
            logger.error(f"Exception while saving action queue: {e}")
            raise Exception(f"Exception while saving action queue: {e}")

    def get_action(self, charname):
        if charname not in self.queues:
            raise KeyError(f"No such character: {charname}")
        return self.queues[charname].pop(0)
