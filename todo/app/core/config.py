from typing import Literal
from starlette.config import Config
from starlette.datastructures import Secret
from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import computed_field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    PREFIX: str = "/api"

    PROJECT_NAME: str = "TODO API"

    @computed_field  # type: ignore[misc]
    @property
    def DESCRIPTION(self) -> str:
        return f"{self.ENVIRONMENT} Environment"

    VERSION: str = "0.0.1"

    PROTOCOL: str = "http"
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    @computed_field  # type: ignore[misc]
    @property
    def url(self) -> str:
        return f"{self.PROTOCOL}://{self.HOST}:{self.PORT}"

    DATABASE_URL: str = ""
    TEST_DATABASE_URL: str = ""

    SECRET_KEY: str
    ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15


settings = Settings()
