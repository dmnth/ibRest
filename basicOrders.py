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

    def __init__(self, action, totalQuantity, orderType):

        self.side = action
        self.orderType = orderType
        self.quantity = totalQuantity

class MktOrder(BaseOrder):
    
    def __init__(self, action, totalQuantity, orderType="MKT"):
        BaseOrder.__init__(self, action, totalQuantity, orderType)

    def __repr__(self):
        return "Market order"

class MarketIfTouched(BaseOrder):
    def __init__(self, action, totalQuantity, auxPrice,
            orderType="MIT"):
        BaseOrder.__init__(self, action, totalQuantity, orderType)
        self.auxPrice = auxPrice

    def __repr__(self):
        return "Market if touched"

class MarketOnClose(BaseOrder):
    
    def __init__(self, action, totalQuantity, orderType="MOC"):
        BaseOrder.__init__(self, action, totalQuantity, orderType)
    
    def __repr__(self):
        return "Market on close"

class MarketOnOpen(BaseOrder):
    
    def __init__(self, action, totalQuantity, orderType="MKT"):
        BaseOrder.__init__(self, action, totalQuantity, orderType)
        self.tif = "OPG"

    def __repr__(self):
        return "Market on open"

class LimitOrder(BaseOrder):

    def __init__(self, action, totalQuantity, limitPrice,
            orderType="LMT"):
        BaseOrder.__init__(self, action, totalQuantity, orderType)
        self.price = limitPrice
    def __repr__(self):
        return "Limit order"

