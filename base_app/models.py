# Bitcoin AVM, an open source Django base Bitcoin ATM
# https://github.com/mn3monic/BitcoinAVM

from django.db import models


class Currency:
    def __init__(self):
        return

    # Accepted currencies

    EUR = 1
    GBP = 2
    USD = 3

    AcceptedCurrency = (
        (EUR, 'EUR'),
        (GBP, 'GBP'),
        (USD, 'USD')
    )


class Configuration(models.Model):
    """
    Default username configuration
    """
    active = models.BooleanField()
    surcharge = models.FloatField(null=True)
    VAT = models.FloatField(null=True)
    max_cash_per_transaction = models.FloatField(null=True)
    btc_transaction_fee = models.FloatField(null=True)
    currency = models.IntegerField(choices=Currency.AcceptedCurrency, default=Currency.EUR)
    wallet_seed = models.CharField(max_length=500, null=True, blank=True)
    wallet_password = models.CharField(max_length=100, null=True)
    wallet_path = models.CharField(max_length=200, null=True, blank=True)
    minimum_btc_transaction = models.FloatField(null=True)


class Transactions(models.Model):
    """
    Transactions historical data
    """

    # Transaction statuses

    INITIALIZED = 1
    ADDRESS_SET = 2
    INSERTING_CASH = 3
    CASH_INSERTED = 4
    BROADCASTING = 5
    COMPLETED = 6
    FAILED = 7
    ABORTED = 8

    TransactionStatus = {
        (INITIALIZED, 'Initialized'),
        (ADDRESS_SET, 'address_set'),
        (INSERTING_CASH, 'inserting_cash'),
        (CASH_INSERTED, 'cash_inserted'),
        (BROADCASTING, 'broadcasting'),
        (COMPLETED, 'completed'),
        (FAILED, 'failed'),
        (ABORTED, 'aborted')
    }

    session_id = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=150, null=True)
    exchange_rate = models.FloatField()
    btc_amount = models.FloatField(null=True)
    coins_available = models.FloatField(null=True)
    cash_amount = models.FloatField(null=True)
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
    dest_address = models.CharField(max_length=40, null=True)
    status = models.IntegerField(choices=TransactionStatus, default=INITIALIZED)
    max_cash_acceptable = models.FloatField(null=True)
    email_address = models.EmailField(null=True)
    ReferenceNumber = models.CharField(max_length=16, null=True)
    surcharge = models.FloatField(null=True)
    currency = models.IntegerField(choices=Currency.AcceptedCurrency, default=Currency.EUR)

class ErrorLog(models.Model):
    """
    Application error log
    """
    error_code = models.CharField(max_length=5)
    message = models.CharField(max_length=1000)
    function = models.CharField(max_length=100)
    created_on = models.DateTimeField()
    session_id = models.CharField(max_length=100)

class Orders(models.Model):
    session_id = models.CharField(max_length=50, null = True)
    username = models.CharField(max_length=50, null=True)
    order_id = models.CharField(max_length=50, null=True)
    exchange = models.CharField(max_length=50, null=True)
    amount = models.FloatField(null=True)
    price = models.FloatField(null=True)
    type = models.FloatField(null=True)
    total = models.FloatField(null=True)
    status = models.FloatField(null=True)
    timestamp = models.FloatField(null=True)

class Peripherals(models.Model):
    qrcode_status = models.BooleanField()