__author__ = 'xxx'
from werkzeug.security import generate_password_hash
from flask.ext.testing import TestCase as Base
from tests import base
from pg import model, app as application

class UserServiceTest(Base):

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

    def test_find_by_username(self):
        u = model.User('admin', 'password')
        model.base.db.session.add(u)
        model.base.db.session.commit()
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
            user = model.User('dublin.krzysztof.maslak@gmail.com', generate_password_hash('abcd'))
            user_service.add_user(user)
            user = user_service.find_by_username('dublin.krzysztof.maslak@gmail.com')
            self.assertIsNotNone(user)
