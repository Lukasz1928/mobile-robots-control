from mrc.control.steering.abstract import AbstractDTPSteeringStrategy


class CarefulDTPSteeringStrategy(AbstractDTPSteeringStrategy):

    def __init__(self, motor_driver):
        self.all_robots_position = None
        self.motor_driver = motor_driver

    def in_route(self, target_point):
        pass

    def drive_to_point(self, point):
        pass

    def update_data(self, *kwargs):
        self.all_robots_position = kwargs['positions']


class SimpleDTPSteeringStrategy(AbstractDTPSteeringStrategy):

    def __init__(self, motor_driver):
        self.all_robots_position = None
        self.motor_driver = motor_driver

    def drive_to_point(self, point):
        pass

    def update_data(self, **kwargs):
        self.all_robots_position = kwargs['positions']
