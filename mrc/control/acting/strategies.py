from mrc.control.acting.abstract import AbstractStrategy
from mrc.control.movement_prediction.target_position_calculator import TargetPositionCalculator
from mrc.control.steering.exceptions import ObstacleOnTheWayException, SteeringException
from mrc.shared.position import PolarPosition


class FollowMasterStrategy(AbstractStrategy):

    def __init__(self, steering_strategy, locator, configurator):
        self.steering_strategy = steering_strategy
        self.locator = locator
        self.configurator = configurator
        self.position_calculator = TargetPositionCalculator(self.configurator)
        self.locations = None
        self.current_step = (0, 0)
        self.step_reached = True
        self.driving = False

    def read(self):
        if self.step_reached:
            self.locations = self.locator.get_locations(None)
            master_position = self.locator.get_locations(self.configurator.master_unit)
            self.current_step = self.position_calculator.calculate_actual_target_position(master_position,
                                                                                          self.current_step)

    def think(self):
        if PolarPosition.are_positions_approximately_same(self.current_step, (0, 0)):
            self.step_reached = True
        else:
            self.step_reached = False

    def act(self):
        if not self.step_reached and not self.driving:
            try:
                self.steering_strategy.drive_to_point(self.current_step)
                self.driving = True
            except ObstacleOnTheWayException as ootwe:
                print(ootwe.message)
                self.driving = False
            except SteeringException:
                print("Something went wrong")  # TODO: Add logger to whole project
                self.driving = False
        elif self.step_reached and self.driving:
            self.driving = False
        else:  # We did not reach the step and still driving
            print("Pyr pyr.")
