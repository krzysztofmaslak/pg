from pg.model import base

__author__ = 'krzysztof.maslak'


class OfferItemVariation(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    title_en = base.db.Column(base.db.String(80))
    title_fr = base.db.Column(base.db.String(80))
    quantity = base.db.Column(base.db.Integer)
    net = base.db.Column(base.db.Float)
    tax = base.db.Column(base.db.Float)
    img = base.db.Column(base.db.String(40))
    shipping = base.db.Column(base.db.Float)
    shipping_additional = base.db.Column(base.db.Float)
    status = base.db.Column(base.db.Integer)
    offer_item_id = base.db.Column(base.db.Integer, base.db.ForeignKey('offer_item.id'))

    def __init__(self, offer_item, title_en='', title_fr='', quantity=0, net=0, tax=0, shipping=0, status=0):
        self.offer_item = offer_item
        self.title_en = title_en
        self.title_fr = title_fr
        self.quantity = quantity
        self.net = net
        self.tax = tax
        self.shipping = shipping
        self.status = status

    def as_json(self, exclude=(), extra=()):
        return self._as_json(exclude='offer_item')

