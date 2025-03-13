from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .dependencies import lifespan_func
from .routers import course

app = FastAPI(root_path="/api/v1", lifespan=lifespan_func)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.include_router(course.router)
