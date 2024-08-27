from pydantic_settings import BaseSettings
from typing import Dict
from config.config import TOKEN_


class Settings(BaseSettings):
    SERVER: str = "https://api.artifactsmmo.com"
    TOKEN: str = TOKEN_
    HEADERS: Dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {TOKEN}",
    }
    DEBUG: bool = True


settings = Settings()
