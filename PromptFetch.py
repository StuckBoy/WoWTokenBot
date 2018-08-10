"File requires requests. Simplified version of Fetch.py, can easily print to BASH screens."

import requests, json, re

token_url = "https://wowtokenprices.com/current_prices.json"

r = json.loads(requests.get(token_url).text)

for region in r:
    current_price = r[region]['current_price']
    last_change = r[region]['last_change']
    time_of_last_change = r[region]['time_of_last_change_utc_timezone']
    print(region + ", " + str(current_price) + ", Change: " + str(last_change) + " occurred at " + str(time_of_last_change) + " UTC")
