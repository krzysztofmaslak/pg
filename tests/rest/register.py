__author__ = 'xxx'

import json
from flask.ext.testing import TestCase as Base
from pg import model, app as application
from tests import base

class RegisterTest(Base):
    environ_base={'REMOTE_ADDR': '127.0.0.1'}

    def create_app(self):
        self.ioc = base.TestServiceFactory()
        self.application = application.App(self.ioc)
        self.app = self.application.create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        return self.app

    def setUp(self):
        RegisterTest.templates = []
        self.application.init_db()
        self.client = self.app.test_client()

    def tearDown(self):
        self.client = None

    def test_register(self):
        r = self.client.post('/rest/register/', data=json.dumps({'username':'test@justsale.it', 'name':'test', 'password':'123'}), content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        user = model.User.query.filter(model.User.username=='test@justsale.it').first()
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.activation_hash)
        r = self.client.post('/rest/register/', data=json.dumps({'username':'test@justsale.it', 'name':'test', 'password':'123'}), content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        self.assertEqual(409, r.status_code)


