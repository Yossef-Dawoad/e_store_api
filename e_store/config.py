# import os
# APP_ENV = os.getenv('APP_ENV', 'development')
# DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'postgres')
# DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '<PASSWORD>')
# DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
# DATABASE_NAME = os.getenv('DATABASE_NAME', 'e_store')

# TEST_DATABASE_NAME = os.getenv('TEST_DATABASE_NAME', 'e_store_test')
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "e-store API"
    database_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache()
def get_settings():
    return Settings()
