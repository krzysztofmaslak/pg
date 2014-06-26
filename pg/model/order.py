import datetime
from pg.model.base import JsonSerializable

__author__ = 'xxx'

from ..app import db

class Order(db.Model, JsonSerializable):
    id = db.Column(db.Integer, primary_key=True)
    subscribe = db.Column(db.Boolean)
    payment_method = db.Column(db.String(10))
    currency = db.Column(db.String(3))
    country = db.Column(db.String(3))
    lang = db.Column(db.String(3))
    creation_date = db.Column(db.DateTime)
    confirmation_email = db.Column(db.Boolean)
    payment_status = db.Column(db.String(20))
    delivery_status = db.Column(db.String(20))
    order_number = db.Column(db.String(10))
    billing = db.relationship('Billing', backref='order', lazy='dynamic')
    shipping = db.relationship('Shipping', backref='order', lazy='dynamic')
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    offer = db.relationship('Offer',
        backref=db.backref('orders', lazy='dynamic'))

    items = db.relationship('OrderItem', backref='order', lazy='dynamic')

    def __init__(self):
        self.creation_date=datetime.datetime.now()
        self.confirmation_email = 0
    