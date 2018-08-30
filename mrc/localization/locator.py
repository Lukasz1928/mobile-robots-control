import threading
from dynaconf import settings
import itertools
import time


class Locator(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.locations = dict(itertools.product(settings.get('ROBOTS'), [None]))
        self.data_reader = settings.get('DATA_READER')
        self.data_processor = settings.get('DATA_PROCESSOR')
        self.interval = settings.get('INTERVAL', 0)
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.__update_locations()
            time.sleep(self.interval)

    def stop(self):
        self.running = False

    def is_running(self):
        return self.running

    def __update_locations(self):
        raw_data = self.data_reader()
        processed_data = self.data_processor(raw_data) if self.data_processor is not None else raw_data
        self.locations = processed_data

    def get_locations(self, robot_id=None):
        if not self.is_running():
            self.__update_locations()
        return self.locations[robot_id] if robot_id is not None else self.locations
