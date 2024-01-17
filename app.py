#! /usr/bin/env python3

import requests
import json
import time
import sys

from sqlalchemy import create_engine, text
from exceptions import *
from orderFactory import createSampleOrder
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

class dB():

    def __init__(self):
        return

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

    def placeOrder(self):
        data = createSampleOrder(self.acctId)
        endpoint = endpoints['place_order'].replace('accountId', self.acctId)
        resp = requests.post(endpoint, verify=False, json=data)
        jsonData = json.loads(resp.text)
        print("/iserver/account/{accountid}/orders response: ", jsonData)
        for el in jsonData:
            if 'error' in el:
                print(f"---> Error while placing order: {jsonData['error']}")
                sys.exit()
            if type(el) == dict and "id" in el.keys():
                time.sleep(1)
                jsonData = self.confirmOrder(el['id'])
        print(jsonData)
        return jsonData[0] 

    def confirmOrder(self, replyId):
        print("Reply id: ", replyId)
#        endpoint = base_url + f"/iserver/reply/{replyID}"
        endpoint = endpoints['reply'].replace('replyId', replyId)
        print(endpoint)
        data = {'confirmed': True}
        response = requests.post(endpoint, verify=False, json=data)
        if len(response.text) != 0:
            jsonData = json.loads(response.text)
            for e in jsonData:
                if 'id' in e.keys():
                    print(f"Confirmation: {e['id']}")
                    orderReply(e['id'])
            return jsonData
        else:
            print("Nothing left to confirm")

    def modifyOrder(self, orderId):
        print("Modifying an order with id: {orderId}")
        return

    def cancelOrder(self, orderId):
        return

    def __repr__(self):
        return 'Main Aplication'

if __name__ == "__main__":
    
    broker = Broker()
    broker.isAuthenticated()
    broker.setAccountId()
    broker.placeOrder()

