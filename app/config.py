from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal['DEV', 'TEST', 'PROD']

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    DATABASE_URL: str = None

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def get_database_url(cls, v, info):
        return f"postgresql+asyncpg://{info.data['DB_USER']}:{info.data['DB_PASS']}@{info.data['DB_HOST']}:{info.data['DB_PORT']}/{info.data['DB_NAME']}"

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    TEST_DATABASE_URL: str = None

    @field_validator("TEST_DATABASE_URL", mode="before")
    @classmethod
    def get_test_database_url(cls, v, info):
        return f"postgresql+asyncpg://{info.data['TEST_DB_USER']}:{info.data['TEST_DB_PASS']}@{info.data['TEST_DB_HOST']}:{info.data['TEST_DB_PORT']}/{info.data['TEST_DB_NAME']}"

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int

    ALGORITHM: str
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()