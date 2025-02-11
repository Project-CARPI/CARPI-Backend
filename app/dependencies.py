from typing import Annotated, Generator

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import Session, SQLModel, create_engine


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
    url=f"{_settings.db_dialect}+{_settings.db_api}"
    + f"://{_settings.db_username}:{_settings.db_password}"
    + f"@{_settings.db_hostname}/{_settings.db_schema}",
    # echo=True,
)


# Creates tables in database based on SQLModel table models
def create_schema_and_tables():
    SQLModel.metadata.create_all(_engine)


def get_settings() -> _Settings:
    return _settings


def get_db_session() -> Generator[Session, None, None]:
    with Session(_engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db_session)]
