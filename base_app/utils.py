# Bitcoin AVM, an open source Django base Bitcoin ATM
# https://github.com/mn3monic/BitcoinAVM

import requests
from base_app.models import ErrorLog, Currency
from exchanges.bitstamp import Bitstamp
from datetime import datetime


def to_satoshis(btc_amount):
    return int(btc_amount/0.00000001)


def to_btc(satoshis_amount):
    return satoshis_amount*0.00000001


def get_btccurrency_rate(currency):
    bitstamp_api = Bitstamp(0,'','')
    bitstamp_api.get_ticker()
    ticker = bitstamp_api.ticker
    return float(ticker.get('last'))*float(get_usdcurrency_rate(currency))


def get_usdcurrency_rate(currency):
    if currency == Currency.EUR:
        url = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.xchange%20where%20pair%20in%20(%22USDEUR%22)&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback='
    elif currency == Currency.GBP:
        url = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.xchange%20where%20pair%20in%20(%22USDGBP%22)&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback='
    elif currency == Currency.USD:
        return 1
    else:
        log_error('get_usdcurrency_rate','unsupported currency: ' + currency)
        raise

    try:
        result = requests.get(url)
    except requests.Timeout, requests.ConnectionError:
        return 101, 'Error getting usd eur rate from Yahoo'
    json_result = result.json()
    rate = json_result['query']['results']['rate']['Rate']
    return rate


def log_error(function_name, error_message, error_code='', session_id=''):
    log = ErrorLog(error_code=error_code, function=function_name, session_id=session_id, message=error_message)
    log.created_on = datetime.now()
    log.save()
    return