__author__ = 'xxx'
from werkzeug.security import generate_password_hash
from pg.model import User, Currency, CurrencyRate
import os
import sys
from flask.ext.testing import TestCase as Base
from pg.app import App, db
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from base import *


class CurrencyServiceTest(Base):

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

    def test_list(self):
        db.session.add(Currency('eur', 1))
        db.session.add(Currency('gbp', 1))
        db.session.add(Currency('usd', 1))
        db.session.add(Currency('jpy', 1))
        db.session.add(Currency('aud', 1))
        db.session.commit()
        currency_service = self.ioc.new_currency_service()
        currencies = currency_service.list()
        self.assertIsNotNone(currencies)
        self.assertEquals(5, len(currencies))

    def test_save_rate(self):
        rate = CurrencyRate('eur', 1.4323)
        saved_rate = self.ioc.new_currency_service().save_rate(rate);
        self.assertIsNotNone(saved_rate)
        self.assertEquals(1.4323, saved_rate.rate)
