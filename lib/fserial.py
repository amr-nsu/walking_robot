import serial
import time
import os

class SerialDevice:

    def __init__(self, device, baud):
        self.serial = serial.Serial(device, baud, timeout=1)

    def send_request(self, n, angle):
        angle = angle*11.1 + 500
        request = "#%sP%sT500\n" %(n, int(angle))
        self.serial.write(request)


