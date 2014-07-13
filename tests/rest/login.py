from werkzeug.security import generate_password_hash

__author__ = 'xxx'

import json
from flask.ext.testing import TestCase as Base
from pg import model, app as application
from tests import base

class LoginTest(Base):
    environ_base={'REMOTE_ADDR': '127.0.0.1'}

    def create_app(self):
        self.ioc = base.TestServiceFactory()
        self.application = application.App(self.ioc)
        self.app = self.application.create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        return self.app

    def setUp(self):
        LoginTest.templates = []
        self.application.init_db()
        self.client = self.app.test_client()

    def tearDown(self):
        self.client = None

    def test_login(self):
        a = model.Account()
        u = model.User('test@justsale.it', generate_password_hash('password'))
        u.active = True
        a.users.append(u)
        model.base.db.session.add(a)
        model.base.db.session.commit()

        r = self.client.post('/rest/login/', data=json.dumps({'username':'test@justsale.it', 'password':'password1'}), content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        self.assertEqual(409, r.status_code)
        r = self.client.post('/rest/login/', data=json.dumps({'username':'test@justsale.it', 'password':'password'}), content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)


