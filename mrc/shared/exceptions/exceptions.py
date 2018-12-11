from mrc.shared.exceptions.mrc_exception import MRCException


class IncorrectShapeException(MRCException):
    pass


class ColorEncodingNotSupportedException(MRCException):
    pass


class SteeringException(MRCException):
    pass


class ObstacleOnTheWayException(SteeringException):
    pass


class DataSizeException(MRCException):
    pass


class ParameterException(MRCException):
    pass
