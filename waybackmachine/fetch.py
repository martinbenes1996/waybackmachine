
from datetime import datetime,timedelta,date
import json
import logging
import re
import requests

class Fetcher:
    def __init__(self, url, dt):
        self._log = logging.getLogger(self.__class__.__name__)
        self._url = url
        self._dt = dt
    def __call__(self):
        self._log.debug(f"GET: {self._url}")
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
        self._log = logging.getLogger(self.__class__.__name__)
        self._url = url
        # parse config
        try:
            self._start, self._end, self._step = [i() for i in self._config[config]]
        except:
            self._start, self._end, self._step = [i() for i in self._config[ 'default' ]]
        # parse explicit settings
        if start is not None: self._start = self._parse_datetime(start)
        if end is not None: self._end = self._parse_datetime(end)
        if step is not None: self._step = self._parse_timedelta(step)
        # set start
        self._now = self._start
        self._responses = True
    def now(self):
        return self._now
    def start(self):
        return self._start
    def end(self):
        return self._end
    def step(self):
        return self._step
    def yield_fetchers(self, yi = True):
        self._responses = not yi
        
    def __iter__(self):
        # yield date sequence from archive
        versions = set()
        while self._now > self._end:
            self._log.info(f"searching in time {self._now.strftime('%Y-%m-%d %H:%M:%S')}")
            # get older version
            archive_url = self._construct_archive_url(self._now)
            version_url,version_time = self._fetch_archive(archive_url)
            #print(self._now, version_time)
            if version_time < self._end:
                break
            if version_time not in versions:
                versions.add(version_time)
                self._log.info(f"Found ({version_time}) {self._url}")
                if self._responses:
                    with Fetcher(version_url, version_time) as response:
                        yield response, version_time
                else:
                    yield Fetcher(version_url, version_time)
                if version_time < self._now:
                    self._now = version_time
            self._now -= self._step
            
    def _construct_archive_url(self, dt = None):
        archive_url = f"http://archive.org/wayback/available?url={self._url}"
        if dt is not None:
            archive_url += f"&timestamp={ dt.strftime('%Y%m%d') }"
        return archive_url
    def _fetch_archive(self, archive_url):
        # fetch
        connection_fail = False
        try:
            response = requests.get(archive_url)
        except:
            connection_fail = True
        if connection_fail:
            raise WaybackMachineError("failed connecting to archive")
        try:
            x = json.loads(response.text)['archived_snapshots']['closest']
            # parse
            return x['url'],datetime.strptime(x['timestamp'], "%Y%m%d%H%M%S")
        except:
            pass
        raise WaybackMachineError("error parsing archive response")
    
    @staticmethod
    def _parse_datetime(dt):
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
    def _parse_timedelta(td):
        if isinstance(td, timedelta):
            return td
        #elif isinstance(td, str):
        #    # todo
        #    return timedelta(days = 24)
        elif isinstance(td, float) or isinstance(td, int):
            return timedelta(seconds = td)
        else:
            raise TypeError("invalid input timedelta type")

__all__ = ["Fetcher","WaybackMachine"]