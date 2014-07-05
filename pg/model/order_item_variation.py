from pg.model import base

__author__ = 'krzysztof.maslak'


class OrderItemVariation(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    title = base.db.Column(base.db.String(80))
    quantity = base.db.Column(base.db.Integer)
    net = base.db.Column(base.db.Float)
    tax = base.db.Column(base.db.Float)
    shipping = base.db.Column(base.db.Float)
    shipping_additional = base.db.Column(base.db.Float)
    multivariate = base.db.Column(base.db.Integer)
    offer_item_variation_id = base.db.Column(base.db.Integer)
    order_item_id = base.db.Column(base.db.Integer, base.db.ForeignKey('order_item.id'))

    def __init__(self, order_item, title='', quantity=0, net=0, tax=0, shipping=0):
        self.order_item = order_item
        self.title = title
        self.quantity = quantity
        self.net = net
        self.tax = tax
        self.shipping = shipping

    def as_json(self, exclude=(), extra=()):
        return self._as_json(exclude=['order_item'])

