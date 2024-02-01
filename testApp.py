#! /usr/bin/env python3

import json
import sys
from broker import Broker
from orderFactory import Contract, Order

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
    contract = Contract()
    contract.fillOptDetails('679322318')
    if broker.isAuthenticated() == True:
        broker.setAccountId()
        broker.makeMdSnapshot(679322318, "31,6509,7283,7633")
#        broker.unsubscribeMd(265598)
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
    contract.fillOptDetails(conid)
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
    order.orderType = 'TRAIL'
    order.side = 'BUY'
    order.trailingType = 'amt'
    order.trailingAmount = 2
    order.quantity = 1
    order.tif = 'GTC'
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



def testWatchlists():
    broker = Broker()
    broker.isAuthenticated()
    broker.setAccountId()
    broker.showWatchlists()

if __name__ == "__main__":
    testAlgoOrder('679322318')
