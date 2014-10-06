# Bitcoin AVM, an open source Django base Bitcoin ATM
# https://github.com/mn3monic/BitcoinAVM

from base_app.models import Configuration, Transactions, Peripherals
from utils import log_error
from os import urandom
from base_app.btcprocessor import BTCProcessor
from base_app.utils import to_btc
from datetime import datetime
from peripherals.qrcode import QRCode as Reader
import sys, time, bitcoinaddress


def init_transaction(exchange_rate):
    """
    - Check if a previous session was pending, if found invalidate it
    - Initialize a new transaction with a new session_id
    - Set fixed exchange rate, init_timestamp, availability, session_id
    - Set status: initialized if coins are available, failed if not
    """
    try:
        btcProc = BTCProcessor(True)
        session_id = urandom(16).encode('hex')
        available_coins =  to_btc(float(btcProc.check_balance()[0]))
        timestamp = datetime.now()
        config = Configuration.objects.get()
        set_transaction = Transactions(session_id=session_id,
                                           created_on=timestamp,
                                           updated_on=timestamp,
                                           exchange_rate=exchange_rate,
                                           coins_available=available_coins,
                                           currency=config.currency
                                           )

        if  available_coins > 0:
            set_transaction.status = Transactions.INITIALIZED
            initialized = True
            # surcharge = user_data.surcharge
            # surcharged_exchange_rate = round(float((exchange_rate*surcharge) + exchange_rate), 2)
            set_transaction.max_cash_acceptable = max_acceptable_cash(exchange_rate, available_coins)
            # enable qr reader
        else:
            set_transaction.status = Transactions.ABORTED
            initialized = False

        set_transaction.save()
    except:
        exc_info = sys.exc_info()
        message = str(exc_info[0]) + ' - ' + str(exc_info[1])
        log_error('init transaction',message)
    return {'initialized': initialized, 'session_id': session_id, 'available_coins': available_coins}


def set_address(session_id, address):
    try:
        transaction = Transactions.objects.get(session_id=session_id)
        if not address:
            message = 'no address supplied'
            error = 1
        else:
            if bitcoinaddress.validate(address):
                transaction.dest_address = address
                transaction.status = Transactions.ADDRESS_SET
                transaction.updated_on = datetime.now()
                transaction.save()
                message = 'address set'
                error = 0
            else:
                message = 'invalid address'
                error = 1
    except Transactions.DoesNotExist:
        message = 'invalid session_id'
        error = 1
    return {'error': error, 'message': message}

def qrcode_reader(status, session_id):
    reader = Reader('/dev/video0')
    transaction = Transactions.objects.get(session_id = session_id)
    if status == 'start':
        per = Peripherals.objects.get()
        per.qrcode_status = True
        cam_status = per.qrcode_status
        per.save()
        while cam_status:
            address = reader.read_address()
            if address != '':
                if bitcoinaddress.validate(address):
                    per.qrcode_status = False
                    per.save()
                    transaction.dest_address = address
                    transaction.status = 2
                    transaction.updated_on = transaction.updated_on = datetime.now()
                    transaction.save()
            per = Peripherals.objects.get()
            cam_status = per.qrcode_status
            time.sleep(0.1)
    if status == 'stop':
        per = Peripherals.objects.get()
        per.qrcode_status = False
        per.save()
    elif status == 'check':
        transaction = Transactions.objects.get(session_id = session_id)
        return transaction.dest_address

def notes_reader(status, session_id):
    pass


def max_acceptable_cash(exchange_rate, available_coins):
    """
    This functios is invoked by init_transaction, it set the maximum amount of FIAT cash
    the AVM could accept
    """
    configuration = Configuration.objects.get()
    max_sellable_amount = configuration.max_cash_per_transaction
    if available_coins * exchange_rate > max_sellable_amount:
        max_accepted_cash = max_sellable_amount
    else:
        max_accepted_cash = available_coins * exchange_rate
    return max_accepted_cash


def check_configuration():
    """
    Checks whether configuration exists in the db
    returns False if not, the configuration object if it does exist
    """
    try:
        configuration = Configuration.objects.get()
        return configuration
    except Configuration.DoesNotExist:
        return False


def check_transaction_status(session_id):
    transaction_status = {}
    try:
        btc_proc = BTCProcessor(True)
        available_coins =  to_btc(float(btc_proc.check_balance()[0]))
        transaction = Transactions.objects.get(session_id=session_id)
        transaction_status['notes_inserted'] = transaction.cash_amount
        transaction_status['btc_amount'] = transaction.btc_amount

    except Transactions.DoesNotExist:
        log_error('check_transaction_status', 'transaction does not exists', session_id=session_id)
    except:
        exc_info = sys.exc_info()
        message = str(exc_info[0]) + ' - ' + str(exc_info[1])
        log_error('check_transaction_status', message, session_id=session_id)
    return transaction_status

def broadcast_transaction(session_id):
    try:
        transaction = Transactions.objects.get(session_id=session_id)
        transaction.status = Transactions.CASH_INSERTED
        transaction.updated_on = datetime.now()
        transaction.save()

        #TODO: broadcast transaction using BTCProcessor and update transaction in DB
        return {'success': True}
    except Transactions.DoesNotExist:
        log_error('broadcast_transaction', 'transaction does not exists', session_id=session_id)
        raise
    except:
        exc_info = sys.exc_info()
        message = str(exc_info[0]) + ' - ' + str(exc_info[1])
        log_error('broadcast_transaction', message, session_id=session_id)
        raise


