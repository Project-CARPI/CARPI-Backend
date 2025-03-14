import os
from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator, Generator

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import Depends, FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import Session, SQLModel, create_engine


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
_engine = None
background_scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan_func(app: FastAPI) -> AsyncGenerator[None, None]:
    # Initialize database connection pool
    global _engine
    _engine = create_engine(
        url=f"{_settings.db_dialect}+{_settings.db_api}"
        + f"://{_settings.db_username}:{_settings.db_password}"
        + f"@{_settings.db_hostname}/{_settings.db_schema}",
        # echo=True,
    )
    # Creates tables in database based on SQLModel table models
    SQLModel.metadata.create_all(_engine)
    # Start background job scheduler
    background_scheduler.start()

    yield

    _engine.dispose()
    background_scheduler.shutdown()


def get_app_settings() -> _Settings:
    return _settings


def get_db_session() -> Generator[Session, None, None]:
    with Session(_engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db_session)]
