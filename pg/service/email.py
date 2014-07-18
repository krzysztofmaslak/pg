import hashlib
import traceback
from flask import render_template
from flask.ext.mail import Message
from werkzeug.security import generate_password_hash
from pg import model

__author__ = 'krzysztof.maslak'

class EmailHandler:
    def __init__(self, mail, ioc, logger):
        self.mail = mail
        self.ioc = ioc
        self.logger = logger

    def send(self, email):
        self.mail.send(email)

class ResetPasswordEmailHandler(EmailHandler):
    def handle(self, email):
        user = self.ioc.new_user_service().find_by_id(int(email.ref_id))
        msg = Message(email.subject, sender= email.from_address, recipients= [email.to_address])
        msg.html = render_template('emails/'+str(email.language)+'/reset-password.html',
                                     username = user.username,
                                     website_address = self.ioc.get_config()['address.www'],
                                     reset_hash = user.reset_hash,
                                     email_hash=hashlib.sha224(user.username.encode('utf-8')).hexdigest()
                                     )
        self.logger.debug('Reset password: %s'%msg.html)
        self.send(msg)

class RegistrationEmailHandler(EmailHandler):
    def handle(self, email):
        user = self.ioc.new_user_service().find_by_id(int(email.ref_id))
        msg = Message(email.subject, sender= email.from_address, recipients= [email.to_address])
        msg.html = render_template('emails/'+str(email.language)+'/registration.html',
                                     username = user.username,
                                     website_address = self.ioc.get_config()['address.www'],
                                     activation_hash = user.activation_hash,
                                     email_hash=hashlib.sha224(user.username.encode('utf-8')).hexdigest()
                                     )
        self.logger.debug('Registration email: %s'%msg.html)
        self.send(msg)

class PurchaseConfirmationAdminEmailHandler(EmailHandler):
    def handle(self, email):
        msg = Message(email.subject, sender= email.from_address, recipients= [email.to_address])
        msg.html = '--'
        self.send(msg)

class RegistrationAdminEmailHandler(EmailHandler):
    def handle(self, email):
        msg = Message(email.subject, sender= email.from_address, recipients= [email.to_address])
        msg.html = '--'
        self.send(msg)

class PurchaseConfirmationEmailHandler(EmailHandler):
    def handle(self, email):
        order = self.ioc.new_order_service().find_by_id(int(email.ref_id))
        address = order.billing[0].address1
        if order.billing[0].address2 is not None and len(order.billing[0].address2):
            address += ' '+order.billing[0].address2
        shipping = order.shipping.first()
        if shipping is None:
            shipping = order.billing[0]
        shipment_first_name = shipping.first_name
        shipment_last_name = shipping.last_name
        shipment_address = shipping.address1
        if shipping.address2 is not None and len(shipping.address2):
            shipment_address += ' '+shipping.address2
        shipment_city = shipping.city

        i = 0
        shipping = 0.0
        basket_items = []
        for item in order.items:
            if item.variations is not None and item.variations.count()>0:
                itotal = 0.0
                for iv in item.variations:
                    itotal = itotal+((iv.quantity*(iv.net+iv.tax)))
                    if iv.quantity==1:
                        shipping = shipping + iv.shipping
                    else:
                        for c in range(iv.quantity-1):
                            if iv.shipping_additional is not None:
                                shipping = shipping + iv.shipping_additional
                            else:
                                shipping = shipping + iv.shipping
                    if order.offer.currency!=order.currency:
                        basket_items.append({'index':(i+1), 'title':item.title+'('+iv.title+')', 'quantity':iv.quantity, 'value':self.ioc.new_currency_service().convert(order.currency, itotal)})
                    else:
                        basket_items.append({'index':(i+1), 'title':item.title+'('+iv.title+')', 'quantity':iv.quantity, 'value': itotal})
                    i = i+1
            else:
                if order.offer.currency!=order.currency:
                    basket_items.append({'index':(i+1), 'title':item.title, 'quantity':item.quantity,'value':self.ioc.new_currency_service().convert(order.currency, (item.quantity*(item.net+item.tax)))})
                else:
                    basket_items.append({'index':(i+1), 'title':item.title, 'quantity':item.quantity, 'value':(item.quantity*(item.net+item.tax))})
                if item.quantity==1:
                    shipping = shipping + item.shipping
                else:
                    for c in range(item.quantity-1):
                        if item.shipping_additional is not None:
                            shipping = shipping + item.shipping_additional
                        else:
                            shipping = shipping + item.shipping
                i = i+1
        email.html = render_template('emails/'+email.language+'/purchase-confirmation.html',
                                     order_number = order.order_number,
                                     creation_date = order.creation_date,
                                     email = order.billing[0].email,
                                     first_name = order.billing[0].first_name,
                                     last_name = order.billing[0].last_name,
                                     address = address,
                                     post_code= order.billing[0].postal_code,
                                     city= order.billing[0].city,
                                     shipment_first_name = shipment_first_name,
                                     shipment_last_name = shipment_last_name,
                                     shipment_address = shipment_address,
                                     shipment_city = shipment_city,
                                     items= basket_items
                                     )
        self.logger.debug('Purchase confirmation: %s'%email.html)
        self.send(email)

class EmailService:

    def __init__(self, ioc, logger, mail):
        super().__init__()
        self.ioc = ioc
        self.logger = logger
        self.mail = mail
        self.email_handlers = {
            'PURCHASE_CONFIRMATION':PurchaseConfirmationEmailHandler(self.mail, self.ioc, self.logger),
            'PURCHASE_CONFIRMATION_ADMIN':PurchaseConfirmationAdminEmailHandler(self.mail, self.ioc, self.logger),
            'RESET_PASSWORD':ResetPasswordEmailHandler(self.mail, self.ioc, self.logger),
            'REGISTRATION_ADMIN':RegistrationAdminEmailHandler(self.mail, self.ioc, self.logger),
            'REGISTRATION':RegistrationEmailHandler(self.mail, self.ioc, self.logger)

        }

    def set_mail(self, m):
        for handler in self.email_handlers:
            self.email_handlers[handler].mail = m

    def process_emails(self):
        with self.ioc.app.app_context():
            emails = self.find_unprocessed()
            if emails is not None and len(emails)>0:
                for email in emails:
                    handler = self.email_handlers[email.type]
                    if handler is not None:
                        try:
                            self.logger.debug('Processing email [type=%s, id=%s]'%(email.type, email.id))
                            handler.handle(email)
                            db_email = model.Email.query.get(email.id)
                            db_email.status = 1
                            model.base.db.session.commit()
                            self.logger.debug('Email processed [type=%s, id=%s]'%(email.type, email.id))
                        except Exception as err:
                            traceback.print_tb(err.__traceback__)
                            traceback.print_exc()
                            self.logger.warn("Failed to process email EmailService.process_emails %s"%email.type)
                    else:
                        self.logger.warn("No email handler defined in EmailService.process_emails %s"%email.type)
                model.base.db.session.commit()


    def find_unprocessed(self):
        with self.ioc.app.app_context():
            return model.Email.query.filter(model.Email.status==0).all()

    def save(self, email):
        if isinstance(email, model.Email):
            model.base.db.session.add(email)
            model.base.db.session.commit()
            return email
        else:
            raise TypeError("Expected Email type in EmailService.save %s"%type(email))