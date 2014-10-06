# Bitcoin AVM, an open source Django base Bitcoin ATM
# https://github.com/mn3monic/BitcoinAVM

import hmac, hashlib, requests, json, urllib
from time import time


######################################
# BTCe API
# Error codes:
#
# 101 = Connection error or timeout
# 102 = Wrong response
# 103 = Error from JSON response
#
######################################



class BTCe():
    def __init__(self, key, secret, debug=True):
        self.key, self.secret = key, secret
        self.debug = debug
        self.name = 'BTC-e'
        self.url = ('https://btc-e.com/tapi', 'https://btc-e.com/api/2')
        self.timeout = 5
        if debug:
            self.debug_messages = {}
        self.pair = 'btc_eur'

    def get_nonce(self):
        nonce = str(int(time()))
        return nonce

    def sign_message(self, message):
        signature = hmac.new(self.secret, message, digestmod=hashlib.sha512).hexdigest()
        return signature

    def get_balance(self):
        func_name = 'get_balance'
        nonce = self.get_nonce()
        payload = {'method': 'getInfo',
                  'nonce': nonce}
        message = urllib.urlencode(payload)
        signature = self.sign_message(message)
        headers = {'key': self.key,
                  'content-type': 'application/x-www-form-urlencoded',
                  'sign': signature}
        try:
            balance = requests.post(self.url[0], data=payload, headers=headers)
        except requests.Timeout, requests.ConnectionError:
            return 101, self.name, func_name, nonce
        try:
            self.balance = balance.json()
        except:
            return 102, self.name, func_name, nonce
        if self.balance.get('error'):
            if self.debug:
                self.debug_messages.update({func_name: self.balance})
            return 103, self.name, func_name, nonce, self.balance['error']
        return 0, self.name, func_name, nonce

    def get_orderbook(self):
        func_name = 'get_orderbook'
        timestamp = self.get_nonce()
        url = '%s/%s/depth' % (self.url[1], self.pair)
        try:
            orderbook = requests.get(url, timeout=self.timeout)
        except requests.Timeout, requests.ConnectionError:
            return 101, self.name, func_name, timestamp
        try:
            self.orderbook = orderbook.json()
        except:
            return 102, self.name, func_name, timestamp
        if self.orderbook.get('error'):
            if self.debug:
                self.debug_messages.update({func_name: self.orderbook})
            return 103, self.name, func_name, timestamp, self.orderbook['error']
        return 0, self.name, func_name, timestamp


    def set_buy_order(self, amount, price):
        func_name = 'set_buy_order'
        nonce = self.get_nonce()
        payload = {'method': 'Trade',
                   'pair': self.pair,
                   'nonce': nonce,
                   'type': 'buy',
                   'rate': float(price),
                   'amount': float(amount)}
        message = urllib.urlencode(payload)
        signature = self.sign_message(message)
        headers = {'key': self.key,
                   'content-type': 'application/x-www-form-urlencoded',
                   'sign': signature}
        try:
            buy_order = requests.post(self.url[0], data=payload, headers=headers)
        except requests.Timeout, requests.ConnectionError:
            return 101, self.name, func_name, nonce
        try:
            self.buy_order = buy_order.json()
        except:
            return 102, self.name, func_name, nonce
        if self.buy_order.get('error'):
            if self.debug:
                self.debug_messages.update({func_name: self.buy_order})
            return 103, self.name, func_name, nonce, self.buy_order['error']
        return 0, self.name, func_name, nonce

    def get_open_orders(self):
        func_name = 'get_open_orders'
        nonce = self.get_nonce()
        payload = {'method': 'ActiveOrders',
                   'pair': self.pair,
                   'nonce': nonce}
        message = urllib.urlencode(payload)
        signature = self.sign_message(message)
        headers = {'key': self.key,
                   'content-type': 'application/x-www-form-urlencoded',
                   'sign': signature}
        try:
            open_orders = requests.post(self.url[0], data=payload, headers=headers)
        except requests.Timeout, requests.ConnectionError:
            return 101, self.name, func_name, nonce
        try:
            self.open_orders = open_orders.json()
        except:
            return 102, self.name, func_name, nonce
        if self.open_orders.get('error'):
            if self.debug:
                self.debug_messages.update({func_name: self.open_orders})
            return 103, self.name, func_name, nonce, self.open_orders['error']
        return 0, self.name, func_name, nonce