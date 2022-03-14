"""
Name: tester
Author: Ryan Parker
Created: 2019-12-03
Purpose:
"""


import os
import requests


def getHelper():
    helperFunctions = os.path.join(os.path.dirname(__file__), "helperFunctions.py")
    url = "https://raw.githubusercontent.com/gsc-permafrost/00_helperScripts/master/helperFunctions.py"
    if not os.path.exists(helperFunctions):
        print "Getting helper functions"
        r = requests.get(url)
        with open(helperFunctions, 'wb') as f:
            f.write(r.content)
        print "DONE!"
    return

