from mrc.control.acting.abstract import AbstractStrategy


class FollowMasterStrategy(AbstractStrategy):

    def __init__(self, steering_strategy, locator, configurator):
        self.steering_strategy = steering_strategy
        self.locator = locator
        self.configurator = configurator

        self.locations = None
        self.pos_to_go = None

    def read(self):
        self.locations = self.locator.get_locations()
        self.pos_to_go = self.configurator.target_position

    def think(self):
        # dla całej mapy if i jest masterem
        #   weź lokalizacja
        #   wyznacz wektor ruchu mastera
        #   oblicz pozycję docelową
        pass

    def act(self):
        pass
