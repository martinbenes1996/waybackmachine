
from datetime import datetime, timedelta
import requests
import sys
import unittest

# tested component
sys.path.append(".")
from waybackmachine import WaybackMachine

class TestIterate(unittest.TestCase):
    
    def test_response(self):
        x = WaybackMachine(
            'https://www.gov.pl/web/koronawirus/wykaz-zarazen-koronawirusem-sars-cov-2',
            start = "2020-05-01", end = "2020-04-20")
        previous = None
        for response,version_date in x:
            # check date order
            if previous is not None:
                self.assertLess(version_date, previous)
            previous = version_date
            # check status
            self.assertIsInstance(response, requests.Response)
    
    #def test_now(self):
    #    print("test_now")
    #    x = WaybackMachine(
    #        'https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/bekraftade-fall-i-sverige/')
    #    print(x._now)
    #    for response,version_date in x:
    #        now = datetime.now()
    #        self.assertLess(abs(version_date - now), timedelta(days = 7))
    #        break
            
        