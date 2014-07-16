import hashlib
import json
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
        r = self.client.post('/rest/register/', data=json.dumps({'username':'admin', 'password':"abcd"}), content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        user = model.User.query.filter(model.User.username=='admin').first()
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.activation_hash)
        r = self.client.get('/login.html?h='+user.activation_hash+'&e='+hashlib.sha224(user.username.encode('utf-8')).hexdigest(), environ_base=self.environ_base)
        self.assertEqual(302, r.status_code)
        u = self.ioc.new_user_service().find_by_username('admin')
        self.assertIsNotNone(u)
        self.assertEqual(u.active, True)
