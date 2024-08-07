from pydantic_settings import BaseSettings
from typing import List, Dict
from config import TOKEN_, CHARACTER_NAMES_


class Settings(BaseSettings):
    SERVER: str = "https://api.artifactsmmo.com"
    TOKEN: str = TOKEN_
    CHARACTER_NAMES: List[str] = CHARACTER_NAMES_
    HEADERS: Dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {TOKEN}",
    }
    COOLDOWN: int = 25


settings = Settings()
