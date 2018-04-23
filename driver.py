import serial

import rospy
from std_msgs.msg import String


class Driver:

    def __init__(self, device, baud):
        self.serial = serial.Serial(device, baud, timeout=1)
        rospy.Subscriber("/robot/motor", String, self.motor_callback)

    def motor_callback(self, data):
        q = data.data.split('&')
        n = int(q[0][2:])
        a = int(q[1][2:])
        self.motor_control(n, a)

    def motor_control(self, n, angle):
        def angle_to_pwm(angle):
            return int(angle * 11.1 + 500)

        request = "#%sP%sT600\n" % (n, angle_to_pwm(angle))
        self.serial.write(request)
        rospy.loginfo(request)


if __name__ == '__main__':
    rospy.init_node('driver')
    driver = Driver('/dev/ttyUSB0', 9600)
    rospy.spin()
