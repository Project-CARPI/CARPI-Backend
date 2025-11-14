import os
from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator, Generator

from fastapi import Depends, FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import carpi_data_model.models as models


class _Settings(BaseSettings):
    db_dialect: str
    db_api: str
    db_hostname: str
    db_username: str
    db_password: str
    db_schema: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env")
    )


_settings = _Settings()
_engine: Engine | None = None
_session_maker: sessionmaker | None = None


@asynccontextmanager
async def lifespan_func(app: FastAPI) -> AsyncGenerator[None, None]:
    # Initialize database connection pool
    global _engine, _session_maker
    if _engine is None:
        _engine = create_engine(
            url=f"{_settings.db_dialect}+{_settings.db_api}"
            + f"://{_settings.db_username}:{_settings.db_password}"
            + f"@{_settings.db_hostname}/{_settings.db_schema}",
            # echo=True,
        )
        _session_maker = sessionmaker(_engine)
    # Creates tables in database based on SQLAlchemy table models
    models.Base.metadata.create_all(_engine)

    yield

    _engine.dispose()


def get_app_settings() -> _Settings:
    return _settings


def get_db_session() -> Generator[Session, None, None]:
    if _session_maker is None:
        raise RuntimeError("Database engine is not initialized")
    with _session_maker() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db_session)]
