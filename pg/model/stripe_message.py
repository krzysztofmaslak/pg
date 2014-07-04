__author__ = 'krzysztof.maslak'
import datetime

from pg.model import base

class StripeMessage(base.db.Model):
    id = base.db.Column(base.db.Integer, primary_key=True)
    tid = base.db.Column(base.db.String(50), unique=True)
    message = base.db.Column(base.db.Text)
    order_id = base.db.Column(base.db.Integer)
    creation_date = base.db.Column(base.db.DateTime)

    def __init__(self, tid, message, order_id, creation_date=datetime.datetime.now()):
        self.tid = tid
        self.message = message
        self.order_id = order_id
        self.creation_date = creation_date

    def __repr__(self):
        return '<StripeMessage %r>' % self.tid

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.tid==other.tid and self.id==other.id