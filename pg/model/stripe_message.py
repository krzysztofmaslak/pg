__author__ = 'krzysztof.maslak'
import datetime

from pg.app import db

class StripeMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tid = db.Column(db.String(50), unique=True)
    message = db.Column(db.Text)
    order_id = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime)

    def __init__(self, tid, message, order_id, creation_date=datetime.datetime.now()):
        self.tid = tid
        self.message = message
        self.order_id = order_id
        self.creation_date = creation_date

    def __repr__(self):
        return '<StripeMessage %r>' % self.tid
