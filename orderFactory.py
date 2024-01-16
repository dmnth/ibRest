#! /usr/bin/env python3

class Contract():

    def __init__(self):
        
        self.conid = ''
        self.symbol = ''
        self.secType = ''
        self.currency = ''
        self.exchnage = ''

    def fillDetails(symbol):
        return

    def __repr__(self):
        return f'Contract: {self.symbol} - {self.conid} - {self.exchange} - {self.secType} - {self.currency}'

class Order(Contract):

    def __init__(self, Contract):
        self.contract = Contract
        self.acctId = ""
        self.cOID = ""
        self.orderType = ""
        self.outsideRth = ""
        self.side = ""
        self.ticker = ""
        self.tif = ""
        self.quantity = ""

    def _toJSON(self):
        jsonData = {
                "acctId": self.acctId,
                "conid": self.contract.conid,
                "orderType": self.orderType,
                "listingExchange": self.contract.exchange,
                "outsideRTH": self.outsideRth,
                "price": self.price,
                "side": self.side,
                "ticker": self.ticker,
                "tif": self.tif,
                "quantity": self.quantity
                }

        return jsonData

    def __repr__(self):
        orderJSON = self._toJSON()
        return f"Order JSON: {orderJSON}"


def createSampleOrder(acctId):

        contract = Contract()
        contract.conid = 570639953 
        contract.exchange = "NASDAQ"

        order = Order(contract)
        order.acctId = acctId 
        order.orderType = "LMT"
        order.outsideRth = False
        order.price = 0.797
        order.side = "BUY"
#        order.ticker = "AAPL"
        order.tif = "GTC"
        order.quantity = 1 

        data = { "orders": [
            order._toJSON() 
            ]
            }

        return data
