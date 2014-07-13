import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from pg.wsgi import get_sha_part

__author__ = 'xxx'

from flask.ext.testing import TestCase as Base
from pg import model, app as application
from flask import _request_ctx_stack
from tests import base

class WsgiTest(Base):
    environ_base={'REMOTE_ADDR': '127.0.0.1'}

    def create_app(self):
        self.ioc = base.TestServiceFactory()
        self.application = application.App(self.ioc)
        self.app = self.application.create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        return self.app

    def setUp(self):
        WsgiTest.templates = []
        self.application.init_db()
        self.client = self.app.test_client()

    def tearDown(self):
        self.client = None

    def get_sha_part(self, hash):
        return hash[len('pbkdf2:sha1:'):]

    def test_activate(self):
        r = self.client.post('/register.html', data={'username':'admin', 'password':"abcd"}, environ_base=self.environ_base)
        user = model.User.query.filter(model.User.username=='admin').first()
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.activation_hash)
        r = self.client.get('/login.html?h='+user.activation_hash+'&e='+hashlib.sha224(user.username.encode('utf-8')).hexdigest(), environ_base=self.environ_base)
        self.assertEqual(302, r.status_code)
        u = self.ioc.new_user_service().find_by_username('admin')
        self.assertIsNotNone(u)
        self.assertEqual(u.active, True)

    def test_reset_password(self):
        a = model.Account()
        a.lang = 'en'
        a.properties.append(model.Property(a, 'sales.email', 'spreadline.limited@gmail.com'))
        u = model.User('dublin.krzysztof.maslak@gmail.com', 'password')
        u.active = True
        a.users.append(u)
        model.base.db.session.add(a)
        model.base.db.session.commit()
        r = self.client.post('/reset_password.html', data={'username':'dublin.krzysztof.maslak@gmail.com'}, environ_base=self.environ_base)
        self.assertEqual(302, r.status_code)
        u = self.ioc.new_user_service().find_by_username('dublin.krzysztof.maslak@gmail.com')
        self.assertIsNotNone(u)
        self.assertIsNotNone(u.reset_hash)

    def test_new_password(self):
        a = model.Account()
        a.lang = 'en'
        a.properties.append(model.Property(a, 'sales.email', 'spreadline.limited@gmail.com'))
        u = model.User('dublin.krzysztof.maslak@gmail.com',generate_password_hash('password'))
        u.active = True
        a.users.append(u)
        model.base.db.session.add(a)
        model.base.db.session.commit()
        r = self.client.post('/reset_password.html', data={'username':'dublin.krzysztof.maslak@gmail.com'}, environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)
        u = self.ioc.new_user_service().find_by_username('dublin.krzysztof.maslak@gmail.com')
        self.assertIsNotNone(u)
        self.assertIsNotNone(u.reset_hash)
        r = self.client.post('/new_password.html', data={'password':'abcde', 'confirmPassword':'abcde', 'h':u.reset_hash,
                                                         'e':hashlib.sha224(u.username.encode('utf-8')).hexdigest()}, environ_base=self.environ_base)
        self.assertEqual(302, r.status_code)
        u = self.ioc.new_user_service().find_by_username('dublin.krzysztof.maslak@gmail.com')
        self.assertIsNotNone(u)
        self.assertFalse(check_password_hash(u.password, "password"))
        self.assertTrue(check_password_hash(u.password, "abcde"))

    def test_reset_password(self):
        a = model.Account()
        a.lang = 'en'
        a.properties.append(model.Property(a, 'sales.email', 'spreadline.limited@gmail.com'))
        u = model.User('dublin.krzysztof.maslak@gmail.com', 'password')
        u.active = True
        a.users.append(u)
        model.base.db.session.add(a)
        model.base.db.session.commit()
        r = self.client.post('/reset_password.html', data={'username':'dublin.krzysztof.maslak@gmail.com'}, environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)
        emails = self.ioc.new_email_service().find_unprocessed()
        self.assertIsNotNone(emails)
        self.assertEqual(1, len(emails))
        self.assertEqual('RESET_PASSWORD', emails[0].type)
        u = self.ioc.new_user_service().find_by_username('dublin.krzysztof.maslak@gmail.com')
        self.assertIsNotNone(u.reset_hash)
        model.base.db.session.commit()