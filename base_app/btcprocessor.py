# Bitcoin AVM, an open source Django base Bitcoin ATM
# https://github.com/mn3monic/BitcoinAVM

import sys
from electrum import SimpleConfig, WalletStorage, Network, Wallet
import BitVending.settings
from base_app.models import Configuration
from base_app import utils

class BTCProcessor():

    def __init__(self, load_wallet):
        self.base_dir = BitVending.settings.BASE_DIR
        self.proc_config = {}
        self.__init_config__()
        self.__set_wallet_path__()
        self.config = SimpleConfig(self.proc_config)
        self.storage = WalletStorage(self.config)
        self.network = Network(self.config)
        self.network.start(False)
        if load_wallet:
            self.wallet = self.create_or_load_wallet()
        self.transaction_fee = utils.to_satoshis(float(self.proc_config.get('fee')))
        return

    def __password__(self):
        return self.proc_config.get('password')

    def __set_wallet_path__(self):
        if not self.proc_config.get('wallet_path'):
            self.proc_config['wallet_path'] = self.base_dir + '/electrum.dat'

    def __init_config__(self):
        config_obj = Configuration.objects.get()
        self.proc_config['wallet_path'] = config_obj.wallet_path
        self.proc_config['password'] = config_obj.wallet_password
        self.proc_config['minimum_transaction'] = config_obj.minimum_btc_transaction
        self.proc_config['fee'] = config_obj.btc_transaction_fee
        self.proc_config['bip32'] = True


    def does_wallet_exists(self):
        if not self.storage.file_exists:
            return False
        else:
            return True


    def restore_wallet_from_seed(self, seed):
        try:
            self.wallet = Wallet.from_seed(str(seed), self.storage)
            if not self.wallet:
                raise Exception('invalid seed')
            self.wallet.save_seed(self.__password__())
            self.wallet.create_accounts(self.__password__())
            self.wallet.start_threads(self.network)
            self.wallet.restore(lambda x: x)
            self.wallet.synchronize()
            #self.wallet.update()
            config_entry = Configuration.objects.get()
            config_entry.wallet_seed = str(seed)
            config_entry.save()
        except:
            exc_info = sys.exc_info()
            message = str(exc_info[0]) + ' - ' + str(exc_info[1])
            log_error('btc processor restore from seed', message)


    def create_or_load_wallet(self):
        wallet = Wallet(self.storage)
        if not self.storage.file_exists:
            try:
                seed = wallet.make_seed()
                wallet.init_seed(seed)
                wallet.save_seed(self.__password__())
                wallet.synchronize()
                config_entry = Configuration.objects.get()
                config_entry.wallet_seed = str(seed)
                config_entry.save()
            except Exception:
                exc_info = sys.exc_info()
                message = str(exc_info[0]) + ' - ' + str(exc_info[1])
                utils.log_error('btc processor create or load wallet', message)

        return wallet

    def check_balance(self):
        try:
            self.wallet.start_threads(self.network)
            self.wallet.update()
            balance = self.wallet.get_account_balance(self.wallet.accounts.get('Main account'))
        except:
            exc_info = sys.exc_info()
            message = str(exc_info[0]) + ' - ' + str(exc_info[1])
            utils.log_error('btc processor check balance', message)
            raise

        return balance

    def broadcast_transaction(self, dest_address, amount):
        try:
            satoshis_amount = utils.to_satoshis(float(amount))
            self.wallet.start_threads(self.network)
            tx = self.wallet.mktx([(dest_address, satoshis_amount)], self.__password__(), self.transaction_fee)
            res = self.wallet.sendtx(tx)
        except:
            exc_info = sys.exc_info()
            message = str(exc_info[0]) + ' - ' + str(exc_info[1])
            utils.log_error('btc processor broadcast transaction', message)
            raise

        return res # returns (Bool, transaction id)