import serial
import time
import os
import rospy
from std_msgs.msg import String

class Driver:

    def __init__(self, device, baud):
        self.serial = serial.Serial(device, baud, timeout=1)
        rospy.Subscriber("/robot/motor", String, self.motor_callback)

    def send_request(self, n, angle):
        angle = angle*11.1 + 500
        request = "#%sP%sT600\n" %(n, int(angle))
        print request
        self.serial.write(request)

    def motor_callback(self, data):
        q = data.data.split('&')       
        n = int(q[0][2:])
        a = int(q[1][2:])
        print n, a
        self.send_request(n, a)

if __name__ == '__main__':
    rospy.init_node('driver')
    driver = Driver('/dev/ttyUSB0', 9600)
    rospy.spin()


