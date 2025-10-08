import asyncio

from fastapi import APIRouter, Response

from app.scrapers import sis_scraper

router = APIRouter(prefix="/scraper")


@router.post("/start")
async def start_scraper():
    if sis_scraper.is_running():
        return Response(status_code=409, content="Scraper already running")
    asyncio.create_task(sis_scraper.main())
    return Response(status_code=202, content="Scraper started")
