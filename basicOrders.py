#! /usr/bin/env python3

orderString = """
        self.acctId = ""
        self.orderType = ""
        self.outsideRth = False 
        self.side = ""
        self.ticker = ""
        self.tif = ""
        self.quantity = ""
        self.cOID = ""
        self.referrer = ""
        self.parentId = ""
        self.price = "" 
        self.useAdaptive = False 
        self.trailingType = ""
        self.trailingAmount = ""
        self.strategy = ""
        self.strategyParameters = "" 
        self.auxPrice = ""
        self.JSON = {}
"""

class BaseOrder:

    def __init__(self, action, totalQuantity):

        self.side = action
        self.quantity = totalQuantity
        # All orders will have a default time 
        # in force value of "DAY" because of reasons
        self.tif = "DAY" 

class MktOrder(BaseOrder):
    
    def __init__(self, action, totalQuantity):
        BaseOrder.__init__(self, action, totalQuantity)
        self.orderType = "MKT"

    def __repr__(self):
        return "Market order"

class LimitOrder(BaseOrder):

    def __init__(self, action, limitPrice, totalQuantity):
        BaseOrder.__init__(self, action, totalQuantity)
        self.orderType = "LMT"
        self.price = limitPrice

    def __repr__(self):
        return  "Limit order"
