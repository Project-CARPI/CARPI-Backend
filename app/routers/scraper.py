import threading
from threading import Event as ThreadEvent

from fastapi import APIRouter


class ScraperThread(threading.Thread):
    def __init__(self, event: ThreadEvent):
        super().__init__()
        self.event = event

    def run(self):
        while not self.event.wait(1800):
            pass


router = APIRouter(prefix="/scraper")
