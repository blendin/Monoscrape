from csi_search import Searcher
import json

scrape = Scraper()

query = scrape.query_builder(num_items=1000000, with_strings="id>11320000")
output = scrape.get_all(query)

print(json.dumps(output))