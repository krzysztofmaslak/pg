import datetime
from pg.model import base

__author__ = 'xxx'


class Email(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    from_address = base.db.Column(base.db.String(50))
    to_address = base.db.Column(base.db.String(50))
    subject = base.db.Column(base.db.String(50))
    type = base.db.Column(base.db.String(30))
    language = base.db.Column(base.db.String(3))
    status = base.db.Column(base.db.Integer)
    creation_date = base.db.Column(base.db.DateTime)
    processed_date = base.db.Column(base.db.DateTime)
    ref_id = base.db.Column(base.db.Integer)
    addon1 = base.db.Column(base.db.String(30))
    addon2 = base.db.Column(base.db.String(30))
    addon3 = base.db.Column(base.db.String(30))

    def __init__(self):
        self.creation_date=datetime.datetime.now()

