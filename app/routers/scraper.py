import asyncio

from fastapi import APIRouter

from ..scrapers import sis_scraper

_is_scraper_running = False

router = APIRouter(prefix="/scraper")


def scrape_courses():
    global _is_scraper_running
    if _is_scraper_running:
        print("Scraper already running")
        return False
    _is_scraper_running = True
    asyncio.run(sis_scraper.main())
    _is_scraper_running = False
    return True
