import hashlib
from werkzeug.security import generate_password_hash, check_password_hash

__author__ = 'xxx'

import json
from flask.ext.testing import TestCase as Base
from pg import model, app as application
from tests import base

class PasswordTest(Base):
    environ_base={'REMOTE_ADDR': '127.0.0.1'}

    def create_app(self):
        self.ioc = base.TestServiceFactory()
        self.application = application.App(self.ioc)
        self.app = self.application.create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        return self.app

    def setUp(self):
        PasswordTest.templates = []
        self.application.init_db()
        self.client = self.app.test_client()

    def tearDown(self):
        self.client = None

    def test_reset(self):
        a = model.Account()
        a.lang='en'
        u = model.User('test@justsale.it', generate_password_hash('password'))
        u.active = True
        a.users.append(u)
        model.base.db.session.add(a)
        model.base.db.session.commit()

        r = self.client.post('/rest/password/reset', data=json.dumps({'username':'test@justsale.it'}), content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        user = model.User.query.filter(model.User.username=='test@justsale.it').first()
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.reset_hash)
        r = self.client.post('/rest/password/reset', data=json.dumps({'username':'test1@justsale.it'}), content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        self.assertEqual(204, r.status_code)
        emails = self.ioc.new_email_service().find_unprocessed()
        self.assertIsNotNone(emails)
        self.assertEqual(1, len(emails))
        self.assertEqual('RESET_PASSWORD', emails[0].type)

    def test_new_password(self):
        a = model.Account()
        a.lang = 'en'
        u = model.User('test@justsale.it',generate_password_hash('password'))
        u.active = True
        a.users.append(u)
        model.base.db.session.add(a)
        model.base.db.session.commit()
        r = self.client.post('/rest/password/reset', data=json.dumps({'username':'test@justsale.it'}), content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        user = model.User.query.filter(model.User.username=='test@justsale.it').first()
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.reset_hash)
        r = self.client.post('/rest/password/new', data=json.dumps({
            'password':'abcde', 'confirmPassword':'abcde',
            'h':u.reset_hash, 'e':hashlib.sha224(u.username.encode('utf-8')).hexdigest()
        }), content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)
        u = self.ioc.new_user_service().find_by_username('test@justsale.it')
        self.assertIsNotNone(u)
        self.assertFalse(check_password_hash(u.password, "password"))
        self.assertTrue(check_password_hash(u.password, "abcde"))
