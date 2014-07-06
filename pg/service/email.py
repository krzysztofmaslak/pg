import traceback
from flask import render_template
from flask.ext.mail import Message
from pg import model

__author__ = 'krzysztof.maslak'

class EmailHandler:
    def __init__(self, mail, logger):
        self.mail = mail
        self.logger = logger

    def send(self, email):
        msg = Message(email.subject, sender= email.from_address, recipients= [email.to_address])
        msg.html = email.html
        self.mail.send(msg)

class PurchaseConfirmationAdminEmailHandler(EmailHandler):
    def handle(self, email):
        email.html = '--'
        self.send(email)

class PurchaseConfirmationEmailHandler(EmailHandler):
    def handle(self, email):
        email.html = render_template('emails/'+email.language+'/purchase-confirmation.html')
        self.logger.debug('Purchase confirmation: %s'%email.html)
        self.send(email)

class EmailService:

    def __init__(self, ioc, logger, mail):
        super().__init__()
        self.ioc = ioc
        self.logger = logger
        self.mail = mail
        self.email_handlers = {
            'PURCHASE_CONFIRMATION':PurchaseConfirmationEmailHandler(self.mail, self.logger),
            'PURCHASE_CONFIRMATION_ADMIN':PurchaseConfirmationAdminEmailHandler(self.mail, self.logger)
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
                        except Exception as err:
                            traceback.print_tb(err.__traceback__)
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