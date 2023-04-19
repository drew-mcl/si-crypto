#!/usr/bin/env python3

from cryptocmd import CmcScraper

# initialise scraper without time interval
scraper = CmcScraper("BTC")

# get raw data as list of list
headers, data = scraper.get_data()

# get data in a json format
xrp_json_data = scraper.get_data("json")

# export the data as csv file, you can also pass optional `name` parameter
scraper.export("csv", name="btc_all_time", path="data/")

# Pandas dataFrame for the same data
df = scraper.get_dataframe()