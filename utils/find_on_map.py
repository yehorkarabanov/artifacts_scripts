from config.settings import settings
from loguru import logger
import aiohttp


async def find_on_map(session, resource):
    try:
        async with session.get(
            url=f"{settings.SERVER}/resources/",
            headers=settings.HEADERS,
            params={"drop": resource},
        ) as response:
            if response.status != 200:
                text = await response.text()
                logger.error(
                    f"Server exception while getting drop from, code:{response.status}, {text}"
                )
                raise Exception(
                    f"Server exception while getting drop from, code:{response.status}, {text}"
                )
            drops = await response.json()
            drops = drops["data"]

        async with session.get(
            url=f"{settings.SERVER}/maps/",
            headers=settings.HEADERS,
            params={"content_code": drops[0]["code"]},
        ) as response:
            if response.status != 200:
                text = await response.text()
                logger.error(
                    f"Server exception while getting map with resource, code:{response.status}, {text}"
                )
                raise Exception(
                    f"Server exception while getting map with resource, code:{response.status}, {text}"
                )
            map_data = await response.json()
            return map_data["data"]

    except aiohttp.ClientError as e:
        logger.error(f"HTTP client error occurred: {str(e)}")
        raise

    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise
