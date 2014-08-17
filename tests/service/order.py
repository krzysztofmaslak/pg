import mock

__author__ = 'krzysztof.maslak'
from flask.ext.testing import TestCase as Base
from nose.tools import *
from pg.exception import quantity_not_available
from pg import app as application, model
from tests import base

class OrderServiceTest(Base):

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

    def test_save(self):
        a = model.Account()
        u = model.User('admin', 'password')
        a.users.append(u)
        o = model.Offer(a)
        oi = model.OfferItem(o, "My offer item", '', 4, 3.99, 2.30, 1.65, 1)
        oi.shipping_additional = 1.2
        o.items.append(oi)
        o.status = 1
        model.base.db.session.add(a)
        model.base.db.session.add(o)
        model.base.db.session.commit()

        order_service = self.ioc.new_order_service()
        items = [base.An(id=o.id, quantity=3, variations=[])]
        payment = base.An(offer_id=o.id, subscribe=True, payment_method='cc', currency='eur', country='fr', lang='en', session_id='kdkdkdkd', items=items)
        payment.billing = base.An(first_name='Mickey', last_name='Mouse', address1='Withworth', address2='Drumcondra', country='ie', city='Dublin', postal_code='10', county='Dublin', email='dublin.krzysztof.maslak@gmail.com', same_address=False)
        payment.shipping = base.An(first_name='Chuck', last_name='Norris', address1='South Central', address2='Rockbrook', country='ie', city='Dublin', postal_code='18', county='Dublin', email='krzysztof.maslak@123.ie', company='Spreadline', phone_number='0842342342')
        o = order_service.save(payment)
        self.assertEqual(o.account_id, a.id)
        self.assertEqual(22.92, o.total)
        self.assertEqual(payment.offer_id, o.offer_id)
        self.assertEqual(payment.subscribe, o.subscribe)
        self.assertEqual(payment.payment_method, o.payment_method)
        self.assertEqual(payment.currency, o.currency)
        self.assertEqual(payment.country, o.country)
        self.assertEqual(payment.lang, o.lang)

        b = o.billing.first()
        self.assertIsNotNone(b)
        self.assertEqual(payment.billing.first_name, b.first_name)
        self.assertEqual(payment.billing.last_name, b.last_name)
        self.assertEqual(payment.billing.address1, b.address1)
        self.assertEqual(payment.billing.address2, b.address2)
        self.assertEqual(payment.billing.country, b.country)
        self.assertEqual(payment.billing.city, b.city)
        self.assertEqual(payment.billing.postal_code, b.postal_code)
        self.assertEqual(payment.billing.county, b.county)
        self.assertEqual(payment.billing.email, b.email)
        self.assertEqual(payment.billing.same_address, b.same_address)

        s = o.shipping.first()
        self.assertIsNotNone(s)
        self.assertEqual(payment.shipping.first_name, s.first_name)
        self.assertEqual(payment.shipping.last_name, s.last_name)
        self.assertEqual(payment.shipping.address1, s.address1)
        self.assertEqual(payment.shipping.address2, s.address2)
        self.assertEqual(payment.shipping.country, s.country)
        self.assertEqual(payment.shipping.city, s.city)
        self.assertEqual(payment.shipping.postal_code, s.postal_code)
        self.assertEqual(payment.shipping.county, s.county)
        self.assertEqual(payment.shipping.email, s.email)
        self.assertEqual(payment.shipping.company, s.company)
        self.assertEqual(payment.shipping.phone_number, s.phone_number)

    @raises(quantity_not_available.QuantityNotAvailable)
    def test_save_with_more_then_available(self):
        a = model.Account()
        u = model.User('admin', 'password')
        a.users.append(u)
        o = model.Offer(a)
        o.status = 1
        oi = model.OfferItem(o, "My offer item", '', 2, 3.20, 1.54, 1.65, 1)
        o.items.append(oi)
        model.base.db.session.add(u)
        model.base.db.session.add(o)
        model.base.db.session.commit()

        order_service = self.ioc.new_order_service()
        items = [base.An(id=oi.id, quantity=3, variations=[])]
        payment = base.An(offer_id=o.id, subscribe=True, payment_method='cc', currency='eur', country='fr', lang='en', session_id='kdkdkdkd', items=items)
        payment.billing = base.An(first_name='Mickey', last_name='Mouse', address1='Withworth', address2='Drumcondra', country='ie', city='Dublin', postal_code='10', county='Dublin', email='dublin.krzysztof.maslak@gmail.com', same_address=True)
        payment.shipping = base.An(first_name='Chuck', last_name='Norris', address1='South Central', address2='Rockbrook', country='ie', city='Dublin', postal_code='18', county='Dublin', email='krzysztof.maslak@123.ie', company='Spreadline', phone_number='0842342342')
        order_service.save(payment)

    def test_find_by_id(self):
        o = model.Order()
        model.base.db.session.add(o)
        model.base.db.session.commit()
        order_service = self.ioc.new_order_service()
        order = order_service.find_by_id(o.id)
        self.assertIsNotNone(order)

    def test_find_order_total(self):
        order = model.Order()
        oi1 = model.OrderItem(order, 'Strings', '', 1, 10.32, 0, 1.65)
        oi1.shipping_additional = 1
        order.items.append(oi1)
        oi2 = model.OrderItem(order, 'Toy', '', 3, 32.73, 0, 1.65)
        oi2.shipping_additional = 1
        order.items.append(oi2)
        oi = model.OrderItem(order, 'Toy', '', 0, 0, 0, 0)
        oiv1 = model.OrderItemVariation(oi, "Big", '', 5, 11.21, 0, 1.65)
        oiv1.shipping_additional = 1
        oi.variations.append(oiv1)
        oiv2 = model.OrderItemVariation(oi, "Small", '', 1, 13.79, 0, 1.65)
        oiv2.shipping_additional = 1
        oi.variations.append(oiv2)
        order.items.append(oi)
        total = self.ioc.new_order_service().find_order_total(order)
        self.assertEqual(190.95, total)

    def test_process_paid_order(self):
        a = model.Account()
        u = model.User('admin', 'password')
        a.users.append(u)
        o = model.Offer(a)
        o.status = 1
        o1 = model.OfferItem(o, "My offer item", '', 2)
        o2 = model.OfferItem(o, "My offer item2")
        blue = model.OfferItemVariation(o2, "Blue", '', 3)
        red = model.OfferItemVariation(o2, "Red", '', 1)
        o2.variations = [blue, red]
        o.items.append(o1)
        o.items.append(o2)
        model.base.db.session.add(u)
        model.base.db.session.add(o)
        model.base.db.session.commit()

        order = model.Order()
        order.offer_id = o.id
        or1 = model.OrderItem(order, 'Strings', '', 1, 10.32, 0, 1.65)
        or1.shipping_additional = 1
        or1.offer_item_id = o1.id
        order.items.append(or1)
        oi = model.OrderItem(order, 'Toy', '', 0, 0, 0, 0)
        oi.offer_item_id = o2.id
        orv1 = model.OrderItemVariation(oi, "Big", '', 1, 11.21, 0, 1.65)
        orv1.shipping_additional = 1
        orv1.offer_item_variation_id = blue.id
        oi.variations.append(orv1)
        order.items.append(oi)
        model.base.db.session.add(order)
        model.base.db.session.commit()

        self.ioc.new_order_service().process_paid_order(order)
        offer = self.ioc.new_offer_service().find_by_id(o.id)
        self.assertIsNotNone(offer)
        self.assertEqual(len(offer.items.all()), 2)
        for oi in offer.items:
            if oi.id==o1.id:
                self.assertEqual(oi.variations.count(), 0)
                self.assertEqual(oi.quantity, 1)
            else:
                self.assertEqual(oi.variations.count(), 2)
                self.assertEqual(oi.variations[0].quantity, 2)

    def test_find_by_page(self):
        a = model.Account()
        u = model.User('admin', 'password')
        a.users.append(u)
        o = model.Offer(a)
        o.status = 1
        o1 = model.OfferItem(o, "My offer item", '', 2)
        o2 = model.OfferItem(o, "My offer item2")
        blue = model.OfferItemVariation(o2, "Blue", '', 3)
        red = model.OfferItemVariation(o2, "Red", '', 1)
        o2.variations = [blue, red]
        o.items.append(o1)
        o.items.append(o2)
        model.base.db.session.add(a)
        model.base.db.session.add(o)
        model.base.db.session.commit()

        for i in range(33):
            order = model.Order()
            order.account_id = a.id
            order.payment_status = 'Completed'
            order.offer_id = o.id
            or1 = model.OrderItem(order, 'Strings', '', 1, 10.32, 0, 1.65)
            or1.shipping_additional = 1
            or1.offer_item_id = o1.id
            order.items.append(or1)
            oi = model.OrderItem(order, 'Toy', '', 0, 0, 0, 0)
            oi.offer_item_id = o2.id
            orv1 = model.OrderItemVariation(oi, "Big", '', 1, 11.21, 0, 1.65)
            orv1.shipping_additional = 1
            orv1.offer_item_variation_id = blue.id
            oi.variations.append(orv1)
            order.items.append(oi)
            model.base.db.session.add(order)
            model.base.db.session.commit()

        order_service = self.ioc.new_order_service()
        items = order_service.find_by_page(a, 1)
        self.assertIsNotNone(items)
        self.assertEqual(10, len(items))
        items = order_service.find_by_page(a, 2)
        self.assertIsNotNone(items)
        self.assertEqual(10, len(items))
        items = order_service.find_by_page(a, 3)
        self.assertIsNotNone(items)
        self.assertEqual(10, len(items))
        items = order_service.find_by_page(a, 4)
        self.assertIsNotNone(items)
        self.assertEqual(3, len(items))

    def test_find_by_page(self):
        a = model.Account()
        u = model.User('admin', 'password')
        a.users.append(u)
        o = model.Offer(a)
        o.status = 1
        o1 = model.OfferItem(o, "My offer item", '', 2)
        o2 = model.OfferItem(o, "My offer item2")
        blue = model.OfferItemVariation(o2, "Blue", '', 3)
        red = model.OfferItemVariation(o2, "Red", '', 1)
        o2.variations = [blue, red]
        o.items.append(o1)
        o.items.append(o2)
        model.base.db.session.add(a)
        model.base.db.session.add(o)
        model.base.db.session.commit()

        order = model.Order()
        order.account_id = a.id
        order.offer_id = o.id
        or1 = model.OrderItem(order, 'Strings', '', 1, 10.32, 0, 1.65)
        or1.shipping_additional = 1
        or1.offer_item_id = o1.id
        order.items.append(or1)
        oi = model.OrderItem(order, 'Toy', '', 0, 0, 0, 0)
        oi.offer_item_id = o2.id
        orv1 = model.OrderItemVariation(oi, "Big", '', 1, 11.21, 0, 1.65)
        orv1.shipping_additional = 1
        orv1.offer_item_variation_id = blue.id
        oi.variations.append(orv1)
        order.items.append(oi)
        model.base.db.session.add(order)
        for i in range(33):
            order = model.Order()
            order.account_id = a.id
            order.payment_status = 'Completed'
            order.offer_id = o.id
            or1 = model.OrderItem(order, 'Strings', '', 1, 10.32, 0, 1.65)
            or1.shipping_additional = 1
            or1.offer_item_id = o1.id
            order.items.append(or1)
            oi = model.OrderItem(order, 'Toy', '', 0, 0, 0, 0)
            oi.offer_item_id = o2.id
            orv1 = model.OrderItemVariation(oi, "Big", '', 1, 11.21, 0, 1.65)
            orv1.shipping_additional = 1
            orv1.offer_item_variation_id = blue.id
            oi.variations.append(orv1)
            order.items.append(oi)
            model.base.db.session.add(order)
            model.base.db.session.commit()

        order_service = self.ioc.new_order_service()
        self.assertEqual(33, order_service.find_paid_orders_count(a))

    def test_get_order_total_reduced_by_fee(self):
        order = model.Order()
        oi1 = model.OrderItem(order, 'Strings', '', 1, 10.32, 0, 1.65)
        oi1.shipping_additional = 1
        order.items.append(oi1)
        oi2 = model.OrderItem(order, 'Toy', '', 3, 32.73, 0, 1.65)
        oi2.shipping_additional = 1
        order.items.append(oi2)
        oi = model.OrderItem(order, 'Toy', '', 0, 0, 0, 0)
        oiv1 = model.OrderItemVariation(oi, "Big", '', 5, 11.21, 0, 1.65)
        oiv1.shipping_additional = 1
        oi.variations.append(oiv1)
        oiv2 = model.OrderItemVariation(oi, "Small", '', 1, 13.79, 0, 1.65)
        oiv2.shipping_additional = 1
        oi.variations.append(oiv2)
        order.items.append(oi)
        total = self.ioc.new_order_service().find_order_total(order)
        self.assertEqual(190.95, total)
        order.total = total
        order_net = self.ioc.new_order_service().get_order_total_reduced_by_fee(order)
        self.assertEqual(181.06, round(order_net, 2))