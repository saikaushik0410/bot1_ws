#! /usr/bin/env python

import rospy
import tf
from geometry_msgs.msg import Quaternion,TransformStamped
import numpy as np
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose2D

rospy.init_node('odometry_publisher')

class Main:
    def __init__(self):
        self.odom_pub = rospy.Publisher('odom', Odometry, queue_size=50)
        self.odom_boradcaster = tf.TransformBroadcaster
        rospy.Subscriber('encoder', Pose2D, self.callback)

        self.x = 0
        self.y = 0
        self.th = 0
        rospy.Rate(10)
        self.last_time = rospy.Time.now()

        self.odom_quat = Quaternion
        self.odom_trans = TransformStamped
        self.odom = Odometry



    def spin(self):
        rospy.spin()
        self.current_time = rospy.Time.now()
        self.dt = (self.current_time - self.last_time)
        self.delta_x = (self.vx * np.cos(self.th)) * self.dt
        self.delta_y = self.vx * np.sin(self.th) * self.dt
        self.delta_th = self.vth * self.dt

        self.x += self.delta_x
        self.y += self.delta_y
        self.th += self.delta_th

    def odom_transmit(self):
        self.odom_quat = tf.transformations.quaternion_from_euler(0, 0, self.th)
        self.odom_trans.header.stamp = self.current_time
        self.odom_trans.header.frame_id = "odom"
        self.odom_trans.child_frame_id = "base_link"

        self.odom_trans.transform.translation.x = self.x
        self.odom_trans.transform.translation.y = self.y
        self.odom_trans.transform.translation.x = 0
        self.odom_trans.transform.rotation = self.odom_quat

        self.odom_boradcaster.sendTransform(self.odom_trans)

    def odom_to_ROS(self):
        self.odom.header.stamp = self.current_time
        self.odom.header.frame_id = "odom"

        self.odom.pose.pose.position.x = self.x
        self.odom.pose.pose.position.y = self.y
        self.odom.pose.pose.position.z = 0
        self.odom.pose.pose.orientation = self.odom_quat

        self.odom.child_frame_id = "base_link"
        self.odom.twist.twist.linear.x = self.vx
        self.odom.twist.twist.angular.z = self.vth

        self.odom_pub.publish(self.odom)

        self.last_time = self.current_time
        rospy.sleep()

    def callback(self,msg):
        self.vx = msg.x
        self.vth = msg.theta


def final():
    main = Main()
    main.spin()
    main.odom_transmit()
    main.odom_to_ROS()


if __name__ == "__main__":
    final()

