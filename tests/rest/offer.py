import os
import sys
from flask import json
from werkzeug.security import generate_password_hash
from pg import User, Account, Offer, OfferItem
from .. import *

__author__ = 'xxx'

from flask.ext.testing import TestCase as Base
from factory import ServiceFactory
from pg.app import App, db
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from base import *


class OfferTest(Base):
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

    def test_list(self):
        a = Account()
        u = User('dublin.krzysztof.maslak@gmail.com', generate_password_hash('abcd'))
        a.users.append(u)
        o = Offer(a, status=1)
        a.offers.append(o)
        o.items = [OfferItem(o, 'Item1'), OfferItem(o, 'Item2'), OfferItem(o, 'Item3')]
        db.session.add(a)
        db.session.commit()
        r = self.client.get('/rest/offer/?page=1', environ_base=self.environ_base)
        self.assertEqual(401, r.status_code)

        r = self.client.post('/login.html', data={'username':u.username, 'password':"abcd"}, environ_base=self.environ_base)
        self.assertEqual(302, r.status_code)
        r = self.client.get('/rest/offer/?page=1', environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, len(r.json['offers']))
        self.assertEqual(1, r.json['count'])
        self.assertEqual(r.json['offers'][0]['items'][0], {'status': 0, 'title': 'Item1', 'quantity': 0, 'id': 1, 'tax': 0.0, 'offer_id': 1, 'net': 0.0, 'variations': [], 'shipping': 0.0})

    def test_new_offer(self):
        a = Account()
        u = User('dublin.krzysztof.maslak@gmail.com', generate_password_hash('abcd'))
        a.users.append(u)
        db.session.add(a)
        db.session.commit()
        r = self.client.post('/rest/offer/new', environ_base=self.environ_base)
        self.assertEqual(401, r.status_code)

        r = self.client.post('/login.html', data={'username':u.username, 'password':"abcd"}, environ_base=self.environ_base)
        self.assertEqual(302, r.status_code)
        r = self.client.post('/rest/offer/new', environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(r.json['id'])
        self.assertTrue(r.json['id']>0)


    def test_new_offer_item(self):
        a = Account()
        u = User('dublin.krzysztof.maslak@gmail.com', generate_password_hash('abcd'))
        a.users.append(u)
        o = Offer(a, status=1)
        a.offers.append(o)
        db.session.add(a)
        db.session.commit()
        r = self.client.post('/rest/offer_item/new', data=json.dumps({'offer_id':o.id}), content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        self.assertEqual(401, r.status_code)

        r = self.client.post('/login.html', data={'username':u.username, 'password':"abcd"}, environ_base=self.environ_base)
        self.assertEqual(302, r.status_code)
        r = self.client.post('/rest/offer_item/new', data=json.dumps({'offer_id':o.id}), content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(r.json['id'])
        self.assertTrue(r.json['id']>0)

    def test_new_offer_item_variation(self):
        a = Account()
        u = User('dublin.krzysztof.maslak@gmail.com', generate_password_hash('abcd'))
        a.users.append(u)
        o = Offer(a, status=1)
        oi = OfferItem(o, 'Item1')
        o.items = [oi]
        a.offers.append(o)
        db.session.add(a)
        db.session.commit()
        r = self.client.post('/rest/offer_item_variation/new', data=json.dumps({'offer_item_id':oi.id, 'count':3}), content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        self.assertEqual(401, r.status_code)

        r = self.client.post('/login.html', data={'username':u.username, 'password':"abcd"}, environ_base=self.environ_base)
        self.assertEqual(302, r.status_code)
        r = self.client.post('/rest/offer_item_variation/new', data=json.dumps({'offer_item_id':oi.id, 'count':3}), content_type='application/json', headers=[('Content-Type', 'application/json')], environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)
        self.assertEqual(r.json, [1, 2, 3])

    def test_delete(self):
        a = Account()
        u = User('dublin.krzysztof.maslak@gmail.com', generate_password_hash('abcd'))
        a.users.append(u)
        o = Offer(a, status=0)
        oi = OfferItem(o, 'Item1')
        o.items = [oi]
        a.offers.append(o)
        db.session.add(a)
        db.session.commit()
        r = self.client.delete('/rest/offer/'+str(o.id), environ_base=self.environ_base)
        self.assertEqual(401, r.status_code)

        r = self.client.post('/login.html', data={'username':u.username, 'password':"abcd"}, environ_base=self.environ_base)
        self.assertEqual(302, r.status_code)
        r = self.client.delete('/rest/offer/'+str(o.id), environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)
        offer = Offer.query.filter(Offer.id==o.id).first()
        self.assertIsNone(offer)

    def test_get_by_hash(self):
        a = Account()
        u = User('admin', 'password')
        a.users.append(u)
        o = Offer(a)
        a.offers.append(o)
        o.items = [OfferItem(o, 'Item1'), OfferItem(o, 'Item2'), OfferItem(o, 'Item3')]
        db.session.add(a)
        db.session.commit()
        items = []
        item_id = 0
        for item in o.items:
            if item.title == 'Item2':
                item.title = 'MyItem2'
                item_id = item.id
            items.append(item)
        # modify item 2
        offer_service = self.ioc.new_offer_service()
        o = offer_service.save_offer(a, An(items= items, id= o.id, title='My offer', currency='USD'))

        r = self.client.get('/rest/offer/'+o.hash, environ_base=self.environ_base)
        self.assertEqual(200, r.status_code)

