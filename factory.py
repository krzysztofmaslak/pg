from pg import service
import os

__author__ = 'xxx'


class ServiceFactory:
    logger = type("", (), dict(info=""))()

    def get_config(self):
        d = {
            'SQLALCHEMY_DATABASE_URI':'sqlite:////data/sqlite/run.db',
            'SESSION_SECRET_KEY':'ASJAFLSDFJOWEJIFOWEJF',
            'IS_DEBUG':True,
            'PROJECT_VERSION':0.1,
            'UPLOAD_FOLDER':'/usr/share/nginx/html/pg/static/images',
            'stripe.publishable':'pk_test_Ji7oZwG0vViJbhCaZjNHfRlX',
            'stripe.secret':'sk_test_b482pdSri7rYt2pzyzqtbISd',
            'paypal.authToken':'BkRqdeXwVMD7RMSw03xAwrwyyG9cs14DZH5XZud_oRZH9SPpfRH2k9_KhtO',
            'paypal.seller':'seller_1302451451_biz@gmail.com',
            'paypal.url':'https://www.sandbox.paypal.com/cgi-bin/webscr',
            'address.www':'https://www.justsale.it',
            'registration_email':'sales@justsale.it',
            'no_reply':'no-reply@justsale.it',
        }
        if 'PRODUCTION_SETTINGS' in os.environ:
            self.load_production_vars(d)
        return d

    def load_production_vars(self, d):
        with open(os.eniron['PRODUCTION_SETTINGS']) as f:
            for line in f:
                key, value = line.split('=')
                d[key] = value

    def new_offer_service(self):
        return service.OfferService(self)

    def new_inovice_service(self):
        return service.InvoiceService(self)

    def new_order_service(self):
        return service.OrderService(self, self.logger)

    def new_user_service(self):
        return service.UserService(self)

    def new_currency_service(self):
        return service.CurrencyService(self)

    def new_stripe_service(self):
        return service.StripeService(self)

    def new_ipn_message_service(self):
        return service.IpnMessageService(self)

    def new_invoice_service(self):
        return service.InvoiceService(self)

    def new_account_service(self):
        return service.AccountService(self)

    def new_property_service(self):
        return service.PropertyService(self)

    def new_email_service(self):
        return service.EmailService(self, self.logger, self.mail)

    def new_country_service(self):
        return service.CountryService(self)

    def new_payment_processor_service(self):
        return service.PaymentProcessorService(self, self.logger)

    def new_paypal_service(self):
        return service.PaypalService(self)

    def new_withdrawal_service(self):
        return service.WithdrawService(self)