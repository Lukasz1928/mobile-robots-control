import logging

from mrc.control.steering.abstract import AbstractDTPSteeringInterface
from mrc.shared.exceptions.exceptions import ObstacleOnTheWayException


class CarefulDTPSteeringInterface(AbstractDTPSteeringInterface):
    """
    Implementation of steering interface.

    In this one, robot won't move if it finds another one in its way to target.
    """

    def __init__(self, motor_driver, angle_offset=0.39):
        """
        Parameters
        ----------
        motor_driver
            Motor controller interface.
            It has to provide method drive_to_point(float, float), where first field is distance, second field is angle.
        angle_offset : float, optional
            Absolute angle range in which we seek for obstacle units and not move if such are found.
        """
        self.master = None
        self.all_robots_position = None
        self.motor_driver = motor_driver
        self.angle_offset = angle_offset
        self._logger = logging.getLogger(__name__)

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
        """
        Implemented unit movement to specified point

        Parameters
        ----------
        point : (float, float)
            Target position.
            First field is distance, second field is angle.
        """
        sth_in_route, names = self._in_route(point)
        if sth_in_route:
            raise ObstacleOnTheWayException("The path is blocked by robots: " + str(names))
        else:
            self._logger.debug("Target point: {}".format(point))
            self.motor_driver.drive_to_point(*point)

    def update_data(self, locations, master):
        """
        Update information about environment in the steering interface.

        Parameters
        ----------
        locations : dict
            Robot id mapped to their position
        master
            Id of unit we're supposed to follow
        """
        self.all_robots_position = locations
        self.master = master


class SimpleDTPSteeringInterface(AbstractDTPSteeringInterface):
    """
    Implementation of steering interface.

    In this one, robot will always move towards the target position.
    """

    def __init__(self, motor_driver):
        """
        Parameters
        ----------
        motor_driver
            Motor controller interface.
            It has to provide method drive_to_point(float, float), where first field is distance, second field is angle.
        """
        self.motor_driver = motor_driver
        self._logger = logging.getLogger(__name__)

    def drive_to_point(self, point):
        """
        Implemented unit movement to specified point

        Parameters
        ----------
        point : (float, float)
            Target position.
            First field is distance, second field is angle.
        """
        self._logger.debug("Target point: {}".format(point))
        self.motor_driver.drive_to_point(*point)

    def update_data(self, locations, master):
        """
        Empty implementation, needed for compatibility.

        Parameters
        ----------
        locations
            Unused, needed for compatibility
        master
            Unused, needed for compatibility
        """
        pass
