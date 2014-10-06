# Bitcoin AVM, an open source Django base Bitcoin ATM
# https://github.com/mn3monic/BitcoinAVM

import scripts, json, sys, time
#from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseServerError
from datetime import datetime
from base_app.btcprocessor import BTCProcessor, Configuration
from base_app.models import Transactions, Peripherals
from base_app.utils import get_btccurrency_rate, Currency, log_error, to_btc

def index(request):
    params = {}
    configuration = scripts.check_configuration()
    if not configuration:
        params['missing_config'] = True
    else:
        params['configuration'] = configuration
        btc_processor = BTCProcessor(False)
        params['wallet_exists'] = btc_processor.does_wallet_exists()

    return render(request, 'index.html', params)

def create_wallet(request):
    BTCProcessor(True)
    return redirect('/')


def restore_from_seed(request):
    btcprocessor = BTCProcessor(False)
    seed = request.POST.get('seedToRestore')
    btcprocessor.restore_wallet_from_seed(seed)
    return redirect('/')


def machine_status(request):
    # get the machine status based on network connectivity, btc availability etc...
    machine_status = {}
    machine_status['active'] = True  # TODO: replace this with proper implementation
    try:
        config = Configuration.objects.get()
    except Configuration.DoesNotExist:
        machine_status['error'] = True
        machine_status['missing_configuration'] = True
        return HttpResponse(json.dumps(machine_status), content_type="application/json")

    try:
        currency_btc_rate = get_btccurrency_rate(config.currency)
        machine_status['exchange_rate'] ='%.2f' % currency_btc_rate
        machine_status['last_retrieved'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        machine_status['currency'] = Currency.AcceptedCurrency[config.currency-1][1]
        return HttpResponse(json.dumps(machine_status), content_type="application/json")
    except:
        return HttpResponseServerError(json.dumps({'error': "can't connect to Bitstamp Api"}), content_type="application/json")


def transaction_init(request):
    """
    Start transaction page:
    - Start transaction with a new session_id
    - Set init_timestamp
    - Set fixed price for exchange rate, fetch latest
    - Enable QR code reader
    - Set status: init
    - Returns sessionId and available coins
    """
    config = Configuration.objects.get()
    transaction_exchange_rate = get_btccurrency_rate(config.currency)
    init_tx_result = scripts.init_transaction(transaction_exchange_rate)
    session_id = init_tx_result['session_id']
    initialized = init_tx_result['initialized']
    request.session['session_id'] = session_id

    if not session_id:
        return HttpResponseServerError(json.dumps('Invalid session id'), content_type="application/json")

    if initialized:
        return HttpResponse(json.dumps(init_tx_result), content_type="application/json")
    else:
        return HttpResponseServerError(json.dumps('ATM disabled'), content_type="application/json")

def read_address(request):
    res = {}
    try:
        session_id = '9d0e2ee14b44d4d75f682f0be1c24f73'
        #session_id = request.session['session_id']
    except:
        res = {'error': 1, 'message': 'no session id'}
        return HttpResponse(json.dumps(res), content_type="application/json")
    else:
        status = request.GET.get('status') # TODO: Switch to post, GET only for testing
        if status == 'start':
            print 'starting qrcode reader'
            scripts.qrcode_reader(status, session_id)
            res['status'] = 'QRCode reader started'
            res['error'] = 0
        elif status == 'stop':
            print 'stopping qrcode reader'
            per = Peripherals.objects.get()
            per.qrcode_status = False
            per.save()
            res['status'] = 'QRCode reader stopped'
            res['error'] = 0
        elif status == 'check':
            transaction = Transactions.objects.get(session_id = session_id)
            dest_addr = transaction.dest_address
            if dest_addr != '':
                res['address'] = dest_addr
                res['error'] = 0
        else:
            res['status'] = 'invalid request'
            res['error'] = 1

    return HttpResponse(json.dumps(res), content_type="application/json")

def set_address(request):
    try:
        session_id = request.session['session_id']
    except:
        res = {'error': 1, 'message': 'no session id'}
        return HttpResponse(json.dumps(res), content_type="application/json")
    address = request.GET.get('address') # TODO: Switch to post, GET only for testing
    print request
    print address
    res = scripts.set_address(session_id, address)
    return HttpResponse(json.dumps(res), content_type="application/json")


def notes_reader(request):
    pass

def check_notes_reader_status(request):
    session_id = request.session['session_id']
    try:
        transaction_status = scripts.check_transaction_status(session_id)
        return HttpResponse(json.dumps(transaction_status), content_type="application/json")
    except Transactions.DoesNotExist:
        log_error('check_notes_reader_status', 'transaction does not exists', session_id=session_id)
        raise
    except:
        exc_info = sys.exc_info()
        message = str(exc_info[0]) + ' - ' + str(exc_info[1])
        log_error('check_notes_reader_status', message, session_id=session_id)
        raise


def confirm_payment(request):
    try:
        res = {}
        session_id = request.session['session_id']
        if not session_id:
            res['message'] = 'Invalid session id'
        if request.method == 'POST':
            #notes_reader_command_message_queue.put(True)
            time.sleep(2)
            notes_reader_status = {}
            transaction = Transactions.objects.get(session_id=session_id)
            notes_reader_status['notes_inserted'] = transaction.cash_amount
            notes_reader_status['btc_amount'] = transaction.btc_amount
            tx_result = scripts.broadcast_transaction(session_id)
            res = notes_reader_status
        else:
            return HttpResponseServerError(json.dumps({'error': "can't broadcast transaction - invalid http method"}), content_type="application/json")

        return HttpResponse(json.dumps(res), content_type="application/json")

    except Transactions.DoesNotExist:
        log_error('confirm_payment', 'transaction does not exists', session_id=session_id)
    except:
        exc_info = sys.exc_info()
        message = str(exc_info[0]) + ' - ' + str(exc_info[1])
        log_error('confirm_payment', message, session_id=session_id)
        return HttpResponseServerError(json.dumps({'error': "can't broadcast transaction"}), content_type="application/json")


def wallet(request):
    btcp = BTCProcessor(True)
    b = btcp.check_balance()
    balance = str(to_btc(b[0])) + ' ' + str(to_btc(b[1]))
    wallet_status = {}
    wallet_status['balance'] = balance
    wallet_status['addresses'] = btcp.wallet.addresses()

    return HttpResponse(json.dumps(wallet_status), content_type="application/json")


def test(request):
    #FIXME what's this ?
    btcp = BTCProcessor(True)
    t = btcp.broadcast_transaction('1GEQsEtzeUJHVNWR9xt24RMXu676rxGhf5',0.0003)
    return HttpResponse(json.dumps(t), content_type="application/json")