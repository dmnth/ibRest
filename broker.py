#! /usr/bin/env python3

import requests
import json
import time
import csv
import sys

from exceptions import *
from json.decoder import JSONDecodeError
from orderFactory import createSampleContract, createSampleOrder, createBracketOrder, Contract, Order
from endpoints import endpoints
from baseContract import Instrument, Contract
from errorParser import errorHandler
from json.decoder import JSONDecodeError

requests.packages.urllib3.disable_warnings()

class ContractDetailsManager():

    def __init__(self):

        self.value = None
        self.contracts = {'stocks': []} 

    def stockContractsFromCompanyNames(self, pathToCsv):
        with open(pathToCsv, 'r') as csvFile:
            csvReader = csv.reader(csvFile)
            lineCount = 0
            for line in csvReader:
                if lineCount == 0:
                    lineCount += 1
                else:
                    compName = line[1]
                    symb = line[0].split(' ')[0]
                    try:
                        inst = Instrument(symbol=symb, companyName=compName)
                        inst.getContractsByName()
                        contract = inst.json
                        self.contracts['stocks'].append(contract[0])
                    except NoContractsFoundForCompany:
                        continue
                    lineCount += 1

    def stockContractsFromSymbols(self, pathToCsv):
        with open(pathToCsv, 'r') as csvFile:
            csvReader = csv.reader(csvFile)
            lineCount = 0
            for line in csvReader:
                if lineCount == 0:
                    lineCount += 1
                else:
                    symb = line[0]
                    inst = Instrument(symbol=symb, companyName='')
                    try:
                        if lineCount > 500:
                            break
                        inst.getContractsBySymbol()
                        contract = inst.json
                        print(contract[0])
                        self.contracts['stocks'].append(contract[0])
                        lineCount += 1
                    except NoContractsFoundForSymbol:
                        continue

    def stokcContractsFromXLSX(self, pathToXLXS):
        return

    def writeJSON(self, filename):
        # Should be defined as helper method as used everywhere
        filename += '.json'
        with open(filename, 'w') as jsonFile:
            json.dump(self.contracts, jsonFile, indent=4)

    def readJSON(self):
        return

    def readTXT(self):
        return

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
        print("Selected account: ", accounts[0])
        accountId = accounts[0]
        self.id = accountId
        return self.id 
