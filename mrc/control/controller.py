from threading import Thread
from typing import Callable

from mrc.configuration.configurator import Configurator
from mrc.localization.locator import Locator


class Controller(Thread):
    def __init__(self, locator: Locator, drive_to_point: Callable([float, float], None), configurator: Configurator):
        super().__init__()
        self.drive_to_point = drive_to_point
        self.locator = locator
        self.configurator = configurator
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            if self.locator.get_locations(self.configurator.my_id) is not self.configurator.get_target_position():
                target_position = self.configurator.get_target_position()
                angle = target_position.angle
                radius = target_position.radius
                self.drive_to_point(angle, radius)

    def is_running(self):
        return self.running

    def stop(self):
        self.running = False
