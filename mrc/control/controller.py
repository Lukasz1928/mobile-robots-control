from threading import Thread


class Controller(Thread):
    def __init__(self, locator, configurator, acting_strategy):
        super().__init__()
        self.locator = locator
        self.configurator = configurator
        self.running = False
        self.acting_strategy = acting_strategy

    def run(self):
        self.running = True
        while self.running:
            self.acting_strategy.read()
            self.acting_strategy.think()
            self.acting_strategy.act()

    def is_running(self):
        return self.running

    def stop(self):
        self.running = False
