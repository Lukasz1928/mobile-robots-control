import math

class iterableClass(type):
    def __iter__(self):
        return self.get_iterator()

    def __getitem__(self, item):
        return self.get_item(item)


class projections(metaclass=iterableClass):

    class equidistant:
        @staticmethod
        def radius(theta, focal):
            return theta * focal

        @staticmethod
        def focal(radius, theta):
            return radius / theta

        @staticmethod
        def theta(radius, focal):
            return radius / focal

    class stereographic:
        @staticmethod
        def radius(theta, focal):
            return 2.0 * focal * math.tan(theta / 2.0)

        @staticmethod
        def focal(radius, theta):
            return radius / (2.0 * math.tan(theta / 2.0))

        @staticmethod
        def theta(radius, focal):
            return 2.0 * math.atan(radius / (2.0 * focal))

    class ortographic:
        @staticmethod
        def radius(theta, focal):
            return focal * math.sin(theta)

        @staticmethod
        def focal(radius, theta):
            return radius / math.sin(theta)

        @staticmethod
        def theta(radius, focal):
            return math.asin(radius / focal)

    class equisolid:
        @staticmethod
        def radius(theta, focal):
            return 2.0 * focal * math.sin(theta / 2.0)

        @staticmethod
        def focal(radius, theta):
            return radius / (2.0 * math.sin(theta / 2.0))

        @staticmethod
        def theta(radius, focal):
            return 2.0 * math.asin(radius / (2.0 * focal))

    _projections = [equidistant, stereographic, ortographic, equisolid]

    @classmethod
    def get_iterator(cls):
        return iter(cls._projections)

    @classmethod
    def get_item(cls, item):
        return cls._projections[item]