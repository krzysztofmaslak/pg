from pg.model.base import JsonSerializable

__author__ = 'krzysztof.maslak'

from ..app import db

class OfferItemVariation(db.Model, JsonSerializable):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    quantity = db.Column(db.Integer)
    net = db.Column(db.Float)
    tax = db.Column(db.Float)
    shipping = db.Column(db.Float)
    shipping_additional = db.Column(db.Float)
    status = db.Column(db.Integer)
    offer_item_id = db.Column(db.Integer, db.ForeignKey('offer_item.id'))

    def __init__(self, offer_item, title, quantity, net, tax, shipping, shipping_additional, status):
        self.offer_item = offer_item
        self.title = title
        self.quantity = quantity
        self.net = net
        self.tax = tax
        self.shipping = shipping
        self.shipping_additional = shipping_additional
        self.status = status

    def __init__(self, offer_item, title='', quantity=0, net=0, tax=0, shipping=0, status=0):
        self.offer_item = offer_item
        self.title = title
        self.quantity = quantity
        self.net = net
        self.tax = tax
        self.shipping = shipping
        self.status = status

    def as_json(self, exclude=(), extra=()):
        return self._as_json(exclude='offer_item')

