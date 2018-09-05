"""Fetches current price, and compares against 30 day price.
Requires requests, AP Scheduler, and win10Toast for desktop notifications"""

import requests, json, time, datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from win10toast import ToastNotifier


def fetchJSON():
    """Function starts by fetching JSON from two URLs, one containing the current in-game gold price for a WoW Token,
        and the other containing history for the price over the last thirty days."""

    curr_token_url = "https://wowtokenprices.com/current_prices.json"
    month_token_url = "https://wowtokenprices.com/history_prices_30_day.json"
    checkPages(curr_token_url, month_token_url)

def throwError():
    errorToaster = ToastNotifier()

    NotifTitle = "WoW Token Bot"
    errorToaster.show_toast(NotifTitle, "Error contacting website, will try again soon.", duration=1800, threaded=True)


def checkPages(curr_token_url, month_token_url):

    r1Text, r2Text = " ", " "
    r1 = requests.get(curr_token_url)
    if r1.status_code == 200:
        r1Text = json.loads(r1.text)
    else:
        throwError()

    r2 = requests.get(month_token_url)
    if r2.status_code == 200:
        r2Text = json.loads(r2.text)
    else:
        throwError()

    findPrice(r1Text, r2Text)


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
    curr_string = str(format(current_price, ',d'))
    low_string = str(format(lowest_price, ',d'))

    if lowest_price > current_price:
        toaster.show_toast(NotifTitle, curr_string + ", BUY NOW!", duration=15, threaded=True)
    else:
        toaster.show_toast(NotifTitle, "Lowest: " + low_string + " < Current: " + curr_string, duration=15, threaded=False)

fetchJSON()