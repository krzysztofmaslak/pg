import datetime
from pg.model import base

__author__ = 'xxx'

class Order(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    subscribe = base.db.Column(base.db.Boolean)
    payment_method = base.db.Column(base.db.String(10))
    currency = base.db.Column(base.db.String(3))
    country = base.db.Column(base.db.String(3))
    lang = base.db.Column(base.db.String(3))
    creation_date = base.db.Column(base.db.DateTime)
    confirmation_email = base.db.Column(base.db.Boolean)
    payment_status = base.db.Column(base.db.String(20))
    delivery_status = base.db.Column(base.db.String(20))
    order_number = base.db.Column(base.db.String(10))
    billing = base.db.relationship('Billing', backref='order', lazy='dynamic')
    shipping = base.db.relationship('Shipping', backref='order', lazy='dynamic')
    offer_id = base.db.Column(base.db.Integer, base.db.ForeignKey('offer.id'))
    offer = base.db.relationship('Offer',
        backref=base.db.backref('orders', lazy='dynamic'))

    items = base.db.relationship('OrderItem', backref='order', lazy='dynamic')

    def __init__(self):
        self.creation_date=datetime.datetime.now()
        self.confirmation_email = 0
    