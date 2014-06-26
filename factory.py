from pg.service import *
import os
from pg.service.country import CountryService
from pg.service.ipn import IpnMessageService
from pg.service.processor import PaymentProcessorService

__author__ = 'xxx'


class ServiceFactory:
    def get_config(self):
        d = {
            'SQLALCHEMY_DATABASE_URI':'sqlite:////data/sqlite/run.db',
            'SESSION_SECRET_KEY':'ASJAFLSDFJOWEJIFOWEJF',
            'IS_DEBUG':True,
            'PROJECT_VERSION':0.1,
            'UPLOAD_FOLDER':'/usr/share/nginx/html/pg/static/images',
            'stripe.publishable':'pk_test_Ji7oZwG0vViJbhCaZjNHfRlX',
            'stripe.secret':'sk_test_b482pdSri7rYt2pzyzqtbISd'
        }
        if 'PRODUCTION_SETTINGS' in os.environ:
            self.load_production_vars(d)
        return d

    def load_production_vars(d):
        with open(os.eniron['PRODUCTION_SETTINGS']) as f:
            for line in f:
                key, value = line.split('=')
                d[key] = value

    def new_offer_service(self):
        return OfferService(self)

    def new_order_service(self):
        return OrderService(self)

    def new_user_service(self):
        return UserService(self)

    def new_currency_service(self):
        return CurrencyService(self)

    def new_stripe_service(self):
        return StripeService(self)

    def new_ipn_message_service(self):
        return IpnMessageService(self)

    def new_invoice_service(self):
        return InvoiceService(self)

    def new_account_service(self):
        return AccountService(self)

    def new_property_service(self):
        return PropertyService(self)

    def new_email_service(self):
        return EmailService(self)

    def new_country_service(self):
        return CountryService(self)

    def new_payment_processor_service(self, logger):
        return PaymentProcessorService(self, logger)