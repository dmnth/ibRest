#! /usr/bin/env python3

class Contract():

    def __init__(self):
       
        # Provide only conid or conidex field
        self.conid = ''
        self.conidex = ''
        self.symbol = ''
        self.secType = ''
        self.currency = ''
        self.exchange = ''
        self.JSON = {}
    
    def useConidex(self):
        return

    def useConidExchange(self):
        return

    def fillDetails(symbol):
        return

    def _toJSON(self):
        self.JSON = {
                "conid": self.conid,
                "conidex": self.conidex, 
                "listingExchange": self.exchange,
                "ticker": self.ticker
                }


    def __repr__(self):
        if not self.JSON:
            self._toJSON()
        return f"Contract JSON: {self.JSON}\n"

class Order():

    def __init__(self):
        self.acctId = ""
        self.orderType = ""
        self.outsideRth = ""
        self.side = ""
        self.ticker = ""
        self.tif = ""
        self.quantity = ""
        self.cOID = ""
        self.referrer = ""
        self.parentId = ""
        self.price = "" 
        self.useAdaptive = False 
        self.JSON = {}

    def _toJSON(self):
        self.JSON = {
                "acctId": self.acctId,
                "cOID": self.cOID,
                "orderType": self.orderType,
                "outsideRTH": self.outsideRth,
#                "price": self.price,
                "side": self.side,
                "ticker": self.ticker,
                "tif": self.tif,
                "quantity": self.quantity,
                "referrer": self.referrer,
                "parentId": self.parentId,
                "useAdaptive": self.useAdaptive
                }

    def updateAccountId(self, acctId):
        self.acctId = acctId

    def __repr__(self):
        if not self.JSON:
            self._toJSON()
        return f"Order JSON: {self.JSON}\n"


def createSampleContract():

    contract = Contract()
    contract.conid = 570639953 
    contract.exchange = "NASDAQ"
    contract.ticker = "XCUR"

    contract.__repr__()

    return contract

def createSampleOrder():
    
    order = Order()
    order.orderType = "MKT"
    order.outsideRth = False 
#    order.price = 0.63
    order.side = "BUY"
    order.tif = "GTC"
    order.quantity = 1
    order.referrer = 'boris'
    order.cOID = "uniqueOrder445w5"

    return order


def createBracketOrder():

    contract = createSampleContract()

    order = Order()
    order.orderType = "MKT"
    order.outsideRth = False 
#    order.price = 0.63
    order.side = "BUY"
    order.tif = "GTC"
    order.quantity = 1
    order.cOID = "uniqueOrderNumber3"

    profitTaker = Order()
    profitTaker.orderType = "MKT"
    profitTaker.outsideRth = False 
#    profitTaker.price = 0.63
    profitTaker.side = "SELL"
    profitTaker.tif = "GTC"
    profitTaker.referrer = "ProfitTaker"
    profitTaker.quantity = 1
    profitTaker.useAdaptive = False
    profitTaker.parentId = order.cOID

    stopLoss = Order()
    stopLoss.orderType = "MKT"
    stopLoss.outsideRth = False 
#    stopLoss.price = 0.65
    stopLoss.side = "SELL"
    stopLoss.tif = "GTC"
    stopLoss.referrer = "ProfitTaker"
    stopLoss.quantity = 1
    stopLoss.useAdaptive = False
    stopLoss.parentId = order.cOID
    
    return [order, profitTaker, stopLoss] 




















