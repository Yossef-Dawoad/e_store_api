from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "e-store API"
    database_url: str
    celery_broker_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class MailSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_SERVER: str
    MAIL_PORT: int

    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool

    MAIL_FROM: str
    MAIL_DEBUG: bool
    MAIL_FROM_NAME: str = "estore-app"
    USE_CREDENTIALS: bool  # set true for prod

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_mail_settings() -> MailSettings:
    return MailSettings()
