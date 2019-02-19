#!/usr/bin/env python
import math
import numpy as np
import rospy
import time

class Sight(object):
    bottle_types_db = ["Coca Cola", "Coca Cola Light", "Water"]
    bottle_types = ["coke", "coke diet", "water"]
    
    def __init__(self):
        self.objects = None
        self.mname = "[FAKE SIGHT] "


    def recognize_objects(self):
        print(self.mname + "Recognizing objects.")
        self.objects = [('Coke', 0.1), ('Water', 0.2), ('person', 0.3),('person', 0.3),('person', 0.3)]

    def count(self, label):
        return sum([1 if obj[0] == label else 0 for obj in self.objects])
                   
    def count_people(self):
       people = self.count('people')
       print(self.mname + "People detected: " + str(people))
       return people

    def count_stock(self):
       stock = [(btdb, self.count(bt)) for (bt, btdb) in zip(self.bottle_types, self.bottle_types_db)]
       print(self.mname + "Stock detected: " + str(stock))
       return stock

    def count_bottles(self):
        bottles = sum([c[1] for c in self.count_stock()])
        print(self.mname + "Bottles detected: " + str(bottles))
        
        return bottles
