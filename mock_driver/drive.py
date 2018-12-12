
class ServoController:

    def __init__(self, maestro, chLeft, chRight):
        self.maestro = maestro
        self.chLeft = chLeft
        self.chRight = chRight
        self.maestro.setAccel(chLeft,0)
        self.maestro.setAccel(chRight,0)
        self.maestro.setSpeed(chLeft, 60)
        self.maestro.setSpeed(chRight, 60)
        self.minL = 4000
        self.minR = 4000
        self.centerL = 6000
        self.centerR = 6000
        self.maxL = 8000
        self.maxR = 8000

    def _maestroScale(self, motorL, motorR):
        if (motorL >= 0) :
            l = int(self.centerL + (self.maxL - self.centerL) * motorL)
        else:
            l = int(self.centerL + (self.centerL - self.minL) * motorL)
        if (motorR >= 0) :
            r = int(self.centerR + (self.maxR - self.centerR) * motorR)
        else:
            r = int(self.centerR + (self.centerR - self.minR) * motorR)
        return (l, r)

    def drive(self, motorL, motorR):
        if motorL == 0 and motorR == 0:
            self.stop()
        else:
            (maestroL, maestroR) = self._maestroScale(-motorL, motorR)
            self.maestro.setTarget(self.chLeft, maestroL)
            self.maestro.setTarget(self.chRight, maestroR)

    def stop(self):
        self.maestro.setTarget(self.chLeft, 0)
        self.maestro.setTarget(self.chRight, 0)

    def close(self):
        self.stop()
