__author__ = 'xxx'
from flask.ext.testing import TestCase as Base
from pg import model, app as application
from tests import base

class InvoiceServiceTest(Base):

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

    def test_new_invoice_from_order(self):
        pass