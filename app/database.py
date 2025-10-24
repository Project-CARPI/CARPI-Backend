from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine

from app.config import CARPIFastAPISettings

_engine: Engine = None


def init_db_engine(settings: CARPIFastAPISettings) -> None:
    global _engine
    _engine = create_engine(
        url=f"{settings.db_dialect}+{settings.db_api}"
        + f"://{settings.db_username}:{settings.db_password}"
        + f"@{settings.db_hostname}/{settings.db_schema}",
        # echo=True,
    )
    SQLModel.metadata.create_all(_engine)


def dispose_db_engine() -> None:
    _engine.dispose()


def get_db_session() -> Generator[Session, None, None]:
    with Session(_engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db_session)]
