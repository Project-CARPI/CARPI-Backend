import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class CARPIFastAPISettings(BaseSettings):
    db_dialect: str
    db_api: str
    db_hostname: str
    db_username: str
    db_password: str
    db_schema: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env")
    )


_SETTINGS = CARPIFastAPISettings()


def get_app_settings() -> CARPIFastAPISettings:
    return _SETTINGS
