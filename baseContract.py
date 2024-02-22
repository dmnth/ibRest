#! /usr/bin/env python3

contractString = """
        # Provide only conid or conidex field
        self.conid = ''
        self.conidex = ''
        self.symbol = ''
        self.secType = ''
        self.currency = ''
        self.exchange = ''
        self.ticker = ''
        self.multiplier = int() 
        self.lastTradeDateOrContractMonth = ''
        self.locaSymbol = ''
        self.JSON = {}
        """

class Contract:

    def __init__(self, conid, exchange="SMART", tif="GTC"):
        self.exchange = exchange
        self.conid = conid
        self.tif = tif

    def __repr__(self):
        return "Basic contract sample"

