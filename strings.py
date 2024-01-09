#! /usr/bin/env python3

import json

string1 = {'tickers': [{'ticker': 'AAPL', 'cspposition': 0, 'ccposition': 1.0, 'stkposition': 122.2749}, {'ticker': 'MSFT', 'cspposition': 1.0, 'ccposition': 0, 'stkposition': 0}, {'ticker': 'AMD', 'cspposition': 0, 'ccposition': 0, 'stkposition': -1.9404}, {'ticker': 'AMZN', 'cspposition': 0, 'ccposition': 2.0, 'stkposition': 127.4625}, {'ticker': 'NVDA', 'cspposition': 2.0, 'ccposition': 0, 'stkposition': -20.5821}]}

string2 = {'tickers': [{'ticker': 'AAPL', 'cspposition': 0, 'ccposition': 1.0, 'stkposition': 122.1749}, {'ticker': 'MSFT', 'cspposition': 1.0, 'ccposition': 0, 'stkposition': 0}, {'ticker': 'AMD', 'cspposition': 0, 'ccposition': 0, 'stkposition': -1.9404}, {'ticker': 'AMZN', 'cspposition': 0, 'ccposition': 2.0, 'stkposition': 127.4625}, {'ticker': 'NVDA', 'cspposition': 2.0, 'ccposition': 0, 'stkposition': -20.5821}]}

print(string1 == string2)

for el in range(len(string1['tickers'])):
    result = string1['tickers'][el] == string2['tickers'][el]
    if result == False:
        print(string1['tickers'][el] , "\n" , string2['tickers'][el])
        break
