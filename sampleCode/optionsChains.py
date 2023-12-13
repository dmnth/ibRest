#! /usr/bin/env python3

import json
import requests

local_ip = "127.0.0.1:5000"
base_url = f"https://{local_ip}/v1/api"

requests.packages.urllib3.disable_warnings()

def searchBySymbol(symbol: str, sectype: str):
    data = {
            "symbol": symbol,
            "name": True,
            "secType": sectype,
            }
    resp = requests.post(base_url + "/iserver/secdef/search", json=data, verify=False)
    if resp.status_code == 200:
        jsonData = json.loads(resp.text)
        contract = jsonData[0]
        print(f"---> Received contract details for {symbol}")
        return contract 
    else:
        raise RuntimeError(f"Nothing found for symbol {symbol}")

def getOptionStrikes(conid, month, exchange=None, secType=None):
    url = "/iserver/secdef/strikes"
    params = {"conid": conid, "sectype": "OPT" if secType is None else secType
            , "month": month,
            "exchange": '' if exchange == None else exchange}
    response = requests.get(base_url + url, params=params, verify=False)
    jsonData = json.loads(response.text)
    return jsonData

def testOptionsContrac(conid, month, right, strike, exchange=None, secType=None):
    url = "/iserver/secdef/info"
    params = {
            "conid": conid,
            "secType": "OPT" if secType is None else secType, 
            "month": month,
            "exchange": 'SMART' if exchange == None else exchange,
            "strike": strike,
            "right": right 
            }
    response = requests.get(base_url + url, params=params, verify=False)
    jsonData = json.loads(response.text)
    print(json.dumps(jsonData, indent=4))

def getFOPcontracts():
    details = searchBySymbol("ES", "STK")
    sections = details['sections']
    for s in sections:
        if s['secType'] == "FOP":
            fopMonths = s['months']
            print(fopMonths)
            for m in fopMonths:
                strikesPerMonth = getOptionStrikes(conid=details['conid'], month=m, exchange="CME", 
                        secType="FOP")
                for s in strikesPerMonth['call']:
                    print(s)
                    testOptionsContrac(conid=details['conid'], right='C',
                            month=m, strike=s, exchange="CME", secType="FOP")

                for s in strikesPerMonth['put']:
                    print(s)
                    testOptionsContrac(conid=details['conid'], right='P',
                            month=m, strike=s, exchange="CME", secType="FOP")
            break
        else:
            print('Not FOP :(')

if __name__ == "__main__":
    getFOPcontracts()
