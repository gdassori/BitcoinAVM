# Bitcoin AVM, an open source Django base Bitcoin ATM
# https://github.com/mn3monic/BitcoinAVM


from django.conf.urls import patterns, include, url
from base_app.views import *
from django.contrib.auth.views import login
from django.contrib import admin
from django.views.generic import TemplateView
from BitVending.settings import STATIC_ROOT_DEVELOPMENT, DEBUG
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BitVending.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', index),

    url(r'^machine_status$', machine_status),
    url(r'^transaction/$', transaction_init),
    url(r'^read_address', read_address),
    url(r'^notes_status$', check_notes_reader_status),
    url(r'^confirm_payment$', confirm_payment),
    url(r'^set_address$', set_address),
    url(r'^create_wallet$', create_wallet),
    url(r'^restore_from_seed$', restore_from_seed),
    url(r'^wallet$', wallet),

    url(r'^test$', test),


    # url(r'^api/peripherals/(\w+)$', api_peripherals), # GET
    # url(r'^api/general_status/(\w+)$', api_general_status), # GET
    # url(r'^api/dest_address$', api_address), # POST
    # url(r'^api/payment$', api_notes_acceptor),

    url(r'^admin/', include(admin.site.urls)),

    # static buy page
    #url(r'^buy/?', TemplateView.as_view(template_name="buy.html")),


)

#if DEBUG:
#    urlpatterns += patterns('',
#                            url(r'^static/(.*)$',
#                                'django.views.static.serve',
#                                {'document_root': STATIC_ROOT_DEVELOPMENT, 'show_indexes': True}
#                            )
#    )