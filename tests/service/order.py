from pg.exception.quantity_not_available import QuantityNotAvailable

__author__ = 'krzysztof.maslak'
from werkzeug.security import generate_password_hash
from pg.model import User, Order, OrderItem, OrderItemVariation, Offer, OfferItem, OfferItemVariation
import os
import sys
from flask.ext.testing import TestCase as Base
from pg.app import App, db
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from base import *
from nose.tools import *


class OrderServiceTest(Base):

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

    def test_save(self):
        u = User('admin', 'password')
        o = Offer(u)
        oi = OfferItem(o, "My offer item", 4)
        o.items.append(oi)
        o.status = 1
        db.session.add(u)
        db.session.add(o)
        db.session.commit()

        order_service = self.ioc.new_order_service()
        items = [An(id=o.id, quantity=3, variations=[])]
        payment = An(offer_id=o.id, subscribe=True, payment_method='cc', currency='eur', country='fr', lang='eng', session_id='kdkdkdkd', items=items)
        payment.billing = An(first_name='Mickey', last_name='Mouse', address1='Withworth', address2='Drumcondra', country='ie', city='Dublin', postal_code='10', county='Dublin', email='dublin.krzysztof.maslak@gmail.com', same_address=False)
        payment.shipping = An(first_name='Chuck', last_name='Norris', address1='South Central', address2='Rockbrook', country='ie', city='Dublin', postal_code='18', county='Dublin', email='krzysztof.maslak@123.ie', company='Spreadline', phone_number='0842342342')
        o = order_service.save(payment)
        self.assertEquals(payment.offer_id, o.offer_id)
        self.assertEquals(payment.subscribe, o.subscribe)
        self.assertEquals(payment.payment_method, o.payment_method)
        self.assertEquals(payment.currency, o.currency)
        self.assertEquals(payment.country, o.country)
        self.assertEquals(payment.lang, o.lang)

        b = o.billing.first()
        self.assertIsNotNone(b)
        self.assertEquals(payment.billing.first_name, b.first_name)
        self.assertEquals(payment.billing.last_name, b.last_name)
        self.assertEquals(payment.billing.address1, b.address1)
        self.assertEquals(payment.billing.address2, b.address2)
        self.assertEquals(payment.billing.country, b.country)
        self.assertEquals(payment.billing.city, b.city)
        self.assertEquals(payment.billing.postal_code, b.postal_code)
        self.assertEquals(payment.billing.county, b.county)
        self.assertEquals(payment.billing.email, b.email)
        self.assertEquals(payment.billing.same_address, b.same_address)

        s = o.shipping.first()
        self.assertIsNotNone(s)
        self.assertEquals(payment.shipping.first_name, s.first_name)
        self.assertEquals(payment.shipping.last_name, s.last_name)
        self.assertEquals(payment.shipping.address1, s.address1)
        self.assertEquals(payment.shipping.address2, s.address2)
        self.assertEquals(payment.shipping.country, s.country)
        self.assertEquals(payment.shipping.city, s.city)
        self.assertEquals(payment.shipping.postal_code, s.postal_code)
        self.assertEquals(payment.shipping.county, s.county)
        self.assertEquals(payment.shipping.email, s.email)
        self.assertEquals(payment.shipping.company, s.company)
        self.assertEquals(payment.shipping.phone_number, s.phone_number)

    @raises(QuantityNotAvailable)
    def test_save_with_more_then_available(self):
        u = User('admin', 'password')
        o = Offer(u)
        o.status = 1
        oi = OfferItem(o, "My offer item", 2)
        o.items.append(oi)
        db.session.add(u)
        db.session.add(o)
        db.session.commit()

        order_service = self.ioc.new_order_service()
        items = [An(id=oi.id, quantity=3, variations=[])]
        payment = An(offer_id=o.id, subscribe=True, payment_method='cc', currency='eur', country='fr', lang='eng', session_id='kdkdkdkd', items=items)
        payment.billing = An(first_name='Mickey', last_name='Mouse', address1='Withworth', address2='Drumcondra', country='ie', city='Dublin', postal_code='10', county='Dublin', email='dublin.krzysztof.maslak@gmail.com', same_address=True)
        payment.shipping = An(first_name='Chuck', last_name='Norris', address1='South Central', address2='Rockbrook', country='ie', city='Dublin', postal_code='18', county='Dublin', email='krzysztof.maslak@123.ie', company='Spreadline', phone_number='0842342342')
        order_service.save(payment)

    def test_find_by_id(self):
        o = Order()
        db.session.add(o)
        db.session.commit()
        order_service = self.ioc.new_order_service()
        order = order_service.find_by_id(o.id)
        self.assertIsNotNone(order)

    def test_find_order_total(self):
        order = Order()
        oi1 = OrderItem(order, 'Strings', 1, 10.32, 0, 1.65)
        oi1.shipping_additional = 1
        order.items.append(oi1)
        oi2 = OrderItem(order, 'Toy', 3, 32.73, 0, 1.65)
        oi2.shipping_additional = 1
        order.items.append(oi2)
        oi = OrderItem(order, 'Toy', 0, 0, 0, 0)
        oiv1 = OrderItemVariation(oi, "Big", 5, 11.21, 0, 1.65)
        oiv1.shipping_additional = 1
        oi.variations.append(oiv1)
        oiv2 = OrderItemVariation(oi, "Small", 1, 13.79, 0, 1.65)
        oiv2.shipping_additional = 1
        oi.variations.append(oiv2)
        order.items.append(oi)
        total = self.ioc.new_order_service().find_order_total(order)
        self.assertEquals(187.65, total)

    def test_process_paid_order(self):
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

        self.ioc.new_order_service().process_paid_order(order)
        offer = self.ioc.new_offer_service().find_by_id(o.id)
        self.assertIsNotNone(offer)
        self.assertEquals(len(offer.items.all()), 2)
        for oi in offer.items:
            if oi.id==o1.id:
                self.assertEquals(oi.variations.count(), 0)
                self.assertEquals(oi.quantity, 1)
            else:
                self.assertEquals(oi.variations.count(), 2)
                self.assertEquals(oi.variations[0].quantity, 2)