#        account = input('Select account: ')
#        while account not in accounts:
#            account = input('Select valid account: ')
#        return account 

    def getWatchlistis(self):
        endpoint = endpoints['watchlists']
        resp = requests.get(endpoint, verify=False)
        print(resp.text)

    def invalidatePositions(self):
        endpoint = endpoints['inv_positions']
        invEndpoint = endpoint.replace('ACCID', self.id)
        response = requests.post(invEndpoint, verify=False)
        jsonData = json.loads(response.text)
        try:
            if jsonData['message'] == 'success':
                print('Succesfully invalidated positions')
        except KeyError as err:
            print("Invalidation failed")

    def getCurrentAccPos(self, pageId):
        self.getAccounts()
        endpoint = endpoints['acc_positions']
        print(endpoint)
        params = {"model": '', 'size': '10', 'sort': 'a', 'direction': 'a', 'period': '1D'}
        accPositions = endpoint.replace('ACCID', self.id).replace('PAGEID', str(pageId))
        print(accPositions)
        response = requests.get(accPositions, verify=False, params=params)
        jsonData = json.loads(response.text)
        print(type(jsonData))
        print(len(jsonData))
        with open('positions.json', 'w') as outFile:
            json.dump(jsonData, outFile, indent=4)
        return jsonData

    def getAccounts(self):
        response = requests.get(endpoints['portfolio_acc'], verify=False)
        jsonData = json.loads(response.text)
        print(jsonData)

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
            sys.exit()

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
        self.contracts = {}
        self.orderQeue = []

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

    def secDefParams(self, symbol, secType):
        inst = Instrument(symbol)
        inst.getContractsBySymbol(symbol)
        inst.assignConid()
        inst.setChainsJSON(secType)
        inst.futSecDefInfo()
        sys.exit()


    def showTrades(self, days=''):
        self.monitor.retrieveTradesHistory(days)

    def setAccountId(self):
        self.acctId = self.account.getId() 

    def showPositions(self, pageId):
        self.account.getCurrentAccPos(pageId)

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

        return orderData 

    def placeOrder(self, contractJSON):
        payload = {'orders': [contractJSON]}
        endpoint = endpoints['place_order'].replace('accountId', self.acctId)
        resp = requests.post(endpoint, verify=False, json=payload)
        print("Place order response: ", resp.text, resp.status_code)
        if resp.status_code == 200:
            order = json.loads(resp.text)
            try:
                if order['error']:
                    # Parse the error JSON here
                    errorHandler(order)

            except TypeError:
                error = order[0]
                print('########################################')
                print(error)
                print('for some reason error came in in format of a list')
            except JSONDecodeError:
                print('Faulty response object that raised JSONDecodeError: ')
                print(response.text)
                sys.exit
            except TypeError:
                # Process response if no error in payload keys
                orderData = self.processOrderResponse(order)
                return orderData
        if resp.status_code == 500:
            print("Writing faulty JSON that triggered 500")
            print("Please spend time realising what has gone wrong")
            print(contractJSON)
            time.sleep(10)
            with open('errors/500ErrorPayload.json') as outfile:
                outfile.dump(contractJSON, outfile, indent=4)
            raise IntenalServerError

        if resp.status_code == 405:
            print("405 in a workflow. Who you gonna call?")
            time.sleep(5)
            print('/iserver/auth/status')

    def confirmOrder(self, replyId):
        endpoint = endpoints['reply'].replace('replyId', replyId)
        data = {'confirmed': True}
        message = {}
        while 'order_id' not in message.keys():
            print("Incoming: ", message)
            response = requests.post(endpoint, verify=False, json=data)
            try:
                jsonData = json.loads(response.text)
                print("Outcoming: ", jsonData)
                if jsonData['error']:
                    # Parse the error JSON here
                    errorHandler(jsonData)
            except TypeError:
                message = jsonData[0]
            except json.decoder.JSONDecodeError:
                print('Faulty response object that raised JSONDecodeError: ')
                print(response.text)
                sys.exit
    
        return message

    def modifySingleOrder(self, orderId, orderPayload, price, size):
        print(orderPayload)

        if len(orderPayload['orders']) > 1:
            print("Cant handle multiple orders at once")
            sys.exit()

        orderPayload['orders'][0]['price'] = price 
        orderPayload['orders'][0]['size'] = size
        del orderPayload['orders'][0]['acctId']
        modPayload = orderPayload['orders'][0]
        endpoint = endpoints['modify'].replace('oid', orderId).replace('aid', self.acctId)
        response = requests.post(endpoint, verify=False, json=modPayload)
        order = json.loads(response.text)
        orderData = self.processOrderResponse(order)
        print("Modification: ", orderData)

    def whatIfplaceOrder(self, orderJson):
        payload = {'orders': [orderJson]}
        endpoint = endpoints['whatif'].replace('ACCID', self.acctId)
        resp = requests.post(endpoint, verify=False, json=payload)
        if resp.status_code == 200:
            order = json.loads(resp.text)
            try:
                if order['error']:
                    # Parse the error JSON here
                    errorHandler(order)
            except JSONDecodeError:
                print('Faulty response object that raised JSONDecodeError: ')
                print(response.text)
                sys.exit
            except TypeError:
                # Process response if no error in payload keys
                orderData = self.processOrderResponse(order)
                return orderData
        if resp.status_code == 500:
            print(f'[ERROR 500] {resp.text} - {orderJson}')
            errorObject = json.loads(resp.text)
            if errorObject['error'] == 'TIMEOUT':
                print('TIMEOUT HAS REACHED')
                raise TimeoutError
            with open('errors/500ErrorPayload.json', 'a') as outfile:
                json.dump(orderJson, outfile, indent=4)

    def makeMdSnapshot(self, conids, fields, since=""):
        params = {
                "conids": conids,
                "fields": fields,
        #        "since": since 
                }
        snapshot = {}
        while True:
            time.sleep(1)
            response = requests.get(endpoints['snapshot'], params=params, verify=False)
            jsonData = json.loads(response.text)
            ticks = jsonData[0]
            try:
                print(f"LAST: {ticks['31']} - BID: {ticks['84']} - ASK: {ticks['86']}")
            except KeyError:
                continue

        return

    def unsubscribeMd(self, conid):
        data = { 'conid': conid }
        response = requests.post(endpoints['unsubscribe'], data=data, verify=False)
        print("Unsubscribed: ", response.text)
        return

    def getHistory(self, conid, exchange, period, bar, startTime, outsideRth):
        endpoint = endpoints['history']
        params = {
                'conid': conid,
                'exchange': exchange,
                'period': period,
                'bar': bar,
                'startTime': startTime,
                'outsideRth': outsideRth
                }
        response = requests.get(endpoint, params=params, verify=False)
        try:
            jsonData = json.loads(response.text)
            if 'error' in jsonData.keys():
                errorHandler(jsonData) 
            with open('historicalSample.json', 'w') as outfile:
                json.dump(jsonData, outfile, indent=4)
                print('data stored')
                outfile.close()
        except JSONDecodeError:
            print('---> Empty response')
            print(f'---> Response length: {len(response.text)}')

    def showWatchlists(self):
        self.account.getWatchlistis()

    def showAccounts(self):
        self.account.getAccounts()

    def cancelOrder(self, orderId):
        return

    def readContactJSON(self, pathToJSON):

        with open(pathToJSON, 'r') as InputFile:
            contracts = json.load(InputFile)

        self.contracts = contracts 

    def __repr__(self):
        return 'Main Aplication'


if __name__ == "__main__":
    testAlgoOrder()
