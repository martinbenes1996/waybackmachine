
# Wayback Machine

This project is an envelope for simple fetching of historical versions of page from archive.org API.

The page can be used for subsequent webscraping

## Setup and usage

Install from [pip](https://pypi.org/project/waybackmachine/) with

```python
pip install waybackmachine
```

Simple usage of the `WaybackMachine` class is as

```python
import waybackmachine as wm

url = "https://en.wikipedia.org/wiki/COVID-19"
for version in wm.browse(url):
    version.response  # requests.Response
    version.date  # capture time
    version.url  # url
```

This will iterate the current version, followed by screenshots from [archive.org](https://archive.org/).
Avoid returning the current (live) version.

```python
from datetime import datetime
for version in wm.browse(url, start=datetime.now()):
    pass
```

You can specify a custom date range as follows.

```python
for version in wm.browse(url, start=datetime(2020,6,30), end=datetime(2020,3,1)):
    pass
```


## Contribution

Developed by [Martin Benes](https://github.com/martinbenes1996).

Join on [GitHub](https://github.com/martinbenes1996/waybackmachine).



