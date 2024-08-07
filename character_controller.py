import json
import math
import time
from typing import Tuple
from loguru import logger
import requests
from settings import settings


class CharacterController:
    def __init__(self, character_name):
        response = requests.get(
            url=f"{settings.SERVER}/characters/{character_name}",
            headers=settings.HEADERS,
        )

        if response.status_code == 200:
            self.character = json.loads(response.text)["data"]
            logger.info(f"Character {character_name} has been successfully retrieved")
        else:
            logger.error(f"Failed to retrieve character {character_name}")
            raise Exception(
                f"Initialization exception code:{response.status_code}, {response.text}"
            )

    def move_to(self, coordinates: Tuple[int, int]):
        if (self.character["x"], self.character["y"]) == coordinates:
            return
        response_move = requests.post(
            url=f"{settings.SERVER}/my/{settings.CHARACTER_NAMES[0]}/action/move",
            headers=settings.HEADERS,
            json=coordinates,
        )
        if response_move.status_code != 200:
            logger.error(
                f"Failed to move character {self.character['name']} to {coordinates}"
            )
            raise Exception(
                f"Server exception code:{response_move.status_code}, {response_move.text}"
            )

        self.character["x"], self.character["y"] = coordinates
        logger.info(f"Moved character {self.character['name']} to {coordinates}")

    def find_nearest(self, resources):
        resource_cords = (resources[0]["x"], resources[0]["y"])
        for item in resources:
            if math.sqrt(
                (self.character["x"] - item["x"]) ** 2
                + (self.character["y"] - item["y"]) ** 2
            ) > math.sqrt(
                (self.character["x"] - resource_cords[0]) ** 2
                + (self.character["y"] - resource_cords[1]) ** 2
            ):
                resource_cords = (resource_cords[0], resource_cords[1])
        return resource_cords

    def harvest_resource(self):
        response = requests.post(
            url=f"{settings.SERVER}/my/{settings.CHARACTER_NAMES[0]}/action/gathering",
            headers=settings.HEADERS,
        )
        if response.status_code != 200:
            logger.error(f"Failed to harvest resource for {self.character['name']}")
            raise Exception(
                f"Server exception code:{response.status_code}, {response.text}"
            )
        logger.info(f"Harvested resource for {self.character['name']}")
        time.sleep(settings.COOLDOWN)
