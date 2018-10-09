import threading
import time
from typing import Callable


class Locator(threading.Thread):
    def __init__(self, read_data: Callable, process_data: Callable, interval: float):
        threading.Thread.__init__(self)
        self.locations = dict()
        self.read_data = read_data
        self.process_data = process_data
        self.interval = interval
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self._update_locations()
            time.sleep(self.interval)

    def update_and_get_locations(self, robot_id=None):
        if not self.is_running():
            self._update_locations()
        return self.get_locations(robot_id)

    def _update_locations(self):
        raw_data = self.read_data()
        processed_data = self.process_data(raw_data) if self.process_data is not None else raw_data
        self.locations = processed_data

    def get_locations(self, robot_id=None):
        return self.locations[robot_id] if robot_id is not None else self.locations

    def stop(self):
        self.running = False

    def is_running(self):
        return self.running

    def set_interval(self, interval: float):
        self.interval = interval
