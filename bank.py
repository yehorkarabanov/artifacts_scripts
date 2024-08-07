import json
import requests
from utils.singleton import Singleton
from settings import settings
from loguru import logger


class Bank(metaclass=Singleton):
    def __init__(self):
        response = requests.get(
            url=f"{settings.SERVER}/my/bank/gold",
            headers=settings.HEADERS,
        )
        if response.status_code == 200:
            self.gold = json.loads(response.text)["data"]["quantity"]
            logger.info(f"Bank gold received, current balance is {self.gold}")
        else:
            logger.error("Bank gold receiving error")
            self.gold = 0

        response = requests.get(
            url=f"{settings.SERVER}/my/bank/items",
            headers=settings.HEADERS,
        )
        if (
            response.status_code == 404
            and json.loads(response.text)["error"]["message"] == "Items not found."
        ):
            logger.info("Bank storage is empty")
            self.storage = []
        elif response.status_code != 200:
            logger.error("Bank storage receiving error")
            self.storage = []
        else:
            self.storage = json.loads(response.text)["data"]
            logger.info(
                f"Bank storage received, current storage is {len(self.storage)}"
            )
