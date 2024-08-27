import aiohttp
import requests
import json
import anyio
from config.settings import settings
from src.character_controller import CharacterController
from src.bank import Bank
from loguru import logger


class GameController:
    def __init__(self):
        logger.add("log.log")

        self.bank = Bank()

        response = requests.get(
            url=f"{settings.SERVER}/my/characters",
            headers=settings.HEADERS,
        )

        if response.status_code == 200:
            data = json.loads(response.text)["data"]
            logger.info("Characters has been successfully retrieved")
        else:
            logger.error("Failed to retrieve characters")
            raise Exception(
                f"Initialization exception code:{response.status_code}, {response.text}"
            )

        self.character_list = []
        for ch in data:
            character = CharacterController(ch)
            self.character_list.append(character)

    def find_character_with_highest_level(self, characteristic):
        character_top = self.character_list[0]
        for character in self.character_list:
            if (
                character.data[f"{characteristic}_level"]
                > character_top.data[f"{characteristic}_level"]
            ):
                character_top = character
        return character_top

    def get_characters_by_skill(self, skill, min_lvl):
        return [
            chr for chr in self.character_list if chr.data[f"{skill}_level"] >= min_lvl
        ]

    def _get_resource_data(self, resource):
        response = requests.get(url=f"{settings.SERVER}/items/{resource}")
        if response.status_code != 200:
            logger.error(f"Failed to retrieve {resource} data")
            raise Exception(f"Failed to retrieve {resource} data")

        data = json.loads(response.text)["data"]
        logger.info(f"Resource {resource} data has been retrieved")
        return data

    async def create_harvest_task(self, harvest_resource, amount):
        data = self._get_resource_data(harvest_resource)
        if data["item"]["type"] != "resource":
            logger.error(f"Trying to harvest {data['item']['craft']} that is craftable")
            raise Exception(
                f"Trying to harvest {data['item']['craft']} that is craftable"
            )
        characters = self.get_characters_by_skill(
            data["item"]["subtype"], data["item"]["level"]
        )
        total_skill = sum(
            [ch.data[f"{data['item']['subtype']}_level"] for ch in characters]
        )

        async with aiohttp.ClientSession() as session:
            async with anyio.create_task_group() as tg:
                for ch in characters:
                    tg.start_soon(
                        ch.harvest_task,
                        session,
                        harvest_resource,
                        int(
                            ch.data[f"{data['item']['subtype']}_level"]
                            / total_skill
                            * amount
                        ),
                    )

    def start(self):
        try:
            anyio.run(self.create_harvest_task, "ash_wood", 300)
        except KeyboardInterrupt:
            logger.info("main loop stopped")
