import asyncio
import importlib
import pkgutil

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import background_scheduler, lifespan_func
from app.scrapers import sis_scraper


def scan_and_include_routers(app: FastAPI, package: str) -> None:
    package_module = importlib.import_module(package)
    for _, module_name, _ in pkgutil.iter_modules(package_module.__path__):
        module = importlib.import_module(f"{package}.{module_name}")
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, APIRouter):
                app.include_router(attr)


def init_background_scheduler(bg_scheduler: BackgroundScheduler) -> None:
    bg_scheduler.add_job(
        lambda: asyncio.run(sis_scraper.main()),
        trigger=CronTrigger(day_of_week="mon", hour=4),
        timezone="America/New_York",
    )


app = FastAPI(root_path="/api/v1", lifespan=lifespan_func)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
_package_name = __name__.split(".")[0]
scan_and_include_routers(app, f"{_package_name}.routers")
init_background_scheduler(background_scheduler)
