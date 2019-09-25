#!/usr/bin/env python

import sys
import RPi.GPIO as GPIO
import time
import rospy
from std_msgs.msg import String

rospy.init_node('Encoder_input_value')

Encoder = rospy.Publisher('value',String, queue_size=50)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

C1 = 15
C2 = 18

GPIO.setup(C1, GPIO.IN)
GPIO.setup(C2, GPIO.IN)

aLastState = GPIO.input(C1)

value = 0

while not rospy.is_shutdown():
    aState = GPIO.input(C1)
    if aState != aLastState:
        if GPIO.input(C2) != aState:
            value += 1
        else:
            value -= 1
        print("Position:" + str(value))
        Encoder.publish(str(value))
    aLastState = aState
