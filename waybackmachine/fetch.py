
from datetime import datetime,timedelta,date
import json
import logging
import re

import requests
    
class WaybackMachineError(Exception):
    def __init__(self, msg):
        self._msg = msg
    def __str__(self):
        return self._msg

# 'https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Poland'
# 'https://www.gov.pl/web/koronawirus/wykaz-zarazen-koronawirusem-sars-cov-2'
class WaybackMachine:
    _config = {
        'default': (lambda: None, lambda: datetime(datetime.now().year, 1, 1), lambda: timedelta(days = 1)),
        'covid': (lambda: None, lambda: datetime(2020,1,1), lambda: timedelta(hours = 12))
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
    def now(self):
        return self._now
    def start(self):
        return self._start
    def end(self):
        return self._end
    def step(self):
        return self._step
        
    def __iter__(self):
        # yield date sequence from archive
        versions = set()
        while self._now > self._end:
            self._log.info(f"searching in time {self._now.strftime('%Y-%m-%d %H:%M:%S')}")
            # get older version
            archive_url = self._construct_archive_url(self._now)
            html,version_time = self._fetch_archive(archive_url)
            #print(self._now, version_time)
            if version_time < self._end:
                break
            if version_time not in versions:
                versions.add(version_time)
                self._log.info(f"Found version from {version_time}")
                yield html, version_time
                if not self._now or version_time < self._now:
                    self._now = version_time
            self._now -= self._step
            
    def _construct_archive_url(self, dt = None):
        #archive_url = f"http://archive.org/wayback/available?url={self._url}"
        #if dt is not None:
        #    archive_url += f"&timestamp={ dt.strftime('%Y%m%d') }"
        #return archive_url
        dt = f"/{dt.strftime('%Y%m%d%H%M%S')}" if dt else ""
        archive_url = f"http://web.archive.org/web{dt}/{self._url}"
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
        #try:
        #    x = json.loads(response.text)['archived_snapshots']['closest']
        #    # parse
        #    return x['url'],datetime.strptime(x['timestamp'], "%Y%m%d%H%M%S")
        #except:
        #    pass
        try:
            dt = re.search(r'^http://web\.archive\.org/web/([0-9]+)/.*', response.url).group(1)
            return response.text, datetime.strptime(dt, "%Y%m%d%H%M%S")
        except: pass
        raise WaybackMachineError("error parsing archive response")
    
    @staticmethod
    def _parse_datetime(dt):
        if dt is None:
            return dt
        elif isinstance(dt, datetime):
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

__all__ = ["WaybackMachine"]