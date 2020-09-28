# Monorail / Chromium Issue Scraper

## What this is

Right now it scrapes bugs.chromium.com for issues, however it can (and  eventually will be) adapted to a general purpose monorail scraper. This was a project I was working on but quickly uploaded due to the permissions bug in monorail.

## Interesting Tidbits

A few main things to note here are the X-XSRF token and that the response comes back as malformed JSON, site is running on Monorail

## Basic Usage

I tried to make sure there weren't any dependencies so this could just be dropped in and used. The query builder function below accepts many different arguments corresponding to the advanced search feature located [here](https://bugs.chromium.org/p/chromium/issues/advsearch). All arguments are expected as space delimited.

```python
from scraper import Scraper

scrape = Scraper()

query = scrape.query_builder(with_string="v8", num_items=1000)

json_results = scrape.search(query)

print(json_results)
```

## Getting Issues, Comments and Attachments

The get_all() function will go a step further and return all issues with their relevant comments and attachments. This is especially useful for getting PoC's before they are triaged and hidden.

```python
from scraper import Scraper

scrape = Scraper()

# grabs any issues with id > 1132000
query = scrape.query_builder(with_string="id>1132000", num_items=100000)

json_results = scrape.get_all(query)

print(json_results)
```

## Advanced Usage

### Raw Query

More advanced tips and tricks on using the search can be found [here](https://bugs.chromium.org/p/chromium/issues/searchtips). If you're a veteran with the search, feel limited by the query_builder, or just want to try some new things you learned from the previous link, try the raw_query as shown below:

```python
from scraper import Scraper

scrape = Scraper()

query = scrape.raw_query('"out of memory" summary:v8')

json_results = scrape.search(query)

print(json_results)
```

