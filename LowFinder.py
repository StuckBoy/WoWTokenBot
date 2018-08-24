"""Fetches current price, and compares against 30 day price.
Requires requests, AP Scheduler, and win10Toast for desktop notifications"""

import requests, json, time, datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from win10toast import ToastNotifier

def fetchJSON():
    """Function starts by fetching JSON from two URLs, one containing the current in-game gold price for a WoW Token,
        and the other containing history for the price over the last thirty days. It then scans through the last thirty
        for the lowest price, and compares it to the current price."""

    curr_token_url = "https://wowtokenprices.com/current_prices.json"
    month_token_url = "https://wowtokenprices.com/history_prices_30_day.json"

    r1 = json.loads(requests.get(curr_token_url).text)
    r2 = json.loads(requests.get(month_token_url).text)
    findPrice(r1, r2)


def findPrice(r1, r2):
    """Function scans through provided JSON in search of lowest price in the past 30 days. Upon finding result, the
        outcome of the comparision determines the response of the script."""

    current_price = r1['us']['current_price']
    last_change = r1['us']['last_change']
    time_of_last_change = r1['us']['time_of_last_change_utc_timezone']

    lowest_price = 1000000000

    for entry in r2["us"]:
        if entry["price"] < lowest_price:
            lowest_price = entry["price"]

    toaster = ToastNotifier()

    NotifTitle = "WoW Token Bot"
    curr_string = str(current_price)
    low_string = str(lowest_price)

    if lowest_price > current_price:
        toaster.show_toast(NotifTitle, curr_string + ", BUY NOW!", duration=10, threaded=True)
    else:
        toaster.show_toast(NotifTitle, "Lowest: " + low_string + " < Current: " + curr_string, duration=1800, threaded=True)

    while toaster.notification_active():
        time.sleep(0.1)


scheduler = BlockingScheduler()
scheduler.add_job(fetchJSON(), 'interval', hours=1)
scheduler.start()