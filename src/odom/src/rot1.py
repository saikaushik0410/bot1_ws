#! /usr/bin/env python

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(15,GPIO.IN)
GPIO.setup(18,GPIO.IN)

count = 0

print ("waiting for edge")
print ("C1_before =" + str(GPIO.input(15)))
channel = GPIO.wait_for_edge(15,GPIO.RISING,timeout=5000)
print ("C1_after =" + str(GPIO.input(15)))
if channel is None:
    print ("edge not detected")

print ("C2 =" + str(GPIO.input(18)))
if GPIO.input(18):
    count += 1
else:
    count -= 1
print (count)
