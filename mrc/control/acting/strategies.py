from mrc.control.acting.abstract import AbstractStrategy
from mrc.control.movement_prediction.target_position_calculator import TargetPositionCalculator
from mrc.control.steering.exceptions import ObstacleOnTheWayException, SteeringException
from mrc.shared.position import PolarPosition


class FollowMasterStrategy(AbstractStrategy):

    def __init__(self, steering_interface, locator, configurator):
        self.steering_interface = steering_interface
        self.locator = locator
        self.configurator = configurator
        self.position_calculator = TargetPositionCalculator(self.configurator)
        self.locations = None
        self.current_step = (0, 0)
        self.step_reached = True

    def read(self):
        self.locations = self.locator.get_locations(None)
        if self.step_reached:
            master_position = self.locator.get_locations(self.configurator.master_unit)
            self.current_step = self.position_calculator.calculate_actual_target_position(master_position,
                                                                                          self.current_step)

    def think(self):
        if PolarPosition.are_positions_approximately_same(self.current_step, (0, 0)):
            self.step_reached = True
        else:
            self.step_reached = False

    def act(self):
        if not self.step_reached:
            try:
                self.steering_interface.update_data(locations=self.locations, master=self.configurator.master_unit)
                self.steering_interface.drive_to_point(self.current_step)
                self.current_step = (0, 0)
            except ObstacleOnTheWayException as ootwe:
                print(ootwe.message)
            except SteeringException:
                print("Something went wrong")  # TODO: Add logger to whole project
        elif self.step_reached:
            print("Dojechalem")
        else:  # We did not reach the step and still driving
            print("Pyr pyr.")
