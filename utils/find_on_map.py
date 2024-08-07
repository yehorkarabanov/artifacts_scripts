import json
import requests
from settings import settings


def find_on_map(self, resource):
    response_map = requests.get(
        url=f"{settings.SERVER}/maps/",
        headers=settings.HEADERS,
        params={"content_code": resource},
    )
    if response_map.status_code != 200:
        raise Exception(
            f"Server exception code:{response_map.status_code}, {response_map.text}"
        )
    return json.loads(response_map.text)["data"]
