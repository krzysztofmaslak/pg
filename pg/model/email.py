import datetime
from pg.app import *
from pg.model.base import JsonSerializable

__author__ = 'xxx'


class Email(db.Model, JsonSerializable):
    id = db.Column(db.Integer, primary_key=True)
    from_address = db.Column(db.String(50))
    to_address = db.Column(db.String(50))
    subject = db.Column(db.String(50))
    type = db.Column(db.String(30))
    language = db.Column(db.String(3))
    status = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime)
    processed_date = db.Column(db.DateTime)
    ref_id = db.Column(db.Integer)
    addon1 = db.Column(db.String(30))
    addon2 = db.Column(db.String(30))
    addon3 = db.Column(db.String(30))

    def __init__(self):
        self.creation_date=datetime.datetime.now()

