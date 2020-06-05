
from datetime import datetime, timedelta
import sys
import unittest

# tested component
sys.path.append(".")
from waybackmachine import WaybackMachine

class TestIterate(unittest.TestCase):
    def test_fetcher(self):
        x = WaybackMachine(
            'https://www.gov.pl/web/koronawirus/wykaz-zarazen-koronawirusem-sars-cov-2',
            start = "2020-05-01", end = "2020-04-15")
        x.yield_fetchers()
        
        previous = None
        for fetcher in x:
            if previous is None:
                previous = fetcher
            else:
                self.assertGreater(previous.date(), fetcher.date())
        