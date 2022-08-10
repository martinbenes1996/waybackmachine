
import dataclasses
from datetime import datetime, timedelta
import logging
import re
import urllib.parse

import requests
from ._common import parse_datetime

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

def fetch_summary(url:str):
    url = urllib.parse.quote_plus(url)
    archive_url = f"https://web.archive.org/__wb/sparkline?output=json&url={url}&collection=web"
    referer = f"https://web.archive.org/web/{datetime.now().year}0000000000*/{url}"
    # fetch
    try:
        response = requests.get(archive_url, headers={'referer': referer})
    # on fail
    except:
        raise WaybackMachineError("failed fetching recording meta")
    # parse datetimes
    try:
        res = response.json()
    except:
        raise WaybackMachineError("failed parsing JSON response")
    if not res:
        return {}, None, None
    return (
        res['years'],
        datetime.strptime(res['first_ts'], '%Y%m%d%H%M%S'),
        datetime.strptime(res['last_ts'], '%Y%m%d%H%M%S'),
    )

def fetch_current(url:str) -> WaybackMachineRecord:
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


def fetch_closest_archived(url:str, date:datetime) -> WaybackMachineRecord:
    """Fetch archived website version, closest to the given time.

    Args:
        url (str): Page URL.
        date (datetime): Datetime of version.
    """
    # construct archive url
    url = urllib.parse.quote_plus(url)
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

def fetch_archived(url:str, date:datetime):
    """"""
    # construct archive url
    url = urllib.parse.quote_plus(url)
    archive_url = f"https://web.archive.org/__wb/calendarcaptures/2?url={url}&date={date.strftime('%Y%m%d')}"
    # fetch
    try:
        response = requests.get(archive_url)
    # on error
    except:
        raise WaybackMachineError("failed connecting to archive")
    # parse datetimes
    try:
        res = response.json()
    except:
        raise WaybackMachineError("failed parsing JSON response")
    if not res:
        return []
    return sorted([
        datetime.strptime(
            f"{date.strftime('%Y%m%d')} {i[0]:06d}",
            '%Y%m%d %H%M%S'
        )
        for i in res['items']
    ], reverse=True)

# 'https://web.archive.org/__wb/sparkline?output=json&url=mbenes.me&collection=web'

def browse(
    url:str,
    start:datetime=None,
    end:datetime=datetime(2000,1,1),
):
    """Browse pages from archive.

    Args:
        url (str): Page URL.
        start (datetime): Start datetime for browsing. From current by default.
        end (datetime): End datetime for browsing. 1st January 2000 by default.
    """
    # parse
    start = parse_datetime(start)
    end = parse_datetime(end)
    # fetch summary
    years, last, first = fetch_summary(url)
    if start < first:
        start = first
    if last > end:
        end = last - timedelta(days=1)
    # print(start, end)
    # print(years)
    # get current version
    if start is None:
        yield fetch_current(url)
        current = datetime.now()
    # skip current version
    else:
        current = start
    # yield date sequence from archive
    versions = set()
    # this_month = {}
    while current >= end:
        # get screenshots
        screenshots = fetch_archived(url, current)
        for dt in screenshots:
            # get screenshot
            record = fetch_closest_archived(url, dt)
            if record.date > start or record.date < end:
                break
            if record.date not in versions:
                versions.add(record.date)
                # logging.info(f"Found version from {record.date.strftime('%Y-%m-%d %H:%M:%S')}")
                yield record
                if not current or record.date < current:
                    current = record.date

            # TODO: check if not to skip the rest of the month

            # # accumulate month stats
            # year_s = current.strftime('%Y')
            # month_i = int(current.strftime('%m'))-1
            # if year_s not in this_month:
            #     this_month[year_s] = {}
            # if month_i not in this_month[year_s]:
            #     this_month[year_s][month_i] = 0
            # this_month[year_s][month_i] += 1
            # if years[year_s][month_i] == this_month[year_s][month_i]:

        current -= timedelta(days=1)



__all__ = ["browse"]