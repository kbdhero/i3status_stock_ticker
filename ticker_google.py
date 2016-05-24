#!/usr/bin/python

# Use the Google finance api to retrieve stock quotes in your i3status bar.
from time import time
import requests
import json


class Py3status:
    cache_timeout = 20
    format = '{output}'
    symbol = '.DJI'
    exchange = 'INDEXDJXL'


    def __init__(self):
        self.last_last_price = 0


    def last_price(self):
        # Retrieve the last price for the target symbol from the google finance API
        base_url = "http://finance.google.com/finance/info?client=ig&q="

        req  = requests.get(base_url + self.exchange + ":" + self.symbol).content

        data = json.loads(str(req, 'utf-8').replace("/", ""))

        return data[0]["l"].replace(",", "")


    def return_response(self, i3s_output_list, i3s_config):
        response = {
            'cached_until': time() + self.cache_timeout,
            'full_text': ''
        }

        last_price = self.last_price()

        # green/red rendering.
        if float(last_price) >  self.last_last_price:
            response["color"] = "#00ff00"

        elif float(last_price) < self.last_last_price:
            response["color"] = "#ff0000"

        self.last_last_price = float(last_price)

        response['full_text'] = self.format.format(output="{}: {}".format(self.symbol, last_price))

        return response


if __name__ == "__main__":
    from time import sleep
    x = Py3status()
    while True:
        print(x.return_response([], config))
        sleep(1)



