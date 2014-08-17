from pg import service
import os

__author__ = 'xxx'


class ServiceFactory:
    logger = type("", (), dict(info=""))()

    def get_config(self):
        d = {
            'SQLALCHEMY_DATABASE_URI':'sqlite:////opt/database/justsale.sqlite',
            'SESSION_SECRET_KEY':'ASJAFLSDFJOWEJIFOWEJF',
            'IS_DEBUG':True,
            'MAIL_DEBUG':True,
            'PROJECT_VERSION':0.1,
            'UPLOAD_FOLDER':'/usr/share/nginx/html/justsale/static/images',
            'stripe.publishable':'pk_test_Ji7oZwG0vViJbhCaZjNHfRlX',
            'stripe.secret':'sk_test_b482pdSri7rYt2pzyzqtbISd',
            'paypal.seller':'seller_1302451451_biz@gmail.com',
            'paypal.url':'https://www.sandbox.paypal.com',
            'address.www':'https://www.justsale.it',
            'registration_email':'sales@justsale.it',
            'purchase_confirmation_email':'sales@justsale.it',
            'contact_email':'contact@justsale.it',
            'no_reply':'no-reply@justsale.it',
            'SKIP_ACCOUNT_ACTIVATION':True,
            'ENVIRONMENT':'DEV'
        }
        if 'PRODUCTION_SETTINGS' in os.environ:
            self.load_production_vars(d)
        return d

    def load_production_vars(self, d):
        with open(os.environ['PRODUCTION_SETTINGS']) as f:
            for line in f:
                key, value = line.split('=')
                d[key] = value.rstrip()

    def new_offer_service(self):
        return service.OfferService(self)

    def new_contact_service(self):
        return service.ContactService(self)

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
        return service.PaypalService(self, self.logger)

    def new_withdrawal_service(self):
        return service.WithdrawService(self)

    def new_event_service(self):
        return service.EventService(self)

    def new_image_service(self):
        return service.ImageService(self)