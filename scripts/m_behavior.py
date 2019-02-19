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

import places_stage as places
from order import Order


class Behavior(object):

    def __init__(self, sight, robot, orders, database, speech, hearing):
        self.sight = sight
        self.robot = robot
        self.orders = orders
        self.speech = speech
        self.hearing = hearing
        self.database = database
        self.mname = "[BEHAVIOR] "
        self.tables = places.tables.keys()
        self.table_index = 0

    def update_stock(self):
        self.robot.go_to_location(places.items)
        self.sight.recognize_objects()
        self.database.update_bottle_count(self.sight.count_stock())
    
    def update_people_at_table(self, table):
        self.sight.recognize_objects()
        people = self.sight.count_people()
        self.database.update_people_count(table, people)
        return people

    def wander_around(self):
        table = self.tables[self.table_index]
        self.table_index += 1 
        if self.table_index == len(self.tables):
            self.table_index = 0
        
        print(self.mname + "Wandering at " + table)
        self.robot.go_to_location(places.tables[table])
        
        if self.update_people_at_table(table) == 0:
            self.database.update_trash(table, self.sight.count_bottles())


    def execute_order(self, order):
        print(self.mname +"Order execution started for " + order.table + " of " + str(order.contents))
        # go and grab the items
        self.robot.go_to_location(places.items)

        self.speech.say("Please load me with " + str(order.contents[1]) + " " + order.contents[0])

        #say DONE?
        raw_input("Press enter when done")
        self.speech.beep()
        print(self.mname + "Items caught")
        # Bring the items to the table
        self.robot.go_to_location(places.tables[order.table])

        self.speech.say("Hello " + order.name + ", here is your " + order.contents[0])
        
        raw_input("Press enter when done")
        self.speech.beep()
        self.orders.did_complete(order)
        print(self.mname + "Order executed")  
        
        print(self.mname + "Counting people")

        people = self.update_people_at_table(order.table)
        
        if(people > 1):
            self.speech.say("Would anyone else like a drink?")
            response = self.hearing.recognize_answer_yn()
            for _ in range(people):
                self.make_local_order(order.table)
                
                self.speech.say("Would anyone else like a drink?")
                response = self.hearing.recognize_answer_yn()
                if not response:
                    break
                pass

        time.sleep(4)
        """
        print(self.mname +"Going to default location")
        self.robot.go_to_location(places.default)
        print(self.mname +"Arrived at default location")
        """

    def ask_refill(self, order):
        print(self.mname +"Checking refill for table "+order.table)
        # Go to the table
        self.robot.go_to_location(places.tables[order.table])     
        
        people = self.update_people_at_table(order.table)
        
        if(people > 0):
            self.speech.say(order.name + " would you like another drink?")
            response = self.hearing.recognize_answer_yn()
            if(response):
                self.speech.beep()
                self.orders.orders.append(order)

    
    def make_local_order(self, table):
        self.speech.say("What would you like to drink?")
        rs = ""
        for j in range(self.hearing.PROMPT_LIMIT):
            response = self.hearing.recognize_answer()
            if("coca cola" in response):
                rs = "coca cola"
                break
            elif("water" in response):
                rs = "water"
                break
            elif("coca cola light" in response):
                rs = "coca cola light"
                break
            else:
                self.speech.say("Sorry, we don't appear to have that. Can I bring you something else?")
        if(rs == ""):
            return
        self.orders.orders.append(Order(1, "sir", table, (rs,1)))

