#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

import RPi.GPIO as GPIO

# set GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

_FREQUENCY = 20


def _clip(value, minimum, maximum):
    if value < minimum:
        return minimum
    elif value > maximum:
        return maximum
    return value


class Motor:
    def __init__(self, forward_pin, backward_pin):
        self.forward_pin = forward_pin
        self.backward_pin = backward_pin

        GPIO.setup(self.forward_pin, GPIO.OUT)
        GPIO.setup(self.backward_pin, GPIO.OUT)

        self.forward_pwm = GPIO.PWM(self.forward_pin,_FREQUENCY)
        self.backward_pwm = GPIO.PWM(self.backward_pin, _FREQUENCY)

    def move(self,speed_percent):
        speed = _clip(abs(speed_percent),0,100)

        if speed_percent<0:
            self.backward_pwm.start(speed)
            self.forward_pwm.start(0)
        else:
            self.forward_pwm.start(speed)
            self.backward_pwm.start(0)

class Driver:
    def __init__(self):
        rospy.init_node('driver')

        self.last_received = rospy.get_time()
        self.timeout = rospy.get_param('~timeout', 2)
        self.rate = rospy.get_param('~rate', 10)
        self.max_speed = rospy.get_param('~max_speed',0.5)
        self.wheel_base = rospy.get_param('~wheel_base',0.09)

        self.left_motor = Motor(10,9)
        self.right_motor = Motor(8,7)
        self.left_speed_percent = 0
        self.right_speed_percent = 0

        rospy.Subscriber('bot_drive_controller/cmd_vel',Twist,self.velocity_received_callback)

    def velocity_received_callback(self,msg):
        self.last_received = rospy.get_time()

        linear = msg.linear.x
        angular= msg.angular.z

        left_speed = linear - angular*self.wheel_base/2
        right_speed = linear + angular*self.wheel_base/2

        self.left_speed_percent = (100*left_speed/self.max_speed)
        self.right_speed_percent = (100 * right_speed / self.max_speed)

    def run(self):
	rate = rospy.Rate(self.rate)

        while not rospy.is_shutdown():
            delay = rospy.get_time() - self.last_received
            if delay < self.timeout:
                self.left_motor.move(self.left_speed_percent)
                self.right_motor.move(self.right_speed_percent)
            else:
                self.left_motor.move(0)
                self.right_motor.move(0)

            rate.sleep()

def main():
    driver = Driver()
    driver.run()

if __name__ == '__main__':
    main()
