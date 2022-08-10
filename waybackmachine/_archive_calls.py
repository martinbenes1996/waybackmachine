
from datetime import datetime
import requests
from typing import Union

from ._common import WaybackMachineError, to_urlencode

def _summary(url:str):
    url = to_urlencode(url)
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

def _year_day_records(url:str, year:Union[str,int]):
    url = to_urlencode(url)
    archive_url = f"https://web.archive.org/__wb/calendarcaptures/2?url={url}&date={year}&groupby=day"
    # fetch
    try:
        response = requests.get(archive_url)
    # on fail
    except:
        raise WaybackMachineError("failed fetching recording meta")
    # parse datetimes
    try:
        res = response.json()
    except:
        raise WaybackMachineError("failed parsing JSON response")
    if not res:
        return []
    return sorted([
        datetime.strptime(
            f"{year}{i[0]:04d} 000000",
            '%Y%m%d %H%M%S'
        )
        for i in res['items']
    ], reverse=True)

def _archived(url:str, date:datetime):
    """"""
    # construct archive url
    url = to_urlencode(url)
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