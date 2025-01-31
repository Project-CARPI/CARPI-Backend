from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .controllers import course_controller

app = FastAPI(root_path="/api/v1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"]
)
app.include_router(course_controller.router)
