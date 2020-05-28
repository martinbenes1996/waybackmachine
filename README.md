
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

url = "https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/bekraftade-fall-i-sverige/"
for response in WaybackMachine(url):
    # process response
    pass
```

In the code the requests are being done from the newest (to the url itself) and then back in history to older and older versions saved on archive.

Parameterization will be later broaden to be more general. Currently the project is used for fetching COVID-19 data.

```bash
pip install --upgrade waybackmachine
```

## Parametrization

### date

By default the start date is `today`. End date is currently set to `2020-03-01`.

Date will be more general in the future.

```python
from waybackmachine import WaybackMachine

url = "https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/bekraftade-fall-i-sverige/"

for response in WaybackMachine(url, "2020-04-01"): # start from 1st April 2020 and go back
    # process response
    pass
```

## Contribution

Developed by [Martin Benes](https://github.com/martinbenes1996).

Join on [GitHub](https://github.com/martinbenes1996/waybackmachine).



