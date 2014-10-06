# Bitcoin AVM, an open source Django base Bitcoin ATM
# https://github.com/mn3monic/BitcoinAVM

import time
from base_app.models import Transactions, Configuration
from base_app.utils import log_error
from datetime import datetime


def notes_reader_worker(command_queue, session_id, available_coins):
    notes_reader = NotesReader(command_queue, session_id, available_coins)
    notes_reader.enable_reader()


class NotesReader():
    def __init__(self, command_queue, session_id, available_coins):
        self.command_queue = command_queue
        self.session_id = session_id
        self.inserted_cash = 0
        self.surcharge = 0
        self.available_coins = available_coins
        self.btc_amount = 0

        try:
            self.transaction = Transactions.objects.get(session_id=self.session_id)
            self.transaction.status = Transactions.INSERTING_CASH
            self.transaction.updated_on = datetime.now()
            self.initial_max_acceptable_cash = self.transaction.max_cash_acceptable
            self.transaction.save()
        except Transactions.DoesNotExist:
            log_error('Notes reader', 'transaction ' + self.session_id + ' does not exists')
            raise

        try:
            configuration = Configuration.objects.get()
            self.config_surcharge = configuration.surcharge
        except Configuration.DoesNotExist:
            log_error('Notes reader', 'Configuration not found.')
            raise


    def enable_reader(self):
        # enable the reader here
        # loop up until the disable message is received on the command_queue
        # push status updates to the status_queue whenever money are inserted
        #TODO: send ccTalk msg to enable reader

        disabled = False
        while not disabled:
            # use whatever library here to interact with the actual notes reader
            # and save the new status in the transactions table for the frontend to read

            #TODO: implement here - using the ccTalk library
            #TODO: poll the notes reader with ccTalk - update status in transactions table and stay in this loop until the
            #TODO: disable command is received
            # TEST CODE HERE , SIMULATING NOTES INSERTION -  TO REMOVE
            notes_inserted = 0.01
            time.sleep(2)
            #TODO: implement the logic here to make the notes reader accept only notes according to max acceptable cash

            self.inserted_cash += notes_inserted
            # END OF TEST CODE

            self.btc_amount = float(self.inserted_cash/self.transaction.exchange_rate)
            surcharge = self.btc_amount*self.config_surcharge
            self.btc_amount -= surcharge

            self.transaction.cash_amount = self.inserted_cash
            self.transaction.btc_amount = self.btc_amount
            self.transaction.surcharge = surcharge
            self.transaction.max_cash_acceptable = self.initial_max_acceptable_cash - ((self.available_coins-self.btc_amount)*self.transaction.exchange_rate)
            self.transaction.updated_on = datetime.now()
            self.transaction.save()

            # check if the disable command has been sent
            if not self.command_queue.empty():
                disabled = self.command_queue.get()


        # it should get here when the disable command is received
        return
