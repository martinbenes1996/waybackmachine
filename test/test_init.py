
from datetime import datetime, timedelta
import sys
import unittest

# tested component
sys.path.append(".")
from waybackmachine import WaybackMachine

class TestInit(unittest.TestCase):
    _datetime_eps = timedelta(seconds = 5)
    def assertDatetimeEqual(self, t1, t2):
        self.assertLessEqual(abs(t1 - t2), self._datetime_eps)
        
    def test_nourl(self):
        self.assertRaises(TypeError, WaybackMachine)
    def test_constructor(self, *args, **kwargs):
        # constructing
        try:
            x = WaybackMachine('https://www.gov.pl/web/koronawirus/wykaz-zarazen-koronawirusem-sars-cov-2', *args, **kwargs)
            now = datetime.now()
        except Exception as e:
            raised = True
            self.assertFalse(raised)
            return
        # end
        self.assertIsInstance(x.end(), datetime)
        # step
        self.assertIsInstance(x.step(), timedelta)
        return x, now
    
    def test_configuration_default(self):
        # default configuration
        x,now = self.test_constructor(config = 'default')
        # === test ===
        # now, start == datetime.now()
        self.assertTrue(x.now() is None)
        self.assertTrue(x.start() is None)
        # end == beginning of current year
        self.assertDatetimeEqual(x.end(), datetime(now.year,1,1))
        # step == 1 day
        self.assertEqual(x.step(), timedelta(days = 1))
        
    def test_configuration_covid(self):
        # default configuration
        x,now = self.test_constructor(config = 'covid')
        # === test ===
        # now, start == None
        self.assertTrue(x.now() is None)
        self.assertTrue(x.start() is None)
        # end == 1st January 2020
        self.assertDatetimeEqual(x.end(), datetime(2020,1,1))
        # step == 12h
        self.assertEqual(x.step(), timedelta(hours = 12))
        
    def test_explicit(self):
        # explicit values over default configuration
        x,now = self.test_constructor(start = datetime(2020,5,1), config = 'default')
        # ...
    
    def test_datetime_format(self):
        # string date values
        x,now = self.test_constructor(start = "2020-11-22", end = "2020-01-01 08:00", config = 'default')
        start = datetime(2020, 11, 22)
        end = datetime(2020, 1, 1, 8)
        # === test ===
        # now, start == datetime.now()
        self.assertDatetimeEqual(x.now(), start)
        self.assertDatetimeEqual(x.start(), start)
        # end == 1st January 2020
        self.assertDatetimeEqual(x.end(), end)
        # step == 12h
        self.assertEqual(x.step(), timedelta(days = 1))
        
        
            