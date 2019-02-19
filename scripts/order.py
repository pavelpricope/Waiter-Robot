#!/usr/bin/env python


class Order(object):
    def __init__(self, id=None, name=None, table=None, contents=None):
        self.id = id
        self.name = name
        self.table = table
        self.contents = contents
