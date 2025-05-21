from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

# https://docs.pydantic.dev/latest/concepts/pydantic_settings/#dotenv-env-support
class Config(BaseSettings):
    model_config: SettingsConfigDict = {
        "env_file": ".env"
    }
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLLBACK: Optional[bool] = False
    ELASTICSEARCH_HOST: Optional[str] = None
    ELASTICSEARCH_PORT: Optional[str] = None
    ELASTICSEARCH_INDEX: Optional[str] = None
    ELASTICSEARCH_LOG_LEVEL: Optional[str] = None

config=Config()