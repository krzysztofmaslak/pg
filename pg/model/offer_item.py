from pg.model.base import JsonSerializable

__author__ = 'krzysztof.maslak'

from ..app import db

class OfferItem(db.Model, JsonSerializable):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    quantity = db.Column(db.Integer)
    net = db.Column(db.Float)
    tax = db.Column(db.Float)
    shipping = db.Column(db.Float)
    shipping_additional = db.Column(db.Float)
    multivariate = db.Column(db.Integer)
    status = db.Column(db.Integer)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))

    variations = db.relationship('OfferItemVariation', backref='offer_item', lazy='dynamic')

    def __init__(self, offer, title, quantity, net, tax, shipping, shipping_additional, status):
        self.offer = offer
        self.title = title
        self.quantity = quantity
        self.net = net
        self.tax = tax
        self.shipping = shipping
        self.shipping_additional = shipping_additional
        self.status = status

    def __init__(self, offer, title='', quantity=0, net=0, tax=0, shipping=0, status=0):
        self.offer = offer
        self.title = title
        self.quantity = quantity
        self.net = net
        self.tax = tax
        self.shipping = shipping
        self.status = status


    def as_json(self, exclude=(), extra=()):
        return self._as_json(exclude=['offer'])


