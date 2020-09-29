# Monorail / Chromium Issue Scraper

## What this is

Right now it scrapes bugs.chromium.com for issues, however it can (and  eventually will be) adapted to a general purpose monorail scraper.

## Interesting Tidbits

A few main things to note here are the X-XSRF token (which you absolutely need to get your responses back). Also the response comes back as malformed JSON so I had to just skip a few characters, [apparently to prevent some nefariousness](https://chromium.googlesource.com/infra/infra/+/master/appengine/monorail/static/js/framework/framework-ajax.js). Speaking of which, all monorail source code is located [here](https://chromium.googlesource.com/infra/infra/+/master/appengine/monorail) if you're interested in looking at it.

## Usage

### Basic Usage

I tried to make sure there weren't any dependencies so this could just be dropped in and used. The query builder function below accepts many different arguments corresponding to the advanced search feature located [here](https://bugs.chromium.org/p/chromium/issues/advsearch). All arguments are expected as space delimited.

```python
from scraper import Scraper
import json

scrape = Scraper()

query = scrape.query_builder(num_items=1000, with_strings="v8")
output = scrape.search(query)

print(json.dumps(output))
```

### Getting Issues, Comments and Attachments

The get_all() function will go a step further and return all issues with their relevant comments and attachments. This is especially useful for getting PoC's before they are triaged and hidden.

```python
from scraper import Scraper
import json

scrape = Scraper()

# grabs any issues with id > 1132000
query = scrape.query_builder(num_items=1000000, with_strings="id>1132000")
output = scrape.get_all(query)

print(json.dumps(output))
```

## Advanced Usage

### Raw Query

More advanced tips and tricks on using the search can be found [here](https://bugs.chromium.org/p/chromium/issues/searchtips). If you're a veteran with the search, feel limited by the query_builder, or just want to try some new things you learned from the previous link, try the raw_query as shown below:

```python
from scraper import Scraper
import json

scrape = Scraper()

query = scrape.raw_query('"out of memory" summary:v8')
output = scrape.search(query)

print(json.dumps(output))
```

## META

### TODOS

1) Make the get_all() asynchronous. As is, it was tacked on in a hurry to get some use out of it  
2) Prebuild a few more queries for people who don't want to investigate search functionality  
3) Generalize for all monorail sites, not just chromium  
4) Read more monorail source and try to play nicely with their rate limiting and restrictions  

### Contributions

Got a neat use case? Love to hear it :) Also feel free to contribute. I will try to be timely on issues / pull requests, but will obviously not turn down good help.

### License

Project is MIT Licensed. I'm NOT responsible for what you do with this. I'm also NOT responsible for any lists you wind up on, [see here](https://chromium.googlesource.com/infra/infra/+/b83fc0c435a27eef10b5dd880a97af3e0c870201). DBAD. 