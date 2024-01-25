#! /usr/bin/env python3

import requests
import json
import time
import sys

from exceptions import *
from orderFactory import createSampleContract, createSampleOrder, createBracketOrder 
from endpoints import endpoints

requests.packages.urllib3.disable_warnings()

class OrderMonitor():

    def __init__(self):
        return

    def __sampleFunction(self):
        print("This function belongs to OrderMonitor class")

    def retrieveLiveOrders(self, filters):
        print(filters)
        params = {'filters': filters}
        response = requests.get(endpoints['live_orders'], params=params, verify=False)
        try:
            jsonData = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            # Sometimes API will return an empty string which
            # json fails to parse
            print("Empty response returned, json failed to parse")
            jsonData = []
        return jsonData

    def retrieveTradesHistory(self, days=''):
        params = {
                "days": days 
                }
        resp = requests.get(endpoints['trades'], params=params, verify=False)
        jsonData = json.loads(resp.text)
        with open('trades.json', 'w') as outfile:
            json.dump(jsonData, outfile, indent=2)
        return jsonData 

    def __repr__(self):
        return f'class OrderMonitor'

class Account():

    def __init__(self):
        self.id = ''

    def getId(self):
        endpoint = endpoints['accounts']
        resp = requests.get(endpoint, verify=False) 
        jsonData = json.loads(resp.text)
        accounts = jsonData['accounts']
        if len(accounts) > 1:
            print("Will have to pick an account")
            sys.exit()
        return accounts[0]

    def switch(selt):
        return

class Session():

    def __init__(self):
        self.attempts = 0

    def authenticateUser(self, username, password):
        return

    def relogin(self, username, password):
        return

    def checkAuthStatus(self):
        if self.attempts != 0:
            print(f"Reauth attempt number: {self.attempts}")
        try:
            endpoint = endpoints['auth_status']
            response = requests.get(endpoint, verify=False)
            if response.status_code == 401:
                raise NotLoggedIn 
            jsonData = json.loads(response.text)
            self.parseAuthResponse(jsonData)
            print(jsonData)
            return jsonData 

        except requests.exceptions.ConnectionError:
            print(f"Could't connect to server. Make sure that gateway is running")

        except NotLoggedIn:
            print("Please log in")

        except NotAuthenticated:
            self.reauthenticateSession()

        except CompetingSessionException:
            print("Only one session is allowed per username")

        except Exception as err:
            print(f"Authentication class exception -> ", err)



    def parseAuthResponse(self, jsonData):
        if jsonData['authenticated'] == jsonData['competing'] == jsonData['connected'] == False:
            # this happens if TWS runs in live or paper mode with same credentials
            raise NotAuthenticated

        if jsonData['competing'] == True:
            raise CompetingSessionException

        else:
            print("Auth response: ", jsonData)

    def reauthenticateSession(self):
        print('Trying to reauthenticate the session... ')
        # Why are we adding /sso/validate ?
        response = requests.get(endpoints['reauth'], verify=False)
        print(response.text)
        self.attempts += 1
        if self.attempts < 5:
            time.sleep(2)
            self.checkAuthStatus()
        else:
            print("Have sent 5 reauth requests, exiting ...")
            # Here should be a relogin call
            sys.exit()

    def __repr__(self):
        return f'class Authentication'


class Broker(Session):

    def __init__(self):
        OrderMonitor.__init__(self)
        Session.__init__(self)
        Account.__init__(self)
        self.account = Account()
        self.monitor = OrderMonitor()
        self.acctId = '' 

    def check(self):
        Order()._Order__sampleFunction()
        OrderMonitor()._OrderMonitor__sampleFunction()

    def isAuthenticated(self):
        data = self.checkAuthStatus()
        print("REAUTH: ", data)
        if data['authenticated'] == True:
            return True

    def showLiveOrders(self, filters=''):
        orders = self.monitor.retrieveLiveOrders(filters)
        jsonRepr = json.dumps(orders, indent=4)
        with open('liveOrders.json', 'w') as outFile:
            outFile.write(jsonRepr)

    def showTrades(self, days=''):
        self.monitor.retrieveTradesHistory(days)

    def setAccountId(self):
        self.acctId = self.account.getId() 

    def processOrderResponse(self, orderData):

        for el in orderData: 

            if el == 'error':
                print(el, orderData)
                sys.exit()

            if 'error' in el.keys():
                print(f"---> Error while placing order: {jsonData['error']}")
                sys.exit()

            if type(el) == dict and "id" in el.keys():
                print("Order requires confirmation")
                time.sleep(1)
                print(orderData)
                orderData = self.confirmOrder(el['id'])
                print("Confirmation 1: ", orderData)

        print("JSON: ", orderData)
        return orderData 

    def placeOrder(self, jsonData):
        endpoint = endpoints['place_order'].replace('accountId', self.acctId)
        resp = requests.post(endpoint, verify=False, json=jsonData)
        order = json.loads(resp.text)
        orderData = self.processOrderResponse(order)
        return orderData

    def confirmOrder(self, replyId):
        endpoint = endpoints['reply'].replace('replyId', replyId)
        data = {'confirmed': True}
        message = {}
        while 'order_id' not in message.keys():
            print("Incoming: ", message)
            response = requests.post(endpoint, verify=False, json=data)
            jsonData = json.loads(response.text)
            print("Outcoming: ", jsonData)
            if type(jsonData) == dict and 'error' in jsonData.keys():
                print("error: ", jsonData['error'])
                sys.exit()

            message = jsonData[0]
    
        return message

    def modifyOrder(self, orderId, jsonData):
        print(jsonData)
        endpoint = endpoints['modify'].replace('oid', orderId).replace('aid', self.acctId)
        response = requests.post(endpoint, verify=False, json=jsonData)
        order = json.loads(response.text)
        orderData = self.processOrderResponse(order)
        print("Modification: ", orderData)

    def makeMdSnapshot(self, conids, fields, since=""):
        params = {
                "conids": conids,
                "fields": fields,
                "since": since 
                }
        snapshot = {}
        while True:
            time.sleep(1)
            response = requests.get(endpoints['snapshot'], params=params, verify=False)
            jsonData = json.loads(response.text)
            print(jsonData)

        return

    def unsubscribeMd(self, conid):
        data = { 'conid': conid }
        response = requests.post(endpoints['unsubscribe'], data=data, verify=False)
        print("Unsubscribed: ", response.text)
        return

    def cancelOrder(self, orderId):
        return

    def __repr__(self):
        return 'Main Aplication'

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
    print(order)
    orderPayload = {'orders': [order.JSON] }

    json = broker.placeOrder(orderPayload)
    print("RETURNED: ", json)
    oid = json['order_id']
    print(oid)
    print("Order id: ", oid)
    orderPayload['orders'][0]['price'] = 0.546
    del orderPayload['orders'][0]['acctId']
    print(orderPayload['orders'][0])
    broker.modifyOrder(oid, orderPayload['orders'][0]) 

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
    broker.modifyOrder(orderPayload)

def testSnapshotFields():

    broker = Broker()
    if broker.isAuthenticated() == True:
        broker.setAccountId()
        broker.makeMdSnapshot(4815747, "6457,80,70,71,83,7087,7284,6509")
#        broker.unsubscribeMd(265598)
    else:
        print("Not authenticated")

if __name__ == "__main__":
    testBracketOrder()
