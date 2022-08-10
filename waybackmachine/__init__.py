# -*- coding: utf-8 -*-
"""Webscraper for WaybackMachine.

Archive URL: https://archive.org/web/
Todo:
    * caching
"""

import pkg_resources
from .browse import browse
from .fetch import fetch
from ._common import WaybackMachineRecord, WaybackMachineError

try:
    __version__ = pkg_resources.get_distribution("waybackmachine").version
except:
    __version__ = None

__all__ = ["browse", "fetch", "WaybackMachineRecord", "WaybackMachineError"]