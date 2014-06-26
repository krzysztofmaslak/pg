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


class PaymentTest(Base):
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

    def test_apply_payment(self):
        u = User('admin', 'password')
        o = Offer(u)
        o.status = 1
        o1 = OfferItem(o, "My offer item", 2)
        o2 = OfferItem(o, "My offer item2")
        blue = OfferItemVariation(o2, "Blue", 3)
        red = OfferItemVariation(o2, "Red", 1)
        o2.variations = [blue, red]
        o.items.append(o1)
        o.items.append(o2)
        db.session.add(u)
        db.session.add(o)
        db.session.commit()

        order = Order()
        order.offer_id = o.id
        or1 = OrderItem(order, 'Strings', 1, 10.32, 0, 1.65)
        or1.shipping_additional = 1
        or1.offer_item_id = o1.id
        order.items.append(or1)
        oi = OrderItem(order, 'Toy', 0, 0, 0, 0)
        oi.offer_item_id = o2.id
        orv1 = OrderItemVariation(oi, "Big", 1, 11.21, 0, 1.65)
        orv1.shipping_additional = 1
        orv1.offer_item_variation_id = blue.id
        oi.variations.append(orv1)
        order.items.append(oi)
        db.session.add(order)
        db.session.commit()

        items = [An(id=o1.id, quantity=1, variations=[])]
        payment = An(offer_id=o.id, subscribe=True, payment_method='cc', currency='eur', country='fr', lang='eng', session_id='kdkdkdkd', items=items)
        payment.billing = An(first_name='Mickey', last_name='Mouse', address1='Withworth', address2='Drumcondra', country='ie', city='Dublin', postal_code='10', county='Dublin', email='dublin.krzysztof.maslak@gmail.com', same_address=False)
        payment.shipping = An(first_name='Chuck', last_name='Norris', address1='South Central', address2='Rockbrook', country='ie', city='Dublin', postal_code='18', county='Dublin', email='krzysztof.maslak@123.ie', company='Spreadline', phone_number='0842342342')

        r = self.client.post('/rest/payment/', data=json.dumps(payment.as_json()), content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(r.json['id'])
        self.assertTrue(r.json['id']>0)

