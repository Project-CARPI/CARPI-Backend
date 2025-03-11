from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import course
from .dependencies import init_db_engine

app = FastAPI(root_path="/api/v1", lifespan=init_db_engine)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["GET"], allow_headers=["*"]
)
app.include_router(course.router)
