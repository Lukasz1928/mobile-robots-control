from mrc.control.steering.abstract import AbstractDTPSteeringStrategy
from mrc.control.steering.exceptions import ObstacleOnTheWayException


class CarefulDTPSteeringStrategy(AbstractDTPSteeringStrategy):

    def __init__(self, motor_driver):
        self.all_robots_position = None
        self.motor_driver = motor_driver

    def _in_route(self, target_point):
        r, theta = target_point
        res = []
        for (name, pos) in self.all_robots_position.values():
            r_i, theta_i = pos
            if r_i < r / 2 and theta_i - 0.17 < theta < theta_i + 0.17:
                res.append(name)
        return bool(len(res)), res

    def drive_to_point(self, point):
        sth_in_route, names = self._in_route(point)
        if sth_in_route:
            raise ObstacleOnTheWayException("The path is blocked by robots: " + str(names))
        else:
            self.motor_driver.drive_to_point(point)

    def update_data(self, *kwargs):
        self.all_robots_position = kwargs['positions']


class SimpleDTPSteeringStrategy(AbstractDTPSteeringStrategy):

    def __init__(self, motor_driver):
        self.all_robots_position = None
        self.motor_driver = motor_driver

    def drive_to_point(self, point):
        self.motor_driver.drive_to_point(point)

    def update_data(self, **kwargs):
        self.all_robots_position = kwargs['positions']
