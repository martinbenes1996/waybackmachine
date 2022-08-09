
import dataclasses
from datetime import datetime, timedelta
import logging
import re

import requests
from ._common import parse_datetime, parse_timedelta

class WaybackMachineError(Exception):
    def __init__(self, msg):
        self._msg = msg
    def __str__(self):
        return self._msg

@dataclasses.dataclass
class WaybackMachineRecord:
    date:datetime
    url:str
    response:requests.Response

def fetch_current(url):
    """Fetches current version of the page."""
    logging.info("fetching current version")
    # fetch
    try:
        response = requests.get(url)
    # on fail
    except:
        raise WaybackMachineError("failed fetching current version")
    # return
    return WaybackMachineRecord(
        date=datetime.now(),
        url=url,
        response=response,
    )

def fetch_closest_archived(url:str, date:datetime):
    """Fetch archive at given time."""
    # construct archive url
    archive_url = f"http://web.archive.org/web/{date.strftime('%Y%m%d%H%M%S')}/{url}"
    # fetch
    try:
        response = requests.get(archive_url)
    # on error
    except:
        raise WaybackMachineError("failed connecting to archive")
    try:
        dt = re.search(r'^http://web\.archive\.org/web/([0-9]+)/.*', response.url).group(1)
        return WaybackMachineRecord(
            date=datetime.strptime(dt, "%Y%m%d%H%M%S"),
            url=archive_url,
            response=response,
        )
    except:
        raise WaybackMachineError("error parsing archive response")


def browse(
    url:str,
    start:datetime=None,
    end:datetime=datetime(2000,1,1),
    step:timedelta=timedelta(days=1),
):
    """Browse pages from archive.

    Args:
        url (str): Page URL.
        start (datetime): Start datetime for browsing. From current by default.
        end (datetime): End datetime for browsing. 1st January 2000 by default.
        step (timedelta): Step for searching. 1 day by default.
    """
    # parse
    start = parse_datetime(start)
    end = parse_datetime(end)
    step = parse_timedelta(step)
    # now
    current = start
    # get current version
    if start is None:
        yield fetch_current(url)
        current = datetime.now()
    # yield date sequence from archive
    versions = set()
    while current > end:
        logging.info(f"searching archive {current.strftime('%Y-%m-%d %H:%M:%S')}")
        # get older version
        record = fetch_closest_archived(url, current)
        if record.date < end:
            break
        if record.date not in versions:
            versions.add(record.date)
            logging.info(f"Found version from {record.date.strftime('%Y-%m-%d %H:%M:%S')}")
            yield record
            if not current or record.date < current:
                current = record.date
        current -= step



__all__ = ["browse"]