import logging

from mrc.control.acting.abstract import AbstractStrategy
from mrc.control.movement_prediction.target_position_calculator import TargetPositionCalculator
from mrc.shared.exceptions.exceptions import ObstacleOnTheWayException, SteeringException
from mrc.shared.position import PolarPosition


class FollowMasterStrategy(AbstractStrategy):
    """
    Implementation of robot behavior.

    In this one, the robot is supposed to follow master in position specified in configuration.
    """

    def __init__(self, steering_interface, locator, configurator):
        """
        Parameters
        ----------
        steering_interface : mrc.control.steering.abstract.AbstractDTPSteeringInterface
            Robot steering interface, responsible for moving unit to received target place.
        locator : mrc.localization.locator.Locator
            Main localization class, responsible for reading the info about environment.
        configurator : mrc.configuration.configurator.Configurator
            Robot configuration container.
        """
        self._steering_interface = steering_interface
        self._locator = locator
        self._configurator = configurator
        self._position_calculator = TargetPositionCalculator(self._configurator)
        self._locations = {}
        self._current_step = (0, 0)
        self._step_reached = True
        self._logger = logging.getLogger(__name__)

    def read(self):
        """
        Method reading environment state.
        """
        self._logger.debug("Read phase")
        # self._locations = self._locator.update_and_get_locations()
        if self._step_reached:
            master_position = self._locator.get_locations(self._configurator.master_unit)
            if master_position is None:
                print("I have no master")
            else:
                self._current_step = self._position_calculator.calculate_actual_target_position(master_position,
                                                                                                self._current_step)

    def think(self):
        """
        Method processing environment state.
        """
        self._logger.debug("Think phase")
        if PolarPosition.are_positions_approximately_same(self._current_step, (0, 0)):
            self._step_reached = True
        else:
            self._step_reached = False

    def act(self):
        """
        Method issuing movement commands according to environment state.
        """
        self._logger.debug("Act phase")
        if not self._step_reached:
            self._logger.debug("Current step: {}".format(self._current_step))
            try:
                self._steering_interface.update_data(locations=self._locations, master=self._configurator.master_unit)
                self._steering_interface.drive_to_point(self._current_step)
                self._current_step = (0, 0)
            except ObstacleOnTheWayException as ootwe:
                self._logger.warning(str(ootwe))
            except SteeringException:
                self._logger.error("Steering error occured")
        elif self._step_reached:
            self._logger.info("Step reached")
        else:  # We did not reach the step and still driving
            self._logger.debug("Still going")
