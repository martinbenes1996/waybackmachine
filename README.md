[![PyPI version](https://badge.fury.io/py/waybackmachine.svg)](https://pypi.org/project/waybackmachine/)
[![PyPI downloads](https://img.shields.io/pypi/dm/waybackmachine)](https://pypi.org/project/waybackmachine/)
[![Stars](https://img.shields.io/github/stars/martinbenes1996/waybackmachine.svg)](https://GitHub.com/martinbenes1996/waybackmachine)
[![Contributors](https://img.shields.io/github/contributors/martinbenes1996/waybackmachine)](https://GitHub.com/martinbenes1996/waybackmachine)
[![Wheel](https://img.shields.io/pypi/wheel/waybackmachine)](https://pypi.org/project/waybackmachine/)
[![Status](https://img.shields.io/pypi/status/waybackmachine)](https://pypi.com/project/waybackmachine/)
[![PyPi license](https://badgen.net/pypi/license/pip/)](https://pypi.com/project/waybackmachine/)
[![Last commit](https://img.shields.io/github/last-commit/martinbenes1996/waybackmachine)](https://GitHub.com/martinbenes1996/waybackmachine)

# Wayback Machine

This project is an envelope for simple fetching of historical versions of page from archive.org API.

The page can be used for subsequent webscraping

## Setup and usage

Install from [pip](https://pypi.org/project/waybackmachine/) with

```python
pip install waybackmachine
```

To fetch the latest version from archive, simply use `fetch()` function.

```python
import waybackmachine as wm

url = "https://en.wikipedia.org/wiki/COVID-19"
latest = wm.fetch(url)
latest.response  # requests.Response
latest.date  # capture time
latest.url  # url
```

Optionally you can specify date. The first version after this date is chosen.

```python
may2020 = wm.fetch(url, date="2020-05-01")
```

### Browsing

You can also iterate archived versions backwards in time.

```python
for version in wm.browse(url):
    version.response  # requests.Response
    version.date  # capture time
    version.url  # url
```

This will iterate the screenshots from [archive.org](https://archive.org/).

You can specify a custom date range as follows.

```python
for version in wm.browse(url, start='2020-06-30', end='2020-03-01'):
    pass
```


## Contribution

Developed by [Martin Benes](https://github.com/martinbenes1996).

Join on [GitHub](https://github.com/martinbenes1996/waybackmachine).



