from pg.model import base

__author__ = 'krzysztof.maslak'


class OrderItem(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    title = base.db.Column(base.db.String(80))
    quantity = base.db.Column(base.db.Integer)
    net = base.db.Column(base.db.Float)
    tax = base.db.Column(base.db.Float)
    shipping = base.db.Column(base.db.Float)
    shipping_additional = base.db.Column(base.db.Float)
    multivariate = base.db.Column(base.db.Integer)
    order_id = base.db.Column(base.db.Integer, base.db.ForeignKey('order.id'))
    offer_item_id = base.db.Column(base.db.Integer)
    variations = base.db.relationship('OrderItemVariation', backref='order_item', lazy='dynamic')

    def __init__(self, order, title='', quantity=0, net=0, tax=0, shipping=0):
        self.order = order
        self.title = title
        self.quantity = quantity
        self.net = net
        self.tax = tax
        self.shipping = shipping

    def as_json(self, exclude=(), extra=()):
        return self._as_json(exclude=['order'])