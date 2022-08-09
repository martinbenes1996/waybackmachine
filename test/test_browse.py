
import logging
import requests
import unittest

# tested component
import waybackmachine

class TestBrowse(unittest.TestCase):

    def test_response(self):
        archive_browser = waybackmachine.browse(
            'https://en.wikipedia.org/wiki/COVID-19',
            start = "2022-08-01", end = "2022-07-01"
        )
        previous = None
        for record in archive_browser:
            # logging.info(record.date)
            # check date order
            if previous is not None:
                self.assertLess(record.date, previous)
            previous = record.date
            # check status
            self.assertIsInstance(record.response, requests.Response)

    #def test_now(self):
    #    print("test_now")
    #    x = WaybackMachine(
    #        'https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/bekraftade-fall-i-sverige/')
    #    print(x._now)
    #    for response,version_date in x:
    #        now = datetime.now()
    #        self.assertLess(abs(version_date - now), timedelta(days = 7))
    #        break

