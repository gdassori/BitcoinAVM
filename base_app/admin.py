# Bitcoin AVM, an open source Django base Bitcoin ATM
# https://github.com/mn3monic/BitcoinAVM

from django.contrib import admin
from base_app.models import Configuration

# Register your models here.
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('active',
                    'surcharge',
                    'VAT',
                    'max_cash_per_transaction',
                    'btc_transaction_fee',
                    'currency',
                    'wallet_seed',
                    'wallet_password',
                    'wallet_path')


admin.site.register(Configuration, ConfigurationAdmin)
