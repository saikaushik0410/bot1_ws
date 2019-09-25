#!/usr/bin/env python

import sys
import RPi.GPIO as GPIO
import time
import rospy
from sensor_msgs.msg import LaserScan

rospy.init_node('laser_scan_publisher')

scan_pub = rospy.Publisher('scan', LaserScan, queue_size=50)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

TRIG = 16
ECHO = 18
servo = 03

GPIO.setup(servo,GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

pwm = GPIO.PWM(servo, 50)
GPIO.output(TRIG, False)

print "Waiting for sensor to settle"
time.sleep(2)

pwm.start(5)
print "Starting"

num_readings = 60

count = 0
PI = 3.14

try:
	while not rospy.is_shutdown():
		current_time = rospy.Time.now()

		scan = LaserScan()

		scan.header.stamp = current_time
		scan.header.frame_id = 'laser_frame'
		scan.angle_min = 0
		scan.angle_max = PI
		scan.angle_increment = PI / num_readings
		scan.time_increment = 0.2
		scan.range_min = 0.0
		scan.range_max = 200.0

		scan.ranges = []
		scan.intensities = []

		angle_min = (180/PI) * scan.angle_min
		angle_max = (180/PI) * scan.angle_max
		angle_increment = (180/PI) * scan.angle_increment

		while count<1:
			count = count + 1
			for angle in range (int(angle_min),int(angle_max + 1),int(angle_increment)):
	        		duty = float(angle)/20 + 2
        			pwm.ChangeDutyCycle(duty)
	        		time.sleep(0.2)
				print (angle)

				now = time.time()
				GPIO.output(TRIG, True)
				time.sleep(0.00001)
				GPIO.output(TRIG, False)

				while GPIO.input(ECHO) == 0:
        				pulse_start = time.time()

				while GPIO.input(ECHO) == 1:
			        	pulse_end = time.time()

				pulse_duration = pulse_end - pulse_start

				distance = pulse_duration * 17150

				distance = round(distance, 1)

				scan.ranges.append(distance)
				scan_pub.publish(scan)

		duty = 1.0/20 + 2
		pwm.ChangeDutyCycle(duty)
		time.sleep(1)

		pwm.stop()
		GPIO.cleanup()
except:
	sys.exit()
