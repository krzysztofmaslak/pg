import calendar
import datetime
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from pg import util

__author__ = 'root'
primitive = (int, str, float, bool)

db = SQLAlchemy()

def json_date(datetime):
    return ''

class JsonSerializable:
    def _as_json(self, longdate=False, exclude=(), extra=()):
        data = {}
        keys = self._sa_instance_state.attrs.items()
        for k, field in  keys:
            if k in exclude: continue
            value = self._serialize(field.value, longdate)
            if value is not None:
                data[k] = value
        return data

    def as_json(self, longdate=False, exclude=(), extra=()):
        return self._as_json(longdate, exclude, extra)

    @classmethod
    def _serialize(cls, value, longdate=False):
        if longdate==False and isinstance(value, datetime.datetime):
            if value.utcoffset() is not None:
                value = value - value.utcoffset()
            return value.strftime('%Y-%m-%dT%H:%M:%S')
        elif longdate==True and isinstance(value, datetime.datetime):
            if value.utcoffset() is not None:
                value = value - value.utcoffset()
            return util.TimeUtil.unix_time_millis(value)
        elif type(value) in (datetime, date):
            ret = value.isoformat()
        elif isinstance(value, primitive):
            ret = value
        elif hasattr(value, '__iter__'):
            ret = []
            for v in value:
                if JsonSerializable in v.__class__.__bases__:
                    serialized = v.as_json()
                    ret.append(serialized)
        elif JsonSerializable in value.__class__.__bases__:
            ret = value.as_json()
        else:
            ret = value

        return ret
