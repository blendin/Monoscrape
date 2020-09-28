from scraper import Scraper
import json

scrape = Scraper()

query = scrape.query_builder(num_items=1000000, with_strings="id>1132000")
output = scrape.get_all(query)

print(json.dumps(output))