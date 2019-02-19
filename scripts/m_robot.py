#!/usr/bin/env python
import math
import numpy as np
import subprocess
import rospy
import os
import time
import requests 
from geometry_msgs.msg import ( PoseStamped, PoseWithCovarianceStamped,
                                PoseArray, Quaternion )
from actionlib_msgs.msg import GoalStatusArray
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import places as places


class Robot(object):

    status = [  "PENDING", "ACTIVE", 
                "PREEMPTED", "SUCCEEDED", 
                "ABORTED", "REJECTED", 
                "PREEMPTING", "RECALLING", 
                "RECALLED", "LOST"]
    PENDING = 0
    ACTIVE = 1
    PREEMPTED = 2
    SUCCEEDED = 3
    ABORTED = 4
    REJECTED = 5
    PREEMPTING = 6
    RECALLING = 7
    RECALLED = 8
    LOST = 9

    def __init__(self):

        self.mname = "[ROBOTCORE] "
        self.initial_pose = places.initialpose
        self.current_pose = None
        self.status = None

        self.pose_publisher = rospy.Publisher("/initialpose", PoseWithCovarianceStamped, queue_size=10)
        self.goal_publisher = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size = 10)
        self.status_subscriber = rospy.Subscriber("/move_base/status", GoalStatusArray, self.status_callback,queue_size=1)

        time.sleep(1)
        
        
    def intialize_robot(self):     
        #set the initial pose of the robot
        self.pose_publisher.publish(self.initial_pose)

        
    def status_callback(self,status):
        self.status = status
        
    def get_status(self):
        if self.status != None and len(self.status.status_list) > 0:
            return int(self.status.status_list[-1].status)
        return self.ABORTED
    
    def go_to_location(self, location):
        def set_goal():
            os.system('rosservice call /move_base/clear_costmaps \"{}\"')
            time.sleep(0.5)
            self.goal_publisher.publish(location)

        print(self.mname + "Departure - publishing to NavStack")
        set_goal()
        time.sleep(2)
        order_status = self.get_status()
        
        counter = 0

        while order_status != self.SUCCEEDED:
            if order_status == self.ABORTED:
                print(self.mname + "Unreachable location. Retrying.")
                set_goal()
            elif order_status != self.ACTIVE:
                print "Order status: " + str(order_status)
            counter += 1
            if counter == 20:
                counter = 0
                set_goal()
            time.sleep(0.2)
            order_status = self.get_status()
            pass
        print(self.mname + "Arrival")
