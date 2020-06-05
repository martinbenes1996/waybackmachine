
from datetime import datetime,timedelta,date
import json
import re
import requests

class Fetcher:
    def __init__(self, url, dt):
        self._url = url
        self._dt = dt
    def __call__(self):
        self._response = requests.get(self._url)
        return self._response
    def __enter__(self):
        try:
            return self._response
        except:
            return self()
    def __exit__(self, type, value, traceback):
        pass
        #print("Type:", type)
        #print("Value:", value)
        #print("Traceback:", traceback)
    # getters
    def url(self): return self._url
    def date(self): return self._dt
    
class WaybackMachineError(Exception):
    def __init__(self, msg):
        self._msg = msg
    def __str__(self):
        return self._msg

# 'https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Poland'
# 'https://www.gov.pl/web/koronawirus/wykaz-zarazen-koronawirusem-sars-cov-2'
class WaybackMachine:
    _config = {
        'default': (datetime.now, lambda : datetime(datetime.now().year, 1, 1), lambda : timedelta(days = 1)),
        'covid': (datetime.now, lambda : datetime(2020,1,1), lambda : timedelta(hours = 12))
    }
    def __init__(self, url, start = None, end = None, step = None, config = 'default'):
        self._url = url
        # parse config
        try:
            self._start, self._end, self._step = [i() for i in self._config[config]]
        except:
            self._start, self._end, self._step = [i() for i in self._config[ 'default' ]]
        # parse explicit settings
        if start is not None: self._start = self._parse_datetime(start)
        if end is not None: self._end = self._parse_datetime(end)
        if step is not None: self._step = self._parse_datetime(step)
        # set start
        self._now = self._start
    def now(self):
        return self._now
    def start(self):
        return self._start
    def end(self):
        return self._end
    def step(self):
        return self._step
        
    def __iter__(self):
        # yield real url
        with Fetcher(self._url, self._now) as response:
            yield response
        # yield date sequence from archive
        dt = self._now
        versions = set()
        while dt > datetime(2020,3,1):
            dt -= timedelta(hours = 12)
            # get older version
            archive_url = self._construct_archive_url(dt)
            url,url_dt = self._fetch_archive(archive_url)
            print(dt, url_dt)
            if url_dt not in versions:
                versions.add(url_dt)
                with Fetcher(url, url_dt) as response:
                    yield response
            if url_dt < dt:
                dt = url_dt
            
    def _construct_archive_url(self, dt = None):
        archive_url = f"http://archive.org/wayback/available?url={self._url}"
        if dt is not None:
            archive_url += f"&timestamp={ dt.strftime('%Y%m%d') }"
        return archive_url
    def _fetch_archive(self, archive_url):
        # fetch
        try:
            response = requests.get(archive_url)
        except:
            raise WaybackMachineError("failed connecting to archive")
        try:
            x = json.loads(response.text)['archived_snapshots']['closest']
            # parse
            return x['url'],datetime.strptime(x['timestamp'], "%Y%m%d%H%M%S")
        except:
            raise WaybackMachineError("error parsing archive response")
    
    @staticmethod
    def _parse_datetime(self, dt):
        if isinstance(dt, datetime):
            return dt
        elif isinstance(dt, date):
            return datetime(dt.year, dt.month, dt.day)
        elif isinstance(dt, str):
            for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"]:
                try:
                    dt = datetime.strptime(dt, fmt)
                    return dt
                except:
                    pass
            else:
                raise ValueError("invalid input date string format")
        else:
            raise TypeError("invalid input date type")
    @staticmethod
    def _parse_timedelte(self, td):
        if isinstance(td, timedelta):
            return td
        elif isinstance(td, str):
            # ...
            return timedelta(days = 24)
        elif isinstance(td, float) or isinstance(td, int):
            return timedelta(seconds = td)
        else:
            raise TypeError("invalid input timedelta type")

__all__ = ["Fetcher","WaybackMachine"]