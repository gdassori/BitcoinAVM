# Bitcoin AVM, an open source Django base Bitcoin ATM
# https://github.com/mn3monic/BitcoinAVM


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BitVending.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
