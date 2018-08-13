"Fetches current price, and compares against 30 day price."

import requests, json, re

curr_token_url = "https://wowtokenprices.com/current_prices.json"
month_token_url = "https://wowtokenprices.com/history_prices_30_day.json"

r1 = json.loads(requests.get(curr_token_url).text)
r2 = json.loads(requests.get(month_token_url).text)

current_price = r1['us']['current_price']
last_change = r1['us']['last_change']
time_of_last_change = r1['us']['time_of_last_change_utc_timezone']

lowest_price = 1000000000

for entry in r2["us"]:
    if entry["price"] < lowest_price:
        lowest_price = entry["price"]

if current_price < lowest_price:
    print("BUY, BUY, BUY!!!")
    print("US, " + str(current_price) + ", Change: " + str(last_change) + " occurred at " + str(time_of_last_change) + "UTC")
else:
    print(str(lowest_price) + " < " + str(current_price) + "...Eternal Sadness")