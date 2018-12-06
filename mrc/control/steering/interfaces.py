from mrc.control.steering.abstract import AbstractDTPSteeringInterface
from mrc.shared.exceptions.exceptions import ObstacleOnTheWayException


class CarefulDTPSteeringInterface(AbstractDTPSteeringInterface):

    def __init__(self, motor_driver, angle_offset=0.39):
        self.master = None
        self.all_robots_position = None
        self.motor_driver = motor_driver
        self.angle_offset = angle_offset

    def _in_route(self, target_point):
        r, theta = target_point
        res = []
        for (name, pos) in self.all_robots_position.values():
            if name != self.master:
                r_i, theta_i = pos
                if r_i < r / 2 and theta_i - self.angle_offset < theta < theta_i + self.angle_offset:
                    res.append(name)
        return bool(len(res)), res

    def drive_to_point(self, point):
        sth_in_route, names = self._in_route(point)
        if sth_in_route:
            raise ObstacleOnTheWayException("The path is blocked by robots: " + str(names))
        else:
            self.motor_driver.drive_to_point(*point)

    def update_data(self, locations, master):
        self.all_robots_position = locations
        self.master = master


class SimpleDTPSteeringInterface(AbstractDTPSteeringInterface):

    def __init__(self, motor_driver):
        self.all_robots_position = None
        self.motor_driver = motor_driver
        self.master = None

    def drive_to_point(self, point):
        self.motor_driver.drive_to_point(*point)

    def update_data(self, locations, master):
        self.all_robots_position = locations
        self.master = master