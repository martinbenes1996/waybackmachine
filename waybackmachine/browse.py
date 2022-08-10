
from datetime import datetime, timedelta
import logging


from ._common import parse_datetime
from . import _archive_calls as ac
from . import fetch


def browse(
    url:str,
    start:datetime=None,
    end:datetime=None,
):
    """Browse pages from archive.

    Args:
        url (str): Page URL.
        start (datetime): Start datetime for browsing. From current by default.
        end (datetime): End datetime for browsing. 1st January 2000 by default.
    """
    # parse
    start = parse_datetime(start, on_none=datetime.now())
    end = parse_datetime(end, on_none=datetime(2000,1,1))
    # fetch summary
    years, _, _ = ac._summary(url)
    versions = set()
    for year in map(int, sorted(years.keys(), key=int, reverse=True)):

        # too early - skip
        if year > start.year:
            continue

        # get year records
        for day in ac._year_day_records(url, year):

            # too early - skip
            if day > start:
                continue
            # too late - end
            if day < end:
                return

            # iterate screenshots of the day
            for screenshot in ac._archived(url, day):
                record = fetch.fetch(url, screenshot)
                if record.date not in versions:
                    versions.add(record.date)
                    logging.info(f"Found version from {record.date.strftime('%Y-%m-%d %H:%M:%S')}")
                    yield record
    return



__all__ = ["browse"]