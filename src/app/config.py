from functools import lru_cache
from pydantic import BaseSettings

"""
Configuration for the REST API
"""
class Settings(BaseSettings):
    token_key: str
    oauth_web_client_id: str
    oauth_desktop_client_id: str
    oauth_ios_client_id: str
    oauth_android_client_id: str
    db_connection_string: str    
    environment: str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()