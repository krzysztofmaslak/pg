from werkzeug.security import generate_password_hash

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
        user = model.User.query.filter(model.User.username=='admin').first()
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(user)
        r = self.client.post('/register.html', data={'username':'admin', 'password':"abcd"}, environ_base=self.environ_base)
        self.assertTrue(str(r.data).find('User already exist') != -1)

    def test_reset_password(self):
        a = model.Account()
        a.lang = 'en'
        a.properties.append(model.Property(a, 'sales.email', 'spreadline.limited@gmail.com'))
        u = model.User('dublin.krzysztof.maslak@gmail.com', 'password')
        u.active = True
        a.users.append(u)
        o = model.Offer(a)
        o.status = 1
        o1 = model.OfferItem(o, "My offer item", 2)
        o2 = model.OfferItem(o, "My offer item2")
        blue = model.OfferItemVariation(o2, "Blue", 3)
        red = model.OfferItemVariation(o2, "Red", 1)
        o2.variations = [blue, red]
        o.items.append(o1)
        o.items.append(o2)
        model.base.db.session.add(a)
        model.base.db.session.add(o)
        model.base.db.session.commit()
        r = self.client.post('/reset_password.html', data={'username':'dublin.krzysztof.maslak@gmail.com'}, environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)
        emails = self.ioc.new_email_service().find_unprocessed()
        self.assertIsNotNone(emails)
        self.assertEqual(1, len(emails))
        self.assertEqual('RESET_PASSWORD', emails[0].type)
        u = self.ioc.new_user_service().find_by_username(u.username)
        self.assertIsNotNone(u.reset_hash)