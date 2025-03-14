import asyncio

from fastapi import APIRouter, Response

from app.scrapers import sis_scraper

router = APIRouter(prefix="/scraper")


@router.post("/start")
def start_scraper():
    if not asyncio.run(sis_scraper.main()):
        return Response(status_code=409, content="Scraper already running")
