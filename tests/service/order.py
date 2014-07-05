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
        oi = model.OfferItem(o, "My offer item", 4, 3.99, 2.30, 1.65, 1)
        oi.shipping_additional = 1.2
        o.items.append(oi)
        o.status = 1
        model.base.db.session.add(a)
        model.base.db.session.add(o)
        model.base.db.session.commit()

        order_service = self.ioc.new_order_service(mock.MagicMock)
        items = [base.An(id=o.id, quantity=3, variations=[])]
        payment = base.An(offer_id=o.id, subscribe=True, payment_method='cc', currency='eur', country='fr', lang='eng', session_id='kdkdkdkd', items=items)
        payment.billing = base.An(first_name='Mickey', last_name='Mouse', address1='Withworth', address2='Drumcondra', country='ie', city='Dublin', postal_code='10', county='Dublin', email='dublin.krzysztof.maslak@gmail.com', same_address=False)
        payment.shipping = base.An(first_name='Chuck', last_name='Norris', address1='South Central', address2='Rockbrook', country='ie', city='Dublin', postal_code='18', county='Dublin', email='krzysztof.maslak@123.ie', company='Spreadline', phone_number='0842342342')
        o = order_service.save(payment)
        self.assertEquals(o.account_id, a.id)
        self.assertEquals(21.27, o.total)
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

    @raises(quantity_not_available.QuantityNotAvailable)
    def test_save_with_more_then_available(self):
        a = model.Account()
        u = model.User('admin', 'password')
        a.users.append(u)
        o = model.Offer(a)
        o.status = 1
        oi = model.OfferItem(o, "My offer item", 2, 3.20, 1.54, 1.65, 1)
        o.items.append(oi)
        model.base.db.session.add(u)
        model.base.db.session.add(o)
        model.base.db.session.commit()

        order_service = self.ioc.new_order_service(mock.MagicMock)
        items = [base.An(id=oi.id, quantity=3, variations=[])]
        payment = base.An(offer_id=o.id, subscribe=True, payment_method='cc', currency='eur', country='fr', lang='eng', session_id='kdkdkdkd', items=items)
        payment.billing = base.An(first_name='Mickey', last_name='Mouse', address1='Withworth', address2='Drumcondra', country='ie', city='Dublin', postal_code='10', county='Dublin', email='dublin.krzysztof.maslak@gmail.com', same_address=True)
        payment.shipping = base.An(first_name='Chuck', last_name='Norris', address1='South Central', address2='Rockbrook', country='ie', city='Dublin', postal_code='18', county='Dublin', email='krzysztof.maslak@123.ie', company='Spreadline', phone_number='0842342342')
        order_service.save(payment)

    def test_find_by_id(self):
        o = model.Order()
        model.base.db.session.add(o)
        model.base.db.session.commit()
        order_service = self.ioc.new_order_service(mock.MagicMock)
        order = order_service.find_by_id(o.id)
        self.assertIsNotNone(order)

    def test_find_order_total(self):
        order = model.Order()
        oi1 = model.OrderItem(order, 'Strings', 1, 10.32, 0, 1.65)
        oi1.shipping_additional = 1
        order.items.append(oi1)
        oi2 = model.OrderItem(order, 'Toy', 3, 32.73, 0, 1.65)
        oi2.shipping_additional = 1
        order.items.append(oi2)
        oi = model.OrderItem(order, 'Toy', 0, 0, 0, 0)
        oiv1 = model.OrderItemVariation(oi, "Big", 5, 11.21, 0, 1.65)
        oiv1.shipping_additional = 1
        oi.variations.append(oiv1)
        oiv2 = model.OrderItemVariation(oi, "Small", 1, 13.79, 0, 1.65)
        oiv2.shipping_additional = 1
        oi.variations.append(oiv2)
        order.items.append(oi)
        total = self.ioc.new_order_service(mock.MagicMock).find_order_total(order)
        self.assertEquals(187.65, total)

    def test_process_paid_order(self):
        a = model.Account()
        u = model.User('admin', 'password')
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
        model.base.db.session.add(u)
        model.base.db.session.add(o)
        model.base.db.session.commit()

        order = model.Order()
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

        self.ioc.new_order_service(mock.MagicMock).process_paid_order(order)
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

    def test_find_by_page(self):
        a = model.Account()
        u = model.User('admin', 'password')
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

        for i in range(33):
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

        order_service = self.ioc.new_order_service(mock.MagicMock())
        items = order_service.find_by_page(a, 1)
        self.assertIsNotNone(items)
        self.assertEquals(10, len(items))
        items = order_service.find_by_page(a, 2)
        self.assertIsNotNone(items)
        self.assertEquals(10, len(items))
        items = order_service.find_by_page(a, 3)
        self.assertIsNotNone(items)
        self.assertEquals(10, len(items))
        items = order_service.find_by_page(a, 4)
        self.assertIsNotNone(items)
        self.assertEquals(3, len(items))

    def test_find_by_page(self):
        a = model.Account()
        u = model.User('admin', 'password')
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
        for i in range(33):
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

        order_service = self.ioc.new_order_service(mock.MagicMock())
        self.assertEquals(33, order_service.find_paid_orders_count(a))