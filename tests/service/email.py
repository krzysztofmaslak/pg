from flask.ext.mail import Message
import mock

__author__ = 'root'

from flask.ext.testing import TestCase as Base
from pg import model, app as application
from tests import base

class EmailServiceTest(Base):

    def create_app(self):
        self.ioc = base.TestServiceFactory()
        self.application = application.App(self.ioc)
        app = self.application.create_app()
        app.testing = True
        return app

    def setUp(self):
        self.application.init_db()

    def tearDown(self):
        pass
        # db.session.remove()
        # db.drop_all

    def test_save(self):
        email = model.Email()
        saved_email = self.ioc.new_email_service().save(email);
        self.assertIsNotNone(saved_email)

    def test_find_unprocessed(self):
        for i in range(11):
            email = model.Email()
            saved_email = self.ioc.new_email_service().save(email);
        unprocessed_emails = self.ioc.new_email_service().find_unprocessed()
        self.assertEqual(11, len(unprocessed_emails))

    def test_process_emails_admin_confirmation(self):
        email = model.Email()
        email.subject = 'Admin purchase confirmation subject'
        email.from_address = 'test@test.ie'
        email.to_address = 'test-to@test.ie'
        email.type='PURCHASE_CONFIRMATION_ADMIN'
        self.ioc.new_email_service().save(email)
        unprocessed_emails = self.ioc.new_email_service().find_unprocessed()
        self.assertEqual(1, len(unprocessed_emails))
        email_service = self.ioc.new_email_service()
        mock_send = mock.MagicMock()
        mock_mail = mock.MagicMock()
        mock_mail.send = mock_send
        email_service.set_mail(mock_mail)
        email_service.process_emails()
        mock_send.assert_called_once_with(mock.ANY)
