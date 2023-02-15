from functools import lru_cache
from pydantic import BaseSettings

# Configuration for the REST API
class Settings(BaseSettings):
    db_connection_string: str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()