#! /usr/bin/env python3

import json
import sys
from exceptions import * 

rejectionReasons = open('errors/rejectionReasons.txt', 'r').read().split('\n')


def errorHandler(responseJSON):

    if responseJSON['error'] == 'No trading permissions.':
        raise NoTradingPermissionError

    if responseJSON['error'].startswith('java.lang.Exception'):
        raise JavaLangException

    if responseJSON['error'] == "Too many history charts requests, please try again later.":
        raise TooManyHistoricalRequests

    try:

        rsn = responseJSON['cqe']['post_payload']['rejections']
        print("Known rejection reasons: \n", rejectionReasons)
        for r in rsn:
            if r not in rejectionReasons:
                with open('errors/rejectionReasons.txt', 'a') as outFile:
                    print("NEW REJECTION REASON")
                    print(f"REASON: {responseJSON['cqe']['post_payload']['rejections']}")
                    outFile.write(r + '\n')

        raise OrderRejectedDueToReasons

    except KeyError:
        pass


    else:
        print("NEW ERROR MESSAGE")
        print("###########################")
        # Write error message to output
        with open('errors/knownErrors.json', 'a') as outFile:
            json.dump(responseJSON, outFile, indent=4)
        sys.exit()
