from pg.model.base import JsonSerializable

__author__ = 'krzysztof.maslak'

from ..app import db

class OrderItemVariation(db.Model, JsonSerializable):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    quantity = db.Column(db.Integer)
    net = db.Column(db.Float)
    tax = db.Column(db.Float)
    shipping = db.Column(db.Float)
    shipping_additional = db.Column(db.Float)
    multivariate = db.Column(db.Integer)
    offer_item_variation_id = db.Column(db.Integer)
    order_item_id = db.Column(db.Integer, db.ForeignKey('order_item.id'))

    def __init__(self, order_item, title='', quantity=0, net=0, tax=0, shipping=0):
        self.order_item = order_item
        self.title = title
        self.quantity = quantity
        self.net = net
        self.tax = tax
        self.shipping = shipping



