import math
from loguru import logger
from config.settings import settings
from queue import Queue
from utils.find_on_map import find_on_map
import anyio


class CharacterController:
    def __init__(self, character_data):
        self.data = character_data
        self._queue = Queue()

    async def move_to(self, session, coordinates):
        if (self.data["x"], self.data["y"]) == coordinates:
            return
        async with session.post(
            url=f"{settings.SERVER}/my/{self.data['name']}/action/move",
            headers=settings.HEADERS,
            json={"x": coordinates[0], "y": coordinates[1]},
        ) as response:
            text = await response.text()
            if response.status != 200:
                logger.error(
                    f"Failed to move character {self.data['name']} to {coordinates}"
                )
                raise Exception(
                    f"Server exception code:{response.status.status_code}, {text}"
                )
            data = await response.json()
            data = data["data"]
        self.data["x"], self.data["y"] = coordinates
        logger.info(f"Moved character {self.data['name']} to {coordinates}")
        await anyio.sleep(data["cooldown"]["remaining_seconds"])

    async def find_nearest(self, session, resource):
        resources = await find_on_map(session, resource)
        resource_cords = (resources[0]["x"], resources[0]["y"])
        for item in resources:
            if math.sqrt(
                (self.data["x"] - item["x"]) ** 2 + (self.data["y"] - item["y"]) ** 2
            ) > math.sqrt(
                (self.data["x"] - resource_cords[0]) ** 2
                + (self.data["y"] - resource_cords[1]) ** 2
            ):
                resource_cords = (resource_cords[0], resource_cords[1])
        return resource_cords

    async def harvest_resource(self, session):
        async with session.post(
            url=f"{settings.SERVER}/my/{self.data['name']}/action/gathering",
            headers=settings.HEADERS,
        ) as response:
            if response.status != 200:
                text = await response.text()
                logger.error(f"Failed to harvest resource for {self.data['name']}")
                raise Exception(f"Server exception code:{response.status}, {text}")
            data = await response.json()
            data = data["data"]
        logger.info(f"Harvested resource for {self.data['name']}")
        await anyio.sleep(data["cooldown"]["remaining_seconds"])

    def put_item_to_bank(self, item):
        pass

    def put_all_items_to_bank(self):
        pass

    async def harvest_task(self, session, resource, amount):
        logger.info(f"Create harvest {resource} {amount} for {self.data['name']}")
        cords = await self.find_nearest(session, resource)
        await self.move_to(session, cords)
        for i in range(amount):
            await self.harvest_resource(session)

    def add_task_to_queue(self, task):
        self._queue.put(task)

    def get_tasks_from_queue(self):
        return self._queue.get()
