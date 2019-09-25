#! /usr/bin/env python
import numpy as np
import rospy
from geometry_msgs.msg import Pose2D
import RPi.GPIO as GPIO


class Odom:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        rospy.init_node('encoder')
        self.clicks = 0
        self.N = 2626
        self.pi = np.pi
        self.radius = 5
        self.distance_per_click = (self.pi * self.radius * 2)/self.N
        self.wheel_base = 15
        self.pub = rospy.Publisher('encoder', Pose2D, queue_size=10)
        self.bot = Pose2D()
        self.distance = 0
        self.left_distance = 0
        self.right_distance = 0
        self.rate = rospy.Rate(10)


    def pose(self):
        rate = rospy.Rate(10)
        self.left_distance = self.distance_of_wheel(15, 18)
        self.right_distance = self.distance_of_wheel(20, 21)
        print ("left =" + str(self.left_distance))
        print ("right = " + str(self.right_distance))
        print ("distance_per_C = " + str(self.distance_per_click))

        self.bot.x = (self.left_distance + self.right_distance) / 2
        self.bot.theta = (self.left_distance - self.right_distance) / self.wheel_base
        #print ("x =" + str(self.bot.x))
        #print ("theta = " + str(self.bot.theta))
        self.pub.publish(self.bot)
        rospy.spin()
        rate.sleep()

    def distance_of_wheel(self, C1, C2):
        GPIO.setup(C1, GPIO.IN)
        GPIO.setup(C2, GPIO.IN)
        aLastState = GPIO.input(C1)
        #print (rospy.is_shutdown())
        while not rospy.is_shutdown():
            aState = GPIO.input(C1)
            if aState != aLastState:
                print ("IN")
                if GPIO.input(C2) != aState:
                    self.clicks += 1
                else:
                    self.clicks -= 1
            aLastState = aState
                # print("Position:" + str(self.clicks))
                # encode.publish(self.clicks)
            self.distance = self.distance_per_click * self.clicks
            print ("dis = " + str(self.distance))
            return self.distance


def final():
    main = Odom()
    main.pose()


if __name__ == "__main__":
    final()

