from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

@lru_cache()
def get_settings():
    return Settings()

class Settings(BaseSettings):
    LOG_LEVEL: str = "WARNING"
    REST_COUNTRIES_BASE_URL: str
    WEATHER_BASE_URL: str
    WEATHERAPI_KEY: str

    model_config = SettingsConfigDict(env_file=".env")
