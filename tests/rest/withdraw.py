__author__ = 'root'

import mock
from flask import json
from werkzeug.security import generate_password_hash
from tests import base
from pg import model, app as application
from flask.ext.testing import TestCase as Base


class WithdrawTest(Base):
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

    def test_balance(self):
        a = model.Account()
        u = model.User('admin', generate_password_hash('abcd'))
        a.users.append(u)
        a.balance = 14.30
        model.base.db.session.add(a)
        model.base.db.session.commit()

        r = self.client.get('/rest/withdraw/balance', environ_base=self.environ_base)
        self.assertEqual(401, r.status_code)

        r = self.client.post('/login.html', data={'username':u.username, 'password':"abcd"}, environ_base=self.environ_base)
        self.assertEqual(302, r.status_code)
        r = self.client.get('/rest/withdraw/balance', environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)
        self.assertEqual(14.30, r.json['balance'])

    def test_request_withdrawal(self):
        a = model.Account()
        u = model.User('admin', generate_password_hash('abcd'))
        a.users.append(u)
        a.balance = 14.30
        model.base.db.session.add(a)
        model.base.db.session.commit()

        r = self.client.post('/rest/withdraw/request', data={'amount':7, 'iban':'12341412414', 'bic':'FFKJD'}, content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        self.assertEqual(401, r.status_code)

        r = self.client.post('/login.html', data={'username':u.username, 'password':"abcd"}, environ_base=self.environ_base)
        self.assertEqual(302, r.status_code)
        r = self.client.post('/rest/withdraw/request', data={'amount':14.31, 'iban':'12341412414', 'bic':'FFKJD'}, content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        self.assertEqual(400, r.status_code)
        r = self.client.post('/rest/withdraw/request', data={'amount':14.30, 'iban':'12341412414', 'bic':'FFKJD'}, content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)
