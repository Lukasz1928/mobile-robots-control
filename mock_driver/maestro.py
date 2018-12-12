import re
import os
import serial
from sys import version_info

PY2 = version_info[0] == 2


class Controller:
    def __init__(self,device=0x0c):
        self.ttyStr = Controller.findTty()
        self.usb = serial.Serial(self.ttyStr)
        self.PololuCmd = chr(0xaa) + chr(device)
        self.Targets = [0] * 24
        self.Mins = [0] * 24
        self.Maxs = [0] * 24

    @staticmethod
    def findTty():
        _list = os.listdir('/dev')
        amcs = list(filter(lambda x: re.match('ttyACM*', x), _list))
        amcs.sort()
        print(amcs)
        return '/dev/' + amcs[0]

    def close(self):
        self.usb.close()

    def sendCmd(self, cmd):
        cmdStr = self.PololuCmd + cmd
        if PY2:
            self.usb.write(cmdStr)
        else:
            self.usb.write(bytes(cmdStr,'latin-1'))

    def setTarget(self, chan, target):
        if self.Mins[chan] > 0 and target < self.Mins[chan]:
            target = self.Mins[chan]
        if 0 < self.Maxs[chan] < target:
            target = self.Maxs[chan]

        lsb = target & 0x7f
        msb = (target >> 7) & 0x7f
        cmd = chr(0x04) + chr(chan) + chr(lsb) + chr(msb)
        self.sendCmd(cmd)
        self.Targets[chan] = target

    def setSpeed(self, chan, speed):
        lsb = speed & 0x7f
        msb = (speed >> 7) & 0x7f
        cmd = chr(0x07) + chr(chan) + chr(lsb) + chr(msb)
        self.sendCmd(cmd)

    def setAccel(self, chan, accel):
        lsb = accel & 0x7f
        msb = (accel >> 7) & 0x7f
        cmd = chr(0x09) + chr(chan) + chr(lsb) + chr(msb)
        self.sendCmd(cmd)

    def getPosition(self, chan):
        cmd = chr(0x10) + chr(chan)
        self.sendCmd(cmd)
        lsb = ord(self.usb.read())
        msb = ord(self.usb.read())
        return (msb << 8) + lsb

    def isMoving(self, chan):
        if self.Targets[chan] > 0:
            if self.getPosition(chan) != self.Targets[chan]:
                return True
        return False

    def getMovingState(self):
        cmd = chr(0x13)
        self.sendCmd(cmd)
        if self.usb.read() == chr(0):
            return False
        else:
            return True

    def runScriptSub(self, subNumber):
        cmd = chr(0x27) + chr(subNumber)
        # can pass a param with command 0x28
        # cmd = chr(0x28) + chr(subNumber) + chr(lsb) + chr(msb)
        self.sendCmd(cmd)

    def stopScript(self):
        cmd = chr(0x24)
        self.sendCmd(cmd)

