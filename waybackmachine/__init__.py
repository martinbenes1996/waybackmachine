# -*- coding: utf-8 -*-
"""Webscraper for WaybackMachine.

Archive URL: https://archive.org/web/
Todo:
    * caching
"""

import pkg_resources
from .fetch import browse, WaybackMachineRecord, WaybackMachineError

try:
    __version__ = pkg_resources.get_distribution("waybackmachine").version
except:
    __version__ = None