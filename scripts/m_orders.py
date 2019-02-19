#!/usr/bin/env python
import requests 
from time import time as now

from order import Order


REFILL_INTERVAL_SECS = 60



class Orders(object):

    def __init__(self, database):
        self.database = database
        self.orders = []
        self.pending_order = None
        self.executed_orders = []

    def did_complete(self, order):
        print "Completed order " + ("matches" if order == self.pending_order else "does not match") + " the pending order"
        self.executed_orders.append([order, now()])
        self.pending_order = None
        #tell database about this qunatity change
    
    def get_next_order(self):
        self.orders.extend(self.database.get_new_orders())
    
        if(len(self.orders) < 1):
            return None

        order = self.pending_order = self.orders[0]
        self.orders.remove(order)
        return order

    def get_next_refill(self):
        if len(self.executed_orders) < 1:
            return None
        
        order = self.executed_orders[0] 
        if (now() - order[1]) < REFILL_INTERVAL_SECS:
            return None
        
        self.executed_orders.remove(order)
        return order[0]


