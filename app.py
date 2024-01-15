#! /usr/bin/env python3

import requests
import json
import time
import sys

local_ip = "127.0.0.1:5000"
base_url = f"https://{local_ip}/v1/api"

requests.packages.urllib3.disable_warnings()

class Unauthenticated(Exception):
    # Is triggered if user is unauthenticated 
    # Either was not logged in or session timed out
    pass

class Unauthorized(Exception):
    pass

class AuthenticationFailureException(Exception):
    # Is triggered on occasion when there is a TWS or IBGateway session running
    # Or if the previous session was not properly exited by logging out of the 
    # TWS or calling /logout endpoint.
    pass

class CompetingSessionException(Exception):
    # is raised if there is a competing session running. Only one session
    # is allowed per username
    pass

class Contract():

    def __init__(self):
        return

    def __repr__(self):
        return f'class Contract'

class Order():

    def __init__(self):
        # Initialize order details

    def __repr__(self):
        return f'class Order'

class OrderMonitor():

    def __init__(self):
        return

    def __sampleFunction(self):
        print("This function belongs to OrderMonitor class")

    def __repr__(self):
        return f'class OrderMonitor'

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
            response = requests.get(base_url + "/iserver/auth/status", verify=False)
            if response.status_code == 401:
                raise Unauthenticated 
            jsonData = json.loads(response.text)
            self.parseAuthResponse(jsonData)
            print("Authenticated successfully")

        except requests.exceptions.ConnectionError:
            print(f"Could't connect to server. Make sure that gateway is running")

        except Unauthenticated:
            print("Please log in")

        except AuthenticationFailureException:
            print("Make sure that you have properly closed the all other sessions")
            self.reauthenticateSession()

        except CompetingSessionException:
            print("Only one session is allowed per username")

        except Exception as err:
            print(f"Authentication class exception -> ", err)

    def parseAuthResponse(self, jsonData):
        if jsonData['authenticated'] == jsonData['competing'] == jsonData['connected'] == False:
            # this happens if TWS runs in live or paper mode with same credentials
            raise AuthenticationFailureException

        if jsonData['competing'] == True:
            raise CompetingSessionException

        else:
            print("Auth response: ", jsonData)

    def reauthenticateSession(self):
        print('Trying to reauthenticate the session... ')
        # Why are we adding /sso/validate ?
        response = requests.get(base_url + '/iserver/reauthenticate', verify=False)
        print(response.text)
        time.sleep(1)
        self.attempts += 1
        if self.attempts < 5:
            self.checkAuthStatus()
        else:
            print("Have sent 5 reauth requests, exiting ...")
            # Here should be a relogin call
            sys.exit()

    def __repr__(self):
        return f'class Authentication'

class DBWriter():

    def __init__(self):
        return

class TraderApp(Session):

    def __init__(self):
        Order.__init__(self)
        OrderMonitor.__init__(self)
        Session.__init__(self)

    def check(self):
        Order()._Order__sampleFunction()
        OrderMonitor()._OrderMonitor__sampleFunction()

    def isAuthenticated(self):
        self.checkAuthStatus()

    def placeOrder(self, contract, order):
        # Check if authenticated
        self.isAuthenticated()

    

    def __repr__(self):
        return 'Main Aplication'

if __name__ == "__main__":
    
    app = TraderApp()
    app.placeOrder('sample', 'test')


