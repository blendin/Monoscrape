# Monorail / Chromium Issue Scraper

## What this is

Right now it scrapes bugs.chromium.com for issues, however it can (and  eventually will be) adapted to a general purpose monorail scraper. This was a project I was working on but quickly uploaded due to the permissions bug in monorail.

## Interesting Tidbits

A few main things to note here are the X-XSRF token (which you absolutely need to get your reponses back) and that the response comes back as malformed JSON [Apparently to prevent some nefariousness](https://chromium.googlesource.com/infra/infra/+/master/appengine/monorail/static/js/framework/framework-ajax.js). Speaking of which, all monorail source code is located [here](https://chromium.googlesource.com/infra/infra/+/master/appengine/monorail)

## Basic Usage

I tried to make sure there weren't any dependencies so this could just be dropped in and used. The query builder function below accepts many different arguments corresponding to the advanced search feature located [here](https://bugs.chromium.org/p/chromium/issues/advsearch). All arguments are expected as space delimited.

```python
from scraper import Scraper
import json

scrape = Scraper()

query = scrape.query_builder(num_items=1000, with_strings="v8")
output = scrape.search(query)

print(json.dumps(output))
```

## Getting Issues, Comments and Attachments

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

## License

Project is MIT Licensed. I'm NOT responsible for what you do with this. DBAD.