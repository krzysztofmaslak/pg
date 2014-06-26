__author__ = 'xxx'
from flask.ext.testing import TestCase as Base
from pg import model, app as application
from tests import base

class CurrencyServiceTest(Base):

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

    def test_list(self):
        model.base.db.session.add(model.Currency('eur', 1))
        model.base.db.session.add(model.Currency('gbp', 1))
        model.base.db.session.add(model.Currency('usd', 1))
        model.base.db.session.add(model.Currency('jpy', 1))
        model.base.db.session.add(model.Currency('aud', 1))
        model.base.db.session.commit()
        currency_service = self.ioc.new_currency_service()
        currencies = currency_service.list()
        self.assertIsNotNone(currencies)
        self.assertEquals(5, len(currencies))

    def test_save_rate(self):
        rate = model.CurrencyRate('eur', 1.4323)
        saved_rate = self.ioc.new_currency_service().save_rate(rate);
        self.assertIsNotNone(saved_rate)
        self.assertEquals(1.4323, saved_rate.rate)
