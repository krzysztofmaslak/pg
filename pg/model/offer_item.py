from pg.model import base

__author__ = 'krzysztof.maslak'

class OfferItem(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    title = base.db.Column(base.db.String(80))
    condition = base.db.Column(base.db.String(4))
    quantity = base.db.Column(base.db.Integer)
    net = base.db.Column(base.db.Float)
    tax = base.db.Column(base.db.Float)
    shipping = base.db.Column(base.db.Float)
    shipping_additional = base.db.Column(base.db.Float)
    multivariate = base.db.Column(base.db.Integer)
    status = base.db.Column(base.db.Integer)
    offer_id = base.db.Column(base.db.Integer, base.db.ForeignKey('offer.id'))

    variations = base.db.relationship('OfferItemVariation', backref='offer_item', lazy='dynamic')

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


