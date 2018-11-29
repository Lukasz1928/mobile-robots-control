from random import random

from mrc.control.acting.abstract import AbstractStrategy
from mrc.control.steering.exceptions import ObstacleOnTheWayException, SteeringException


class FollowMasterStrategy(AbstractStrategy):

    def __init__(self, steering_strategy, locator, configurator):
        self.steering_strategy = steering_strategy
        self.locator = locator
        self.configurator = configurator

        self.locations = None
        self.target_position = None
        self.position_reached = False

    def read(self):
        self.locations = self.locator.get_locations()
        self.target_position = self.configurator.target_position

    def think(self):
        x = random.choice([True, False])
        if x:  # TODO : getPositionFromMichal is not reached
            self.position_reached = False
            self.target_position = 5  # TODO: getFromMichal
        else:
            self.position_reached = True
            self.target_position = 3

    def act(self):
        if not self.position_reached:
            try:
                self.steering_strategy.drive_to_point(self.target_position)
            except ObstacleOnTheWayException as ootwe:
                print(ootwe.message)
            except SteeringException:
                print("Nie da sie")
        else:
            print("Pojechalem jak szalony rozjezdzajac wszystko po drodze")
