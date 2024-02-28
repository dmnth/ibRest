#! /usr/bin/env python3

import json
import sys
from broker import Broker
from orderFactory import Contract, Order
from basicOrders import MktOrder, LimitOrder
from baseContract import Contract as BaseContract, Instrument

def testOrderOperations():
    broker = Broker()
    broker.isAuthenticated()
    broker.setAccountId()

    broker.showLiveOrders('PreSubmitted')

    contract = createSampleContract() 
    order = createSampleOrder()
    order.updateAccountId(broker.acctId)
    order._toJSON()
    order.JSON.update(contract.JSON)
    orderPayload = {'orders': [order.JSON] }

    json = broker.placeOrder(orderPayload)
    oid = json['order_id']
    broker.modifySingleOrder(oid, orderPayload, price=0.845, size=2) 

    broker.showLiveOrders('')

def testBracketOrder():
    broker = Broker()
    broker.isAuthenticated()
    broker.setAccountId()
    contract = createSampleContract()
    bracketOrder = createBracketOrder() 
    orderPayload = {'orders': [] }
    for el in bracketOrder:
        el.updateAccountId(broker.acctId)
        el._toJSON()
        el.JSON.update(contract.JSON)
        orderPayload['orders'].append(el.JSON)
        print(orderPayload)

    broker.placeOrder(orderPayload)

def testSnapshotFields():

    broker = Broker()
    broker.isAuthenticated()
    broker.setAccountId()
    broker.secDefParams('BMW', 'FUT')
    sys.exit()
    if broker.isAuthenticated() == True:
        broker.setAccountId()
        broker.makeMdSnapshot(14094, "55,58,31,6509,7283,7633")
        broker.unsubscribeMd(667220441)
    else:
        print("Not authenticated")

def testTrailStopOrder():
    broker = Broker()
    broker.isAuthenticated()
    broker.setAccountId()
    contract = Contract()
    contract.fillOptDetails('679322318')

    order = Order()
    order.price = 11
    order.orderType = 'TRAIL'
    order.side = 'BUY'
    order.trailingType = 'amt'
    order.trailingAmount = 2
    order.quantity = 1
    order.tif = 'GTC'
    order._toJSON()

    order.updateAccountId(broker.acctId)
    order._toJSON()
    order.JSON.update(contract.JSON)
    del order.JSON['cOID']
    del order.JSON['ticker']
    del order.JSON['referrer']
    del order.JSON['parentId']
    del order.JSON['conidex']
    order.JSON['conid'] = 679322318
    orderPayload = {'orders': [order.JSON] }
    jsonFile = json.dumps(orderPayload, indent=4)
    with open('stpPayload.txt', 'w') as outfile:
        outfile.write(jsonFile)
        outfile.close()
    print(jsonFile)
    jsonReply = broker.placeOrder(orderPayload)
    print(jsonReply)
    print(type(jsonReply))

def fillStrategyParams(algos, conid):
    return
    

def testAlgoOrder(conid):
    broker = Broker()
    broker.isAuthenticated()
    broker.setAccountId()
    contract = Contract()
    contract.fillContractDetails(conid)
    algos = contract.getAvailableAlgos(conid)
    print(f"Available algorithms for {contract.symbol}")
    for i in range(len(algos)):
        print(f'{i+1}. {algos[i]["name"]}')
    choises= [i for i in range(1, len(algos)+1)]
    choise = int(input(f"Please select algo. Available choices: {choises}"))
    print(choise)
    while choise not in choises:
        print(f"{choise} should be one of {choises}")
        choise = int(input("Please select algo: "))
    algoIdx = choise - 1
    algo = algos[algoIdx]
    print(f"You have chosen {algos[algoIdx]}")
    algoParams = contract.getAlgoParams(conid, algo['id'])
    strategyParameters = {}
    for param in algoParams[0]['parameters']:
        print("Current parameter: ", param['id'], param['valueClassName'])
        value = input(f"Specify values for {param['id']}: ")
        pair = { param['id']: value }
        strategyParameters.update(pair)

    order = Order()
    order.price = 11
    order.orderType = 'LMT'
    order.side = 'BUY'
#    order.trailingType = 'amt'
#    order.trailingAmount = 2
    order.quantity = 1
    order.tif = 'DAY'
    order.strategy = "TWAP"
    order.strategyParameters = strategyParameters 
    order.updateAccountId(broker.acctId)
    order._toJSON()
    contract.exchange = ""
    contract._toJSON()
    print(contract.exchange)
    print(contract.JSON)
    order.JSON.update(contract.JSON)
    print(order.JSON['listingExchange'])
    orderPayload = {'orders': [order.JSON] }
    jsonFile = json.dumps(orderPayload, indent=4)
    with open('algoPayload.txt', 'w') as outfile:
        outfile.write(jsonFile)
        outfile.close()
    jsonReply = broker.placeOrder(orderPayload)
    print(jsonReply)
    print(type(jsonReply))

    orders = broker.showLiveOrders()

