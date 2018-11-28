from threading import Thread
from mrc.shared.position import PolarPosition


class Controller(Thread):
    def __init__(self, locator, drive_to_point, configurator):
        super().__init__()
        self.drive_to_point = drive_to_point
        self.locator = locator
        self.configurator = configurator
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            target_position = self.configurator.target_position
            if PolarPosition.are_positions_approximately_same(target_position,
                                                      self.locator.get_locations(self.configurator.master_unit)):
                angle = target_position.angle
                radius = target_position.radius
                self.drive_to_point(angle, radius)

    def is_running(self):
        return self.running

    def stop(self):
        self.running = False
