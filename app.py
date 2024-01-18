#! /usr/bin/env python3

import requests
import json
import time
import sys

from exceptions import *
from orderFactory import createSampleOrder, createBracketOrder
from endpoints import endpoints

requests.packages.urllib3.disable_warnings()

class OrderMonitor():

    def __init__(self):
        return

    def __sampleFunction(self):
        print("This function belongs to OrderMonitor class")

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
            print("Authenticated successfully")

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
        self.checkAuthStatus()

    def getTrades(self, days=''):
        self.monitor.retrieveTradesHistory(days)

    def setAccountId(self):
        self.isAuthenticated()
        self.acctId = self.account.getId() 

    def placeOrder(self, jsonData):
        data = createSampleOrder(self.acctId)
        endpoint = endpoints['place_order'].replace('accountId', self.acctId)
        resp = requests.post(endpoint, verify=False, json=data)
        jsonData = json.loads(resp.text)
        for el in jsonData:
            if 'error' in el.keys():
                print(f"---> Error while placing order: {jsonData['error']}")
                sys.exit()
            if type(el) == dict and "id" in el.keys():
                time.sleep(1)
                jsonData = self.confirmOrder(el['id'])

        print(jsonData)
        return jsonData[0] 

    def confirmOrder(self, replyId):
        endpoint = endpoints['reply'].replace('replyId', replyId)
        print(endpoint)
        data = {'confirmed': True}
        response = requests.post(endpoint, verify=False, json=data)
        if len(response.text) != 0:
            jsonData = json.loads(response.text)
            print(jsonData)
            for e in jsonData:

                if e == 'error':
                    print(jsonData['error'], 'error')
                    sys.exit()

                if 'id' in e.keys():
                    print(f"Confirmation: {e['id']}")
                    self.confirmOrder(e['id'])

                if jsonData[0]['order_status'] == 'Cancelled':
                    print("Order status: Cancelled")
                    sys.exit()
        else:
            return jsonData

    def modifyOrder(self, orderId, jsonData):
        print(jsonData)
        endpoint = endpoints['modify'].replace('oid', orderId).replace('aid', self.acctId)
        response = requests.post(endpoint, verify=False, json=jsonData)
        print(response.text)

    def cancelOrder(self, orderId):
        return

    def __repr__(self):
        return 'Main Aplication'

if __name__ == "__main__":
    
    broker = Broker()
    broker.isAuthenticated()
    broker.setAccountId()

    order1 = createSampleOrder(broker.acctId) 
    order2 = createBracketOrder(broker.acctId)
    print(order1)
    print(order2)

    json = broker.placeOrder(order1)
    print("RETURNED: ", json)
    oid = json['order_id']
    time.sleep(1)
    removed = order2['orders'][0].pop('acctId')
    broker.modifyOrder(oid, order2['orders'][0]) 

