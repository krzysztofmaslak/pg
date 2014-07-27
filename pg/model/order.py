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
    refund_payment = base.db.Column(base.db.INT)
    total = base.db.Column(base.db.Float)
    fee = base.db.Column(base.db.Float)
    billing = base.db.relationship('Billing', backref='order', lazy='dynamic')
    shipping = base.db.relationship('Shipping', backref='order', lazy='dynamic')
    offer_id = base.db.Column(base.db.Integer, base.db.ForeignKey('offer.id'))
    account_id = base.db.Column(base.db.Integer, base.db.ForeignKey('account.id'))
    offer = base.db.relationship('Offer',
        backref=base.db.backref('orders', lazy='dynamic'))

    items = base.db.relationship('OrderItem', backref='order', lazy='dynamic')

    def __init__(self):
        self.creation_date=datetime.datetime.now()
        self.confirmation_email = 0
        self.refund_payment = 0

    def __eq__(self, other):
        print("Calling order eq %s"%(isinstance(other, self.__class__) and self.id==other.id))
        return isinstance(other, self.__class__) and self.id==other.id

    def as_json(self, exclude=(), extra=()):
        return self._as_json(exclude=['offer'])
