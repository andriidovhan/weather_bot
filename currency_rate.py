#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

#TODO use https://market.mashape.com/dontgiveafish/hryvna-today instead of the following link
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
            rate_buy += round(float(resp['rateBuy']), 2)
            rate_sale += round(float(resp['rateSale']), 2)

    av_rate_buy = rate_buy/count
    av_rate_sale = rate_sale/count
    return "{}: {}/{}".format(c, av_rate_buy, av_rate_sale)
