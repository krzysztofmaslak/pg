import os
import sys
from flask import json
from werkzeug.security import generate_password_hash
from pg import User, Account, Offer, OfferItem, OfferItemVariation, Order, OrderItem, OrderItemVariation
from .. import *

__author__ = 'xxx'

from flask.ext.testing import TestCase as Base
from factory import ServiceFactory
from pg.app import App, db
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from base import *


class StripeTest(Base):
    environ_base={'REMOTE_ADDR': '127.0.0.1'}
    def create_app(self):
        self.ioc = TestServiceFactory()
        self.application = App(self.ioc)
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

    def test_proces(self):
        pass