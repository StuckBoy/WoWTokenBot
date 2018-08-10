"File requires requests and termcolor"

import requests, json, re
from termcolor import colored

token_url = "https://wowtokenprices.com/current_prices.json"

r = json.loads(requests.get(token_url).text)

def checkNumber(number):
    pattern = re.compile("^-")
    if pattern.findall(str(number)):
        return colored(str(number), "red")
    else:
        return colored(str(number), "green")

for region in r:
    current_price = r[region]['current_price']
    last_change = r[region]['last_change']
    time_of_last_change = r[region]['time_of_last_change_utc_timezone']
    change_effect = checkNumber(last_change)
    print(region + ", " + str(current_price) + ", Change: " + str(change_effect) + " occurred at " + str(time_of_last_change) + " UTC")