def placeAlgoOrder():

    broker = Broker()
    broker.isAuthenticated()
    broker.setAccountId()
    vwapAlgoPayload = { 
                "acctId": "U10412366",
                "conid": 265598,
                "cOID": "MY_VERY_UNIQUE_VWAP_ORDER_FULL_PARAMS",
                "secType": "265598@STK",
                "price": 186.20,
                "orderType": "LMT",
                "outsideRTH": False,
                "side": "BUY",
                "ticker": "AAPL",
                "tif": "DAY",
                "quantity": 1,
                "strategy": "Vwap",
                "strategyParameters": {
                    "maxPctVol": 10,
                    "startTime": "14:00:00 US/Eastern",
                    "endTime": "10:00:00 US/Eastern",
                    "allowPastEndTime": True,
                    "noTakeLiq": True,
                    "speedUp": True,
                    "conditionalPrice": 180.21
                    }
                }
    twapAlgoPayload = { 
                "acctId": "U10412366",
                "conid": 265598,
                "cOID": "MY_VERY_UNIQUE_TWAP_ORDER_FULL_PARAMS",
                "secType": "265598@STK",
                "price": 186.20,
                "orderType": "LMT",
                "outsideRTH": False,
                "side": "BUY",
                "ticker": "AAPL",
                "tif": "DAY",
                "quantity": 1,
                "strategy": "Twap",
                "strategyParameters": {
                    "startTime": "14:00:00 US/Eastern",
                    "endTime": "10:00:00 US/Eastern",
                    "allowPastEndTime": True,
                    "catchUp": True,
                    "conditionalPrice": 180.21
                    }
                }
                

    payload = {
            "acctId": "U10412366",
            "conid": 265598,
            "orderType": "LMT",
            "price": 110,
            "listingExchange": "SMART",
            "side": "BUY",
            "ticker": "AAPL",
            "tif": "GTC",
            "quantity": 200,
            "outsideRTH": True 
            }
    
    orderPayload = {'orders': [twapAlgoPayload]}
    jsonData = json.dumps(orderPayload, indent=4)
    with open('validAlgoPayload.json', 'w') as outFile:
        outFile.write(jsonData)
        outFile.close()
    broker.placeOrder(orderPayload)

def placeSimpleOrder():
    broker = Broker()
    broker.isAuthenticated()
    broker.setAccountId()
    payload = {
            'acctId': 'U10412366',
            'conid': 265598,
            'orderType': 'LMT',
            'price': 110,
            'listingExchange': 'SMART',
            'side': 'BUY',
            'ticker': 'AAPL',
            'tif': 'GTC',
            'quantity': 200,
            'outsideRTH': True 
            }
    
    orderPayload = {'orders': [payload]}
    broker.placeOrder(orderPayload)


def testWatchlists():
    broker = Broker()
    broker.isAuthenticated()
    broker.setAccountId()
    broker.showWatchlists()

def testSymbolSearch():
    broker = Broker()
    broker.isAuthenticated()
    broker.setAccountId()
    contract = Contract()
    contract.symbol = "AAPL"
    contract.searchSymbol()

def testOrderObject():
    mktOrder = MktOrder("BUY", 1)
    print(mktOrder)
    print(mktOrder.__dict__)

    lmtOrder = LimitOrder("BUY", 1, 1) 
    print(lmtOrder)
    print(lmtOrder.__dict__)

def testContractObject():
    contract = BaseContract("265598")
    print(contract)
    print(contract.__dict__)

def testPayload():
    contract = BaseContract("265598").__dict__
    mktOrder = MktOrder("BUY", 1).__dict__
    contract.update(mktOrder)
    print(contract)

def testChangeTif():
    mktOrder = MktOrder("BUY", 1)
    mktOrder.tif = "GTC"
    print(mktOrder)
    print(mktOrder.__dict__)

def testPlaceOrder():
    broker = Broker()
    broker.isAuthenticated()
    broker.setAccountId()
    contract = BaseContract(265598)
    mktOrder = MktOrder("BUY", 1)
    mktOrder.tif = "GTC"
    contract.__dict__.update(mktOrder.__dict__)
    payload = {'orders': [contract.__dict__] }
    print(payload)
    broker.placeOrder(payload)

def testOrderPlacementLogic():
    testOrderObject()
    testContractObject()
    testChangeTif()
    testPayload()
    testPlaceOrder()

def testPositionsPerAccount():
    broker = Broker()
    broker.isAuthenticated()
    broker.setAccountId()
    broker.showPositions(pageId=0)

def testCanParseCSVtoObject():
    broker = Broker()
    broker.isAuthenticated()
    broker.setAccountId()
    instrumentList = broker.namesToList('contractCsvData/worst20SPversion2.csv')

if __name__ == "__main__":
    testCanParseCSVtoObject()
#    testPlaceOrder()
#    testPositionsPerAccount()
