"""Fetches current price, and compares against 30 day price.
Requires requests and win10Toast for desktop notifications"""

import requests, json, re
from win10toast import ToastNotifier

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

toaster = ToastNotifier()

if lowest_price > current_price:
    toaster.show_toast("WoW Token Bot", str(current_price) + ", BUY NOW!")
else:
    toaster.show_toast("WoW Token Bot", "Lowest: " + str(lowest_price) + " < Current: " + str(current_price))