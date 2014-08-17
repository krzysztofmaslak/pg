import datetime
from pg.model import base
from pg import util
__author__ = 'krzysztof.maslak'


class Image(base.db.Model, base.JsonSerializable):
    id = base.db.Column(base.db.Integer, primary_key=True)
    creation_date = base.db.Column(base.db.String(35))
    offer_item_id = base.db.Column(base.db.Integer, base.db.ForeignKey('offer_item.id'))

    def __init__(self, offer_item):
        self.offer_item = offer_item
        self.creation_date = util.TimeUtil.unix_time_millis(datetime.datetime.now())

    def as_json(self, exclude=(), extra=()):
        return self._as_json(exclude='offer_item')

