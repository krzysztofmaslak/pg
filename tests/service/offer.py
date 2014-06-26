__author__ = 'xxx'
from flask.ext.testing import TestCase
from pg import model, app as application
from tests import base


class OfferServiceTest(TestCase):

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

    def test_delete(self):
        a2 = model.Account()
        a = model.Account()
        u = model.User('admin', 'password')
        a.users.append(u)
        model.base.db.session.add(a)
        model.base.db.session.add(a2)
        model.base.db.session.commit()
        offer_service = self.ioc.new_offer_service()
        o = offer_service.new_offer(a)
        self.assertIsNotNone(o)
        self.assertIsNotNone(o.id)
        try:
            offer_service.delete_offer(a2, o.id)
        except RuntimeError:
            pass
        o = model.Offer.query.filter(model.Offer.id == o.id, model.Offer.account_id == a.id).first()
        self.assertIsNotNone(o)
        offer_service.delete_offer(a, o.id)
        o = model.Offer.query.filter(model.Offer.id == o.id, model.Offer.account_id == a.id).first()
        self.assertIsNone(o)

    def test_save(self):
        a = model.Account()
        u = model.User('admin', 'password')
        a.users.append(u)
        o = model.Offer(a)
        a.offers.append(o)
        o.items = [model.OfferItem(o, 'Item1'), model.OfferItem(o, 'Item2'), model.OfferItem(o, 'Item3')]
        model.base.db.session.add(a)
        model.base.db.session.commit()
        items = []
        item_id = 0
        for item in o.items:
            if item.title == 'Item2':
                item.title = 'MyItem2'
                item_id = item.id
            items.append(item)
        # modify item 2
        offer_service = self.ioc.new_offer_service()
        offer_service.save_offer(a, base.An(items= items, id= o.id, title='My offer', currency='USD'))
        o = model.Offer.query.filter(model.Offer.id == o.id).first()
        for item in o.items:
            if item.id == item_id:
                self.assertEqual(item.title, 'MyItem2')
        # remove item 3
        offer_service.save_offer(a, base.An(items= items[0:2], id= o.id, title='My offer', currency='USD'))
        o = model.Offer.query.filter(model.Offer.id == o.id).first()
        self.assertEquals(2, len(o.items.all()))
        # add variations to item 1
        o.items[0].variations = [model.OfferItemVariation(o.items[0], 'Blue'), model.OfferItemVariation(o.items[0], 'Red')]
        model.base.db.session.commit()
        variations = []
        for variation in o.items[0].variations:
            if variation.title == 'Red':
                variation.title = 'Red2'
            variations.append(variation)
        items = []
        for item in o.items:
            items.append(item)
        items[0].variations = variations
        offer_service.save_offer(a, base.An(items= items, id= o.id, title='My offer', currency='USD'))
        o = model.Offer.query.filter(model.Offer.id == o.id).first()
        self.assertEquals('Red2', o.items[0].variations[1].title)

    def test_save_with_variations(self):
        a = model.Account()
        u = model.User('admin', 'password')
        a.users.append(u)
        o = model.Offer(a)
        a.offers.append(o)
        oi = model.OfferItem(o, 'Item1')
        oiv = model.OfferItemVariation(oi, 'Red size 45')
        oi.variations.append(oiv)
        o.items = [oi, model.OfferItem(o, 'Item2'), model.OfferItem(o, 'Item3')]
        model.base.db.session.add(a)
        model.base.db.session.commit()

        items = []
        item_id = 0
        for item in o.items:
            if item.title == 'Item1':
                item.title = 'MyItem2'
                item_id = item.id
                oiv.quantity = 1
                oiv.net = 3.99
                oiv.shipping = 1.65
                oiv.tax = 0
            items.append(item)
        # modify item 2
        offer_service = self.ioc.new_offer_service()
        offer_service.save_offer(a, base.An(items= items, id= o.id, title='My offer', currency='USD'))
        o = model.Offer.query.filter(model.Offer.id == o.id).first()
        for item in o.items:
            if item.id == item_id:
                self.assertEqual(item.title, 'MyItem2')
                self.assertEqual(item.variations[0].net, 3.99)

    def test_new_offer_item_variation(self):
        a = model.Account()
        u = model.User('admin', 'password')
        a.users.append(u)
        o = model.Offer(a)
        o.items = [model.OfferItem(o, 'Item1'), model.OfferItem(o, 'Item2'), model.OfferItem(o, 'Item3')]
        a.offers.append(o)
        model.base.db.session.add(a)
        model.base.db.session.commit()
        offer_service = self.ioc.new_offer_service()
        oiv = offer_service.new_offer_item_variation(a, o.items[0].id)
        self.assertIsNotNone(oiv)
        self.assertIsNotNone(oiv.id)

    def test_new_offer_item(self):
        a = model.Account()
        u = model.User('admin', 'password')
        a.users.append(u)
        o = model.Offer(a)
        a.offers.append(o)
        model.base.db.session.add(a)
        model.base.db.session.commit()
        offer_service = self.ioc.new_offer_service()
        oi = offer_service.new_offer_item(a, o.id)
        self.assertIsNotNone(oi)
        self.assertIsNotNone(oi.id)

    def test_new_offer(self):
        a = model.Account()
        u = model.User('admin', 'password')
        a.users.append(u)
        model.base.db.session.add(a)
        model.base.db.session.commit()
        offer_service = self.ioc.new_offer_service()
        o = offer_service.new_offer(a)
        self.assertIsNotNone(o)

    def test_find_offers_count(self):
        a = model.Account()
        u = model.User('admin', 'password')
        a.users.append(u)
        model.base.db.session.add(a)
        model.base.db.session.commit()
        o = model.Offer(a)
        o.status = 1
        o2 = model.Offer(a)
        o2.status = 1
        model.base.db.session.add(o)
        model.base.db.session.add(o2)
        model.base.db.session.commit()
        offer_service = self.ioc.new_offer_service()
        c = offer_service.find_offers_count(a)
        self.assertIsNotNone(c)
        self.assertEquals(2, c)

    def test_find_by_page(self):
        a = model.Account()
        u = model.User('admin', 'password')
        a.users.append(u)
        for i in range(33):
            o = model.Offer(a)
            o.status = 1
            a.offers.append(o)
        model.base.db.session.add(a)
        model.base.db.session.commit()
        offer_service = self.ioc.new_offer_service()
        items = offer_service.find_by_page(a, 1)
        self.assertIsNotNone(items)
        self.assertEquals(10, len(items))
        items = offer_service.find_by_page(a, 2)
        self.assertIsNotNone(items)
        self.assertEquals(10, len(items))
        items = offer_service.find_by_page(a, 3)
        self.assertIsNotNone(items)
        self.assertEquals(10, len(items))
        items = offer_service.find_by_page(a, 4)
        self.assertIsNotNone(items)
        self.assertEquals(3, len(items))

    def test_find_by_id(self):
        a = model.Account()
        u = model.User('admin', 'password')
        a.users.append(u)
        o = model.Offer(a)
        o.status = 1
        a.offers.append(o)
        model.base.db.session.add(a)
        model.base.db.session.commit()
        offer_service = self.ioc.new_offer_service()
        offer = offer_service.find_by_id(o.id)
        self.assertIsNotNone(offer)

    def test_find_by_hash(self):
        a = model.Account()
        u = model.User('admin', 'password')
        a.users.append(u)
        o = model.Offer(a)
        o.hash = 'abc123'
        o.status = 1
        a.offers.append(o)
        model.base.db.session.add(a)
        model.base.db.session.commit()
        offer_service = self.ioc.new_offer_service()
        o2 = offer_service.find_by_hash('abc123')
        self.assertIsNotNone(o2)
        self.assertEquals(o2.id, o.id)