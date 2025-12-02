import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Zoom Data API"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    API_KEY: str
    CSV_FOLDER_PATH: str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
