from mrc.control.strategy.abstract import AbstractStrategy


class FollowMasterStrategy(AbstractStrategy):
    def read(self):
        # get locations
        #
        pass

    def think(self):
        # dla całej mapy if i jest masterem
        #   weź lokalizacja
        #   wyznacz wektor ruchu mastera
        #   oblicz pozycję docelową
        pass

    def act(self):
        pass
