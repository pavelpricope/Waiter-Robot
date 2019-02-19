#!/usr/bin/env python
import math
import numpy as np
import subprocess
import rospy
import time
import requests


import m_sight as m_sight
import m_behavior
import m_robot
import m_orders
import m_database
import m_speech
import m_hearing as m_hearing

class RobotMain(object):

    def __init__(self):
        rospy.init_node("beer_bot")
        self.sight = m_sight.Sight()
        self.robot = m_robot.Robot()
        self.database = m_database.Database()
        self.orders = m_orders.Orders(self.database)
        self.speech = m_speech.Speech()
        self.hearing = m_hearing.Hearing(self.speech)
        self.behavior = m_behavior.Behavior(self.sight, self.robot, self.orders, self.database, self.speech, self.hearing)
        self.robot.intialize_robot()
        self.behavior.update_stock()

    def run(self):
        print("Looping...")

        order = self.orders.get_next_order()
        print("Order: " + str(order))
        if order != None:
            self.behavior.execute_order(order)
            return
        
        refill = self.orders.get_next_refill() 
        print("Refill: " + str(refill))
        if refill != None:
            self.behavior.ask_refill(refill)
            return

        self.behavior.wander_around()



def looper(func, freq = 1):
    rate_interval = rospy.Rate(freq)
    while not rospy.is_shutdown():
        func()
        rate_interval.sleep()


if __name__ == "__main__":
    looper(RobotMain().run)
