#!/usr/bin/env python
import time
import rospy
from geometry_msgs.msg import ( PoseStamped, PoseWithCovarianceStamped,
                                PoseArray, Quaternion )

# Set default initial pose to initial position and orientation.

def poseCovMaker(x,y,z,w):
	pose =  PoseWithCovarianceStamped()
	pose.pose.pose.position.x = x
	pose.pose.pose.position.y = y
	pose.pose.pose.position.z = 0
	pose.pose.pose.orientation.x = 0
	pose.pose.pose.orientation.y = 0
	pose.pose.pose.orientation.z = z
	pose.pose.pose.orientation.w = w
	pose.header.stamp.secs = time.time()
	pose.header.frame_id = "map"
	return pose

def poseMaker(x,y,z,w):
	pose =  PoseStamped()
	pose.pose.position.x = x
	pose.pose.position.y = y
	pose.pose.position.z = 0
	pose.pose.orientation.x = 0
	pose.pose.orientation.y = 0
	pose.pose.orientation.z = z
	pose.pose.orientation.w = w
	pose.header.stamp.secs = time.time()
	pose.header.frame_id = "map"
	return pose

default = poseMaker(12, 15, -0.44, 0.89)
initialpose = poseCovMaker(12, 15, -0.44, 0.89)
items = poseMaker(11, 11, 0.88, 0.47)

table1 = poseMaker(21,20, -0.48, 0.87)
table2 = poseMaker(18,18,-0.48, 0.87)
table3 = poseMaker( 15,16, -0.48, 0.87)
table4 = poseMaker(11,13, -0.48, 0.87)
table5 = poseMaker(9, 11,-0.48, 0.87)


tables = { "Table 1":table1, "Table 2":table2, "Table 3":table3, "Table 4":table4, "Table 5":table5 }
