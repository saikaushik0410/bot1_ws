#!/usr/bin/env python

from __future__ import print_function

import roslib
import rospy

from geometry_msgs.msg import Twist

import sys, select, termios, tty

msg = """
XXXXXXXXReading from the keyboard and Publishing to command topic.
--------------------------------------------------------
Moving around:
		w
	a	s	d
		x

w,s for forward and backward motion
a,d for turning left and right
CTRL+C to quit
"""

moveBindings = {
	'w':(2.0,0.0),
	'a':(0.0,4.0),
	's':(-2.0,0.0),
	'd':(0.0,-4.0),
	'x':(0.0,0.0),
	}

def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key

if __name__=="__main__":
	settings = termios.tcgetattr(sys.stdin)

	pub = rospy.Publisher('bot_drive_controller/cmd_vel',Twist, queue_size = 1)
	rospy.init_node('teleop_command_keyboard')

	try:
		print(msg)
		while(1):
			key = getKey()
			lin_x = moveBindings[key][0]
			lin_y = 0
			lin_z = 0
			ang_x = 0
			ang_y = 0
			ang_z = moveBindings[key][1]

			twist = Twist()
			twist.linear.x = lin_x
			twist.linear.y = lin_y
			twist.linear.z = lin_z
			twist.angular.x = ang_x
			twist.angular.y = ang_y
			twist.angular.z = ang_z
			pub.publish(twist)

	except Exception as e:
		print(e)

	finally:
		twist = Twist()
		twist.linear.x = 0
		twist.linear.y = 0
		twist.linear.z = 0
		twist.angular.x = 0
		twist.angular.y = 0
		twist.angular.z = 0
		pub.publish(twist)

termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
