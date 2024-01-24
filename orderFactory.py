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
        return f"Contract JSON: {self.JSON}"
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
        self.JSON = {}

    def _toJSON(self):
        self.JSON = {
                "acctId": self.acctId,
                "cOID": self.cOID,
                "orderType": self.orderType,
                "outsideRTH": self.outsideRth,
                "price": self.price,
                "side": self.side,
                "ticker": self.ticker,
                "tif": self.tif,
                "quantity": self.quantity
                }

    def updateAccountId(self, acctId):
        self.acctId = acctId

    def __repr__(self):
        if not self.JSON:
            self._toJSON()
        return f"Order JSON: {self.JSON}"


def createSampleContract():

    contract = Contract()
    contract.conid = 570639953
    contract.exchange = "NASDAQ"
    contract.ticker = "XCUR"

    contract.__repr__()

    return contract

def createSampleOrder():
    
    order = Order()
    order.orderType = "LMT"
    order.outsideRth = True
    order.price = 0.63
    order.side = "BUY"
    order.tif = "GTC"
    order.quantity = 1117
    order.cOID = "uniqueOrder"

    return order

