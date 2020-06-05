
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
from waybackmachine import WaybackMachine

url = "https://www.gov.pl/web/koronawirus/wykaz-zarazen-koronawirusem-sars-cov-2"
for response in WaybackMachine(url):
    # process response
    pass
```

The iterated version goes from newest to the older and older version all the way to end date at given step of date axis for querying the archive.

Update of package is done with

```bash
pip install --upgrade waybackmachine
```

### Start, end and step configuration

Library enables setting of start date, end date and step size as timedelta.

Since iterating is done backwards in time, **end date precedes start date!**

Setting the querying for weekly from 1st May back to 1st February 2020 is done with

```python
from datetime import datetime,timedelta
from waybackmachine import WaybackMachine

url = "https://www.liu.se/"
for response in WaybackMachine(url, start = datetime(2020,5,1), end = datetime(2020,2,1), step = timedelta(days = 7)):
    # process response
    pass
```

The date can be also specified one of following string formats:

* *%Y-%m-%d*
* *%Y-%m-%d %H:%M*
* *%Y-%m-%d %H:%M:%S*

```python
for response in WaybackMachine(url, start = "2020-05-01", end = "2020-02-01", step = timedelta(days = 7)):
    # process response
    pass
```

*String representation of timedelta will be added.*



### Configurations

On frequent use-cases, custom configurations of parameters are added to the packages.

These consist of default parameter values.

So far following configurations are available:

* *default* - start is *now()*, end is beginning of year of start (hence length can be 0 - 365 days), 1 day step
* *covid* - start is *now()* (might be changed, if covid disappears), end is *2020-01-01*, COVID-19 spread into the world after. *In China the COVID-19 has already occurred before!*. Step is 12 h.
 
## Contribution

Developed by [Martin Benes](https://github.com/martinbenes1996).

Join on [GitHub](https://github.com/martinbenes1996/waybackmachine).



