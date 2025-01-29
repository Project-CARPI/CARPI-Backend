from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import Session, create_engine


class _Settings(BaseSettings):
    db_dialect: str
    db_api: str
    db_hostname: str
    db_username: str
    db_password: str
    db_schema: str
    model_config = SettingsConfigDict(env_file=".env")

_settings = _Settings()
_engine = create_engine(
    url = f"{_settings.db_dialect}+{_settings.db_api}" +
          f"://{_settings.db_username}:{_settings.db_password}" +
          f"@{_settings.db_hostname}/{_settings.db_schema}"
)

def get_db_session():
    with Session(_engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db_session)]

def get_settings():
    return _settings
