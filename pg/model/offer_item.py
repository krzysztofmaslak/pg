from pg.model import base

__author__ = 'krzysztof.maslak'

class OfferItem(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    title_en = base.db.Column(base.db.String(80))
    title_fr = base.db.Column(base.db.String(80))
    description_en = base.db.Column(base.db.Text)
    description_fr = base.db.Column(base.db.Text)
    condition = base.db.Column(base.db.String(4))
    quantity = base.db.Column(base.db.Integer)
    img = base.db.Column(base.db.String(40))
    net = base.db.Column(base.db.Float)
    tax = base.db.Column(base.db.Float)
    shipping = base.db.Column(base.db.Float)
    shipping_additional = base.db.Column(base.db.Float)
    multivariate = base.db.Column(base.db.Integer)
    status = base.db.Column(base.db.Integer)
    offer_id = base.db.Column(base.db.Integer, base.db.ForeignKey('offer.id'))

    variations = base.db.relationship('OfferItemVariation', backref='offer_item', lazy='dynamic')

    def __init__(self, offer, title_en='', title_fr='', quantity=0, net=0, tax=0, shipping=0, status=0):
        self.offer = offer
        self.title_en = title_en
        self.title_fr = title_fr
        self.quantity = quantity
        self.net = net
        self.tax = tax
        self.shipping = shipping
        self.status = status


    def as_json(self, exclude=(), extra=()):
        return self._as_json(exclude=['offer'])


