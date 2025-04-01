import importlib
import pkgutil
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_app_settings
from app.database import dispose_db_engine, init_db_engine

BACKGROUND_SCHEDULER = BackgroundScheduler()


@asynccontextmanager
async def lifespan_func(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Initializes resources throughout the FastAPI application's lifespan and
    ensures proper cleanup on application shutdown.
    """
    # Initialize database connection pool
    init_db_engine(get_app_settings())
    # Start background job scheduler
    BACKGROUND_SCHEDULER.start()

    yield

    dispose_db_engine()
    BACKGROUND_SCHEDULER.shutdown()


def scan_and_include_routers(app: FastAPI) -> None:
    """
    Dynamically scans and loads all APIRouter instances from the 'routers'
    package.
    """
    app_package_name = __name__.split(".")[0]
    package_module_name = f"{app_package_name}.routers"
    package_module = importlib.import_module(package_module_name)
    for _, module_name, _ in pkgutil.iter_modules(package_module.__path__):
        module = importlib.import_module(f"{package_module_name}.{module_name}")
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, APIRouter):
                app.include_router(attr)


def init_background_scheduler(bg_scheduler: BackgroundScheduler) -> None:
    """
    Initializes the background task scheduler with tasks.
    """
    pass


app = FastAPI(root_path="/api/v1", lifespan=lifespan_func)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["GET"], allow_headers=["*"]
)
scan_and_include_routers(app)
init_background_scheduler(BACKGROUND_SCHEDULER)
