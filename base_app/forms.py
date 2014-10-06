# Bitcoin AVM, an open source Django base Bitcoin ATM
# https://github.com/mn3monic/BitcoinAVM

from django import forms
import bitcoinaddress

class AddressForm(forms.Form):
    address = forms.CharField()

    def clean_address(self):
        address = self.cleaned_data['address']
        if not bitcoinaddress.validate(address):
            raise forms.ValidationError("Invalid Bitcoin Address")
        return address
