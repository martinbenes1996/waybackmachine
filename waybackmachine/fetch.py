
from datetime import datetime
import logging
import re
import requests

from ._common import WaybackMachineError, WaybackMachineRecord, to_urlencode
from . import _archive_calls as ac

def _get_latest_version_date(url:str) -> WaybackMachineRecord:
    """Returns the date of the latest version in archive."""
    logging.info("fetching latest version")
    _, _, latest = ac._summary(url)
    return latest
def fetch(url:str, date:datetime=None) -> WaybackMachineRecord:
    """Fetch archived website version, closest to the given time.

    Args:
        url (str): Page URL.
        date (datetime): Datetime of version.
    """
    # latest archived version
    if date is None:
        date = _get_latest_version_date(url)
    # construct archive url
    url = to_urlencode(url)
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



__all__ = ["fetch_closest", "fetch_current", "fetch_latest"]
