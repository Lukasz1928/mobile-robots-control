import logging
import threading
import time

from mrc.localization.filtering.kalman import KalmanPredictor


class Locator(threading.Thread):
    """
    Main class in location package. Its responsible for providing information about robot locations.

    Attributes
    ----------
    interval : float
        Amount of seconds between measurements.
    """

    def __init__(self, robot_list, read_data, process_data=None, interval=0.0):
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
        self.predictors = {robot_id: KalmanPredictor() for robot_id in robot_list}
        self._running = False
        self._logger = logging.getLogger(__name__)

    def run(self):
        """
        Main thread loop function
        """
        self._logger.info("Locator started main loop")
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
        """
        Read image and make calculations to get robots positions
        """
        raw_data = self._read_data()
        processed_data = self._process_data(raw_data) if self._process_data is not None else raw_data
        if processed_data:
            for k, v in processed_data.items():
                if k in self._locations.keys():
                    self.predictors[k].update(*v)
                    self._locations[k] = v
            for k, v in self._locations.items():
                if k not in processed_data:
                    self._locations[k] = self.predictors[k].predict()
        else:
            self._locations = {k: self.predictors[k].predict() for k in self._locations.keys()}
        self._logger.debug("Locator updated locations")

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
        self._logger.info("Locator finished main loop")

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
            self.predictors[robot_id] = KalmanPredictor()
            self._logger.info("Robot {} added".format(str(robot_id)))

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
            del self.predictors[robot_id]
            self._logger.info("Robot {} removed".format(str(robot_id)))
