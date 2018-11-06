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
            target_position = self.configurator.target_position
            if self._are_locations_approximately_same(target_position,
                                                      self.locator.get_locations(self.configurator.master_unit)):
                angle = target_position.angle
                radius = target_position.radius
                self.drive_to_point(angle, radius)

    def is_running(self):
        return self.running

    def stop(self):
        self.running = False

    def _are_locations_approximately_same(self, location_one, location_two):
        # TODO
        return False
