class SteeringException(Exception):
    pass


class ObstacleOnTheWayException(SteeringException):
    """Raised in Careful Strategy when there is another robot in the robot path"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)
