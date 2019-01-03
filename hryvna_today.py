#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

import datetime
import os
import requests


CURRENT_DATE = datetime.datetime.now()  # type: datetime
URL = 'https://hryvna-today.p.mashape.com/v1/rates/averages'


def init_request():
    response = requests.get(URL,
                           headers={
                               "X-Mashape-Key": os.environ.get('TOKEN_HRYVNA_TODAY'),
                               "Accept": "application/json"
                           })
    return response.json()

def get_rate(currency=[]):
    # USD = 840, EUR = 978
    c = currency[0].upper() if bool(currency) else 'USD'
    code_currency = {"USD": 840, "EUR": 978}
    resp = init_request()

    usd_rate = resp['data'][CURRENT_DATE.strftime("%Y-%m-%d")][str(code_currency[c])]
    com_buy = round(float(usd_rate['commercial']['buy']['value']), 2)
    com_sale = round(float(usd_rate['commercial']['sale']['value']), 2)
    black_buy = round(float(usd_rate['commercial']['buy']['value']), 2)
    black_sale = round(float(usd_rate['commercial']['sale']['value']), 2)

    return """Commercial {}/{}\n Black {}/{}""".format(com_buy, com_sale, black_buy, black_sale)
