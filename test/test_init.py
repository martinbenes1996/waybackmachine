
import sys
import unittest

# tested component
sys.path.append(".")
from waybackmachine import WaybackMachine

class TestInit(unittest.TestCase):
    def test_nourl(self):
        self.assertRaises(TypeError, WaybackMachine)
    def test_url(self):
        # constructing
        raised = False
        try: x = WaybackMachine('https://www.gov.pl/web/koronawirus/wykaz-zarazen-koronawirusem-sars-cov-2')
        except: raised = True
        self.assertFalse(raised)
        
        
            