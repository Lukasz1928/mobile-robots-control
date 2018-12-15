import math
import time

from mrc.configuration.configurator import Configurator
from mrc.control.acting.strategies import FollowMasterStrategy
from mrc.control.controller import Controller
from mrc.control.steering.interfaces import SimpleDTPSteeringInterface
from mrc.localization.calculator.location_calculator import LocationCalculator
from mrc.localization.camera.data_processor import FisheyeCameraDataProcessor
from mrc.localization.camera.reader import CameraReader
from mrc.localization.color.quick_mean.quick_mean import QuickMeanStrategy
from mrc.localization.locator import Locator
from mock_driver.driver import Driver

robots_list = ['red']
locator = Locator(robots_list, CameraReader(), FisheyeCameraDataProcessor(
    robots_list, QuickMeanStrategy(), LocationCalculator(
        (640, 480), 411, lambda x: 6*math.tan(math.pi * x)
    )
))
configurator = Configurator('red', (10, 0), 'yellow')
motor_driver = Driver()
acting_strategy = FollowMasterStrategy(SimpleDTPSteeringInterface(motor_driver), locator, configurator)
controller = Controller(locator, configurator, acting_strategy)

controller.run()
time.sleep(20)
controller.stop()