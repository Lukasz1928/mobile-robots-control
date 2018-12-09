from threading import Thread


class Controller(Thread):
    """
    Main robot control thread class.
    """
    def __init__(self, locator, configurator, acting_strategy):
        """
        Parameters
        ----------
        locator : mrc.localization.locator.Locator
            Main localization class, based on which output robot will act
        configurator : mrc.configuration.configurator.Configurator
            Robot configuration container
        acting_strategy : mrc.control.acting.abstract.AbstractStrategy
            Strategy in according to which robot will act
        """
        super().__init__()
        self._locator = locator
        self._configurator = configurator
        self._running = False
        self._acting_strategy = acting_strategy

    def run(self):
        """
        Thread main loop.

        While thread is working, in each iteration it calls acting strategy methods in order:
            1. read
            2. think
            3. act
        """
        self._running = True
        while self._running:
            self._acting_strategy.read()
            self._acting_strategy.think()
            self._acting_strategy.act()

    def is_running(self):
        """
        Get state of thread

        Returns
        -------
        bool
            Information about thread running currently
        """
        return self._running

    def stop(self):
        """
        Finish work of thread
        """
        self._running = False
