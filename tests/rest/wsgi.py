__author__ = 'xxx'

from flask.ext.testing import TestCase as Base
from pg import model, app as application
import mock
import copy
from tests import base

class WsgiTest(Base):
    environ_base={'REMOTE_ADDR': '127.0.0.1'}

    def create_app(self):
        self.ioc = base.TestServiceFactory()
        self.application = application.App(self.ioc)
        app = self.application.create_app()
        app.testing = True
        self.client = app.test_client()
        return app

    def setUp(self):
        self.application.init_db()

    def tearDown(self):
        pass
        # db.session.remove()
        # db.drop_all()

    def test_register(self):
        r = self.client.post('/register.html', data={'username':'admin', 'password':"abcd"}, environ_base=self.environ_base)
        user = self.ioc.new_user_service().find_by_username('admin')
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(user)
        r = self.client.post('/register.html', data={'username':'admin', 'password':"abcd"}, environ_base=self.environ_base)
        self.assertEqual(409, r.status_code)

    def test_reset_password(self):
        r = self.client.post('/register.html', data={'username':'admin', 'password':"abcd"}, environ_base=self.environ_base)
        user = self.ioc.new_user_service().find_by_username('admin')
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(user)
        r = self.client.post('/reset_password.html', data={'username':'admin'}, environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)
        emails = self.ioc.new_email_service().find_unprocessed()
        self.assertIsNotNone(emails)
        self.assertEqual(1, len(emails))
        self.assertEqual('RESET_PASSWORD', emails[0].type)