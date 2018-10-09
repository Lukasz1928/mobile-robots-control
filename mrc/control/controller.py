from threading import Thread
from typing import Callable

from mrc.localization.locator import Locator


class Controller(Thread):
    def __init__(self, locator: Locator, dtp_func: Callable([float, float], None)):
        super().__init__()
        self.dtp_func = dtp_func
        self.locator = locator
        self.running = False

    def run(self):
        self.running = True
        while True:
            pass

    def is_running(self):
        return self.running
