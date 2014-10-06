# Bitcoin AVM, an open source Django base Bitcoin ATM
# https://github.com/mn3monic/BitcoinAVM

import hmac, hashlib, requests, json, urllib
from time import time


######################################
# BitStamp API
# Error codes:
#
# 101 = Connection error or timeout
# 102 = Wrong response
# 103 = Error from JSON response
#
######################################


class Bitstamp():

    def __init__(self, client_id, key, secret, debug=True):
        self.client_id, self.key, self.secret = client_id, key, secret
        self.debug = debug
        self.name = 'Bitstamp'
        self.url = ('https://www.bitstamp.net/api',)
        self.timeout = 5
        if debug:
            self.debug_messages = {}

    def sign_message(self):
        nonce = str(int(time()))
        message = nonce + self.client_id + self.key
        signature = hmac.new(self.secret, msg=message, digestmod=hashlib.sha256).hexdigest().upper()
        return signature, nonce

    def get_balance(self):
        func_name = 'get_balance'
        signature, nonce = self.sign_message()
        url = '%s/balance/' % self.url[0]
        try:
            payload = {'key': self.key,
                       'signature': signature,
                       'nonce': nonce}
            balance = requests.post(url, timeout=self.timeout, data=payload)
        except requests.Timeout, requests.ConnectionError:
            return 101, self.name, func_name, nonce
        if balance.headers['content-type'] != 'application/json':
            return 102, self.name, func_name, nonce
        self.balance = balance.json()
        if self.balance.get('error'):
            if self.debug:
                self.debug_messages.update({func_name: self.balance})
            return 103, self.name, func_name, nonce, self.balance['error']
        return 0, self.name, func_name, nonce

    def get_orderbook(self):
        func_name = 'get_orderbook'
        timestamp = int(time())
        url = '%s/order_book/' % self.url[0]
        try:
            orderbook = requests.get(url, timeout=self.timeout)
        except requests.Timeout, requests.ConnectionError:
            return 101, self.name, func_name, timestamp
        if orderbook.headers['content-type'] != 'application/json':
            return 102, self.name, func_name, timestamp
        self.orderbook = orderbook.json()
        if self.orderbook.get('error'):
            if self.debug:
                self.debug_messages.update({func_name: self.orderbook})
            return 103, self.name, func_name, timestamp, self.orderbook['error']
        return 0, self.name, func_name, timestamp


    def set_buy_order(self, amount, price):
        func_name = 'set_buy_order'
        signature, nonce = self.sign_message()
        url = '%s/buy/' % self.url[0]
        try:
            payload = {'key': self.key,
                       'signature': signature,
                       'nonce': nonce,
                       'amount': amount,
                       'price': price}
            buy_order = requests.post(url, timeout=self.timeout, data=payload)
        except requests.Timeout, requests.ConnectionError:
            return 101, self.name, func_name, nonce
        if buy_order.headers['content-type'] != 'application/json':
            return 102, self.name, func_name, nonce
        self.buy_order = buy_order.json()
        if self.buy_order.get('error'):
            if self.debug:
                self.debug_messages.update({func_name: self.buy_order})
            return 103, self.name, func_name, nonce, self.buy_order['error']
        return 0, self.name, func_name, nonce

    def get_open_orders(self):
        func_name = 'get_open_orders'
        signature, nonce = self.sign_message()
        url = '%s/open_orders/' % self.url[0]
        try:
            payload = {'key': self.key,
                       'signature': signature,
                       'nonce': nonce}
            open_orders = requests.post(url, timeout=self.timeout, data=payload)
        except requests.Timeout, requests.ConnectionError:
            return 101, self.name, func_name, nonce
        if open_orders.headers['content-type'] != 'application/json':
            return 102, self.name, func_name, nonce
        self.open_orders = open_orders.json()
        if type(self.open_orders) == type(dict()):
            if self.open_orders.get('error'):
                if self.debug:
                    self.debug_messages.update({func_name: self.open_orders})
                return 103, self.name, func_name, nonce
        return 0, self.name, func_name, nonce

    def set_cancel_order(self, order_id):
        func_name = 'cancel_order'
        signature, nonce = self.sign_message()
        url = '%s/cancel_order/' % self.url[0]
        try:
            payload = { 'key': self.key,
                        'signature' : signature,
                        'nonce': nonce,
                        'id': order_id}
            cancel_order = requests.post(url, timeout=self.timeout, data=payload)
        except requests.Timeout, requests.ConnectionError:
           return 101, self.name, func_name, nonce
        if cancel_order.headers['content-type'] != 'application/json':
            return 102, self.name, func_name, nonce
        self.cancel_order = cancel_order.json()
        if type(self.cancel_order) == type(dict()):
            if self.cancel_order.get('error'):
                if self.debug:
                    self.debug_messages.update({func_name: self.cancel_order})
                return 103, self.name, func_name, nonce
        return 0, self.name, func_name, nonce

    def set_bitcoin_withdrawal(self, amount, address):
        func_name = 'set_bitcoin_withdraw'
        signature, nonce = self.sign_message()
        url = '%s/bitcoin_withdrawal/' % self.url[0]
        try:
            payload = {'key': self.key,
                       'signature': signature,
                       'nonce': nonce,
                       'amount': amount,
                       'address': address}
            bitcoin_withdrawal = requests.post(url, timeout=self.timeout, data=payload)
        except requests.Timeout, requests.ConnectionError:
            return 101, self.name, func_name, nonce
        if bitcoin_withdrawal.headers['content-type'] != 'application/json':
            return 102, self.name, func_name, nonce
        self.bitcoin_withdrawal = bitcoin_withdrawal.json()
        if self.bitcoin_withdrawal.get('error'):
            if self.debug:
                self.debug_messages.update({func_name: self.bitcoin_withdrawal})
            return 103, self.name, func_name, nonce
        return 0, self.name, func_name, nonce

    def get_ticker(self):
         func_name = 'get_ticker'
         timestamp = int(time())
         url = '%s/ticker/' % self.url[0]
         try:
             ticker = requests.get(url, timeout=self.timeout)
         except requests.Timeout, requests.ConnectionError:
             return 101, self.name, func_name
         if ticker.headers['content-type'] != 'application/json':
             return 102, self.name, func_name
         self.ticker = ticker.json()
         if self.ticker.get('error'):
             if self.debug:
                 self.debug_messages.update({func_name: self.balance})
             return 103, self.name, func_name, self.ticker['error']
         return 0, self.name, func_name, timestamp

    def get_buy_prices(self, amount):
        """
        Return (ap, hp):
        - average price (ap, float): the expected total price for the bought
        - high price (ap, float): should be the market order price, to get accomplished asap
        """
        func_name = 'get_buy_prices'
        timestamp = int(time())
        book = self.get_orderbook()
        if book[0] != 0:
            return 201, self.name, func_name, timestamp
        total, prices, market_price = [], [], []
        i, expected_price, high_price = 0, 0, 0
        while sum(total) < amount:
            total.append(float(self.orderbook['asks'][i][1]))
            prices.append(float(self.orderbook['asks'][i][1]) * float(self.orderbook['asks'][i][0]))
            amount -= total[i]
            expected_price = sum(prices) / sum(total)
            high_price = prices[i] / total[i]
            i += 1
        return 0, expected_price, high_price

    def get_bitcoin_availability(self, cash=True, cryptos=True):
        """
        Return approx Bitcoin availability
        methods:
        cash=True (default) return the buyable bitcoins from fiat cash
        cryptos=True (default) return the bitcoins availability on the exchange wallet
        """
        func_name = 'get_bitcoin_availability'
        timestamp = int(time())
        if self.get_balance()[0]:
            return 201, self.name, func_name, timestamp
        bitcoins = 0
        if cash:
            if self.get_orderbook()[0]:
                return 201, self.name, func_name, timestamp
            total, btcs = [], []
            i = 0
            balance = float(self.balance['usd_balance'])
            while sum(total) < balance:
                total.append(float(self.orderbook['asks'][i][0])*float(self.orderbook['asks'][i][1]))
                btcs.append(float(self.orderbook['asks'][i][1]))
                i += 1
            bitcoins += (balance / sum(total)) * sum(btcs)
        if cryptos:
            bitcoins += float(self.balance['btc_balance'])
        return 0, round(bitcoins, 4)