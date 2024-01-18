#! /usr/bin/env python3

class Contract():

    def __init__(self):
       
        # Provide only conid or conidex field
        self.conid = ''
        self.conidex = ''
        self.symbol = ''
        self.secType = ''
        self.currency = ''
        self.exchnage = ''
    
    def useConidex(self):
        if self.conid != '' or self.exchnage != '':
            self.conidex = self.conid + '@' + self.exchange
            self.conid = ''
            self.exchnage = ''
        else:
            print("To create conidex both conid and exchange are required")

    def useConidExchange(self):
        if self.conidex != '':
            pair = self.conidex.split('@')
            self.conid = pair[0]
            self.exchnage = pair[1]
        else:
            print("conidex is missing")

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
                "cOID": self.cOID,
                "conidex": self.contract.conidex, 
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
#        order.cOID = "other_unique_payload1"
        order.orderType = "LMT"
        order.outsideRth = False 
        order.price = 0.797
        order.side = "SELL"
        order.ticker = "undefined"
        order.tif = "GTC"
        order.quantity = 1117 

        data = { "orders": [
            order._toJSON() 
            ]
            }

        return data

def createBracketOrder(accId):

    contract = Contract()
    contract.conid = "570639953"
    contract.exchange = "NASDAQ"
#    contract.useConidex()

    order = Order(contract)
#    order.cOID = "other_unique_payload1"
    order.acctId = accId
    order.orderType = "LMT"
    order.outsideRth = False
    order.price = 0.8955000000000001
    order.side = "SELL"
    order.ticker = "undefined"
    order.tif = "GTC"
    order.quantity = 1117

    data = {"orders": [
        order._toJSON()
        ]
        }

    return data
