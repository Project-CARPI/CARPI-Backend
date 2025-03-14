from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import lifespan_func

from .routers import course, scraper

app = FastAPI(root_path="/api/v1", lifespan=lifespan_func)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.include_router(course.router)
app.include_router(scraper.router)
