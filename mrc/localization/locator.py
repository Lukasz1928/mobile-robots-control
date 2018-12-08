import threading
import time
from typing import Callable


class Locator(threading.Thread):
    """
    Main class in location package. Its responsible for providing information about robot locations.

    Attributes
    ----------
    interval : float
        Amount of seconds between measurements.
    """

    def __init__(self, robot_list: list, read_data: Callable, process_data: Callable = None, interval: float = 0.0):
        """
        Parameters
        ----------
        robot_list : list
            List of IDs of robots in environment.
        read_data : Callable
            Function taking no arguments returning raw robot location data.
        process_data : Callable, optional
            Optional function that takes raw location data and returns processed data.
            If None, the `read_data` output will be treated as final localization data.
        interval : float
            Amount of seconds between measurements.
        """
        threading.Thread.__init__(self)
        self._locations = {robot_id: None for robot_id in robot_list}
        self._read_data = read_data
        self._process_data = process_data
        self.interval = interval
        self._running = False

    def run(self):
        """
        Main thread loop function
        """
        self._running = True
        while self._running:
            self._update_locations()
            time.sleep(self.interval)

    def update_and_get_locations(self, robot_id=None):
        """
        Force update locations and return results

        Parameters
        ----------
        robot_id : Any, optional
            If specified, function will return only location of robot with that id.
            If None, function will return all robot locations.

        Returns
        -------
        dict
            Locations of all robots in environment, if robot_id = None
        float, float
            Location of specified robot, if robot_id is not None.
        """
        if not self.is_running():
            self._update_locations()
        return self.get_locations(robot_id)

    def _update_locations(self):
        raw_data = self._read_data()
        processed_data = self._process_data(raw_data) if self._process_data is not None else raw_data
        self._locations = processed_data

    def get_locations(self, robot_id=None):
        """
        Return locations of robots

        Parameters
        ----------
        robot_id : Any, optional
            If specified, function will return only location of robot with that id.
            If None, function will return all robot locations.

        Returns
        -------
        dict
            Locations of all robots in environment, if robot_id = None
        float, float
            Location of specified robot, if robot_id is not None.
        """
        return self._locations[robot_id] if robot_id is not None else self._locations

    def stop(self):
        """
        Stop running locator thread
        """
        self._running = False

    def is_running(self):
        """
        Return info if locator thread is currently running

        Returns
        -------
        bool
            Info if locator thread is currently running
        """
        return self._running

    def add_robot(self, robot_id):
        """
        Add new robot to search for in environment

        Parameters
        ----------
        robot_id : Any
            Id of new robot
        """
        if robot_id not in self._locations.keys():
            self._locations[robot_id] = None

    def remove_robot(self, robot_id):
        """
        Remove robot from search

        Parameters
        ----------
        robot_id : Any
            Id of robot to delete
        """
        if robot_id in self._locations.keys():
            del self._locations[robot_id]
