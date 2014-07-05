import mock

__author__ = 'xxx'
from flask import json
from werkzeug.security import generate_password_hash
from tests import base
from pg import model, app as application
from flask.ext.testing import TestCase as Base


class OfferTest(Base):
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

    def test_list(self):
        a = model.Account()
        u = model.User('admin', generate_password_hash('abcd'))
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

        order = model.Order()
        order.account_id = a.id
        order.payment_status = 'Completed'
        order.offer_id = o.id
        or1 = model.OrderItem(order, 'Strings', 1, 10.32, 0, 1.65)
        or1.shipping_additional = 1
        or1.offer_item_id = o1.id
        order.items.append(or1)
        oi = model.OrderItem(order, 'Toy', 0, 0, 0, 0)
        oi.offer_item_id = o2.id
        orv1 = model.OrderItemVariation(oi, "Big", 1, 11.21, 0, 1.65)
        orv1.shipping_additional = 1
        orv1.offer_item_variation_id = blue.id
        oi.variations.append(orv1)
        order.items.append(oi)
        model.base.db.session.add(order)
        model.base.db.session.commit()

        r = self.client.get('/rest/order/?page=1', environ_base=self.environ_base)
        self.assertEqual(401, r.status_code)

        r = self.client.post('/login.html', data={'username':u.username, 'password':"abcd"}, environ_base=self.environ_base)
        self.assertEqual(302, r.status_code)
        r = self.client.get('/rest/order/?page=1', environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, len(r.json['orders']))
        self.assertEqual(1, r.json['count'])
