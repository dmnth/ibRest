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

    def __init__(self, action, totalQuantity, tif):

        self.side = action
        self.quantity = totalQuantity
        # All orders will have a default time 
        # in force value of "DAY" because of reasons
        self.tif = tif 

class MktOrder(BaseOrder):
    
    def __init__(self, action, totalQuantity, tif):
        BaseOrder.__init__(self, action, totalQuantity, tif)
        self.orderType = "MKT"

    def __repr__(self):
        return "Market order"

class LimitOrder(BaseOrder):

    def __init__(self, action, limitPrice, totalQuantity, tif):
        BaseOrder.__init__(self, action, totalQuantity, tif)
        self.orderType = "LMT"
        self.price = limitPrice

    def __repr__(self):
        return  "Limit order"

class GTDLimitOrder(LimitOrder):
    def __init__(self, action, limitPrice, totalQuantity, tif, gdUntl, expTime):
        LimitOrder.__init__(self, action, limitPrice, totalQuantity, tif)
        self.goodTillDate = gdUntl 
        self.expireTime = expireTime 


class FxMktOrder(MktOrder):
    # needs isCcyConv: True
    def __init__(self):
        return

class FxLimitOrder(MktOrder):
    # isCcyConv: True and fxQty instead of totalQuantity
    def __init__(self):
        return
