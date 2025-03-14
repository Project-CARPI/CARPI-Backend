import importlib
import pkgutil

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import lifespan_func


def scan_and_include_routers(app: FastAPI, package: str) -> None:
    package_module = importlib.import_module(package)
    for _, module_name, _ in pkgutil.iter_modules(package_module.__path__):
        module = importlib.import_module(f"{package}.{module_name}")
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, APIRouter):
                app.include_router(attr)


app = FastAPI(root_path="/api/v1", lifespan=lifespan_func)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
_package_name = __name__.split(".")[0]
scan_and_include_routers(app, f"{_package_name}.routers")
