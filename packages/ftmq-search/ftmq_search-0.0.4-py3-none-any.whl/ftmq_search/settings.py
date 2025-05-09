from urllib.parse import urlparse

from nomenklatura import settings
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_db_url() -> str:
    """
    Try to align with NK setting if it's sqlite
    """
    parsed = urlparse(settings.DB_URL)
    if "sqlite" in parsed.scheme:
        return settings.DB_URL
    return "sqlite:///ftmqs.db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ftmqs_")

    debug: bool = Field(alias="debug", default=False)

    uri: str = get_db_url()
    yaml_uri: str | None = None
    json_uri: str | None = None

    # sql
    sql_table_name: str = "ftmqs"


class ElasticSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="elastic_")

    index: str = "ftmqs"
    user: str = ""
    password: str = ""
