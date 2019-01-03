#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

URL = 'http://bank-ua.com/export/exchange_rate_cash.json'


def init_request(url):
    r = requests.get(url)
    return r.json()


def get_rate(currency=[]):
    count = 0
    rate_buy = 0
    rate_sale = 0
    c = currency[0] if bool(currency) else 'USD'

    response = init_request(URL)
    for resp in response:
        if resp['codeAlpha'] == c.upper():
            count += 1
            rate_buy += float(resp['rateBuy'])
            rate_sale += float(resp['rateSale'])

    av_rate_buy = round(rate_buy/count, 2)
    av_rate_sale = round(rate_sale/count, 2)
    return "{}: {}/{}".format(c, av_rate_buy, av_rate_sale)
