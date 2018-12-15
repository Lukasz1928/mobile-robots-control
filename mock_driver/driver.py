import time
import mock_driver.drive as drive
import mock_driver.maestro as maestro


class Driver:

    def __init__(self):
        self.m = maestro.Controller()
        self.driver = drive.ServoController(self.m, 0, 1)
        self.rotation_speed = 0.5
        self.drive_speed = 0.5

    def rotate(self, angle):
        if angle >= 0:
            self.driver.drive(-self.rotation_speed, self.rotation_speed)
        else:
            self.driver.drive(self.rotation_speed, -self.rotation_speed)

        time.sleep(self._calculate_sleep_time_for_rotation(angle))
        self.driver.drive(0, 0)

    def _calculate_sleep_time_for_rotation(self, angle):
        angle = abs(angle)
        if angle < 3.1415 / 2:
            return max(0.75 * angle / 3.1415 - 0.05, 0)
        else:
            return max(0.7 * angle / 3.1415, 0)

    def _calculate_sleep_time_for_drive(self, distance):
        return max(distance / 30.0, 0)

    def drive(self, distance):
        self.driver.drive(self.drive_speed, self.drive_speed)
        time.sleep(self._calculate_sleep_time_for_drive(distance))
        self.driver.drive(0, 0)

    def drive_to_point(self, radius, angle):
        self.rotate(angle)
        self.drive(radius)
