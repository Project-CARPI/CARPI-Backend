import importlib
import pkgutil

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import lifespan_func


def scan_and_include_routers(app: FastAPI) -> None:
    app_package_name = __name__.split(".")[0]
    package_module_name = f"{app_package_name}.routers"
    package_module = importlib.import_module(package_module_name)
    for _, module_name, _ in pkgutil.iter_modules(package_module.__path__):
        module = importlib.import_module(f"{package_module_name}.{module_name}")
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, APIRouter) and getattr(attr, "__module__", None) == module.__name__:
                app.include_router(attr)


app = FastAPI(root_path="/api/v1", lifespan=lifespan_func)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
scan_and_include_routers(app)
