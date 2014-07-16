from werkzeug.security import generate_password_hash

__author__ = 'xxx'

import json
from flask.ext.testing import TestCase as Base
from pg import model, app as application
from tests import base

class ContactTest(Base):
    environ_base={'REMOTE_ADDR': '127.0.0.1'}

    def create_app(self):
        self.ioc = base.TestServiceFactory()
        self.application = application.App(self.ioc)
        self.app = self.application.create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        return self.app

    def setUp(self):
        ContactTest.templates = []
        self.application.init_db()
        self.client = self.app.test_client()

    def tearDown(self):
        self.client = None

    def test_new_message(self):
        r = self.client.post('/rest/contact/', data=json.dumps({'email':'test@justsale.it', 'message':'password1'}), content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)
        contacts = model.Contact.query.all()
        self.assertNotNull(contacts)
        self.assertEqual(1, len(contacts))
