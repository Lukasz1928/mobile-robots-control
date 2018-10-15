from threading import Thread
from typing import Callable

from mrc.localization.locator import Locator


class Controller(Thread):
    def __init__(self, locator: Locator, drive_to_point: Callable([float, float], None)):
        super().__init__()
        self.drive_to_point = drive_to_point
        self.locator = locator
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            pass

    def is_running(self):
        return self.running

    def stop(self):
        self.running = False
