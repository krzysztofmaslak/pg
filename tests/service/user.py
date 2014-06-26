__author__ = 'xxx'
from werkzeug.security import generate_password_hash
from pg.model import User
import os
import sys
from flask.ext.testing import TestCase as Base
from pg.app import App, db
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from base import *


class UserServiceTest(Base):

    def create_app(self):
        self.ioc = TestServiceFactory()
        self.application = App(self.ioc)
        app = self.application.create_app()
        app.testing = True
        return app

    def setUp(self):
        self.application.init_db()

    def tearDown(self):
        pass
        # db.session.remove()
        # db.drop_all

    def test_find_by_username(self):
        u = User('admin', 'password')
        db.session.add(u)
        db.session.commit()
        user_service = self.ioc.new_user_service()
        user = user_service.find_by_username('noname')
        self.assertIsNone(user)
        user = user_service.find_by_username('admin')
        self.assertIsNotNone(user)

    def test_add_user(self):
        with self.app.app_context():
            user_service = self.ioc.new_user_service()
            user = user_service.find_by_username('dublin.krzysztof.maslak@gmail.com')
            self.assertIsNone(user)
            user = User('dublin.krzysztof.maslak@gmail.com', generate_password_hash('abcd'))
            user_service.add_user(user)
            user = user_service.find_by_username('dublin.krzysztof.maslak@gmail.com')
            self.assertIsNotNone(user)
