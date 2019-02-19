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

default = poseMaker(-2.5475525856, -2.34635090828, 0.752833499146, 0.658211001552)
initialpose = poseCovMaker(-2.5475525856, -2.34635090828, 0.752833499146, 0.658211001552)
items = poseMaker(4.15583992004, -1.13486647606, -0.665280425926, 0.746593567398)

table1 = poseMaker(-5.98257446289,-0.700616967678, 0.712800185632, 0.701367161594)
table2 = poseMaker(-2.95339369774, -0.689374160767, 0.712755210782, 0.701412866651)
table3 = poseMaker( 0.0413001403213, -0.245340591669, 0.730257059437, 0.683172472472)
table4 = poseMaker(2.92179298401, -0.2637598931789, 0.737209381793, 0.675664360017)
table5 = poseMaker(6.00674962997, 0.512006092072, 0.752844299097, 0.658198648826)


tables = { "Table 1":table1, "Table 2":table2, "Table 3":table3, "Table 4":table4, "Table 5":table5 }
