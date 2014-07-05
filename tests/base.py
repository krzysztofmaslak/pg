import datetime
from factory import ServiceFactory

__author__ = 'xxx'

primitive = (int, str, float, bool)

class An:
    def __init__(self, **entries): self.__dict__.update(entries)
    def as_json(self, exclude=(), extra=()):
        data = {}
        for k in self.__dict__:
            if k in exclude: continue
            value = self._serialize(self.__dict__[k])
            data[k] = value
        return data

    @classmethod
    def _serialize(cls, value, follow_fk=False):
        if isinstance(value, datetime.datetime):
            if value.utcoffset() is not None:
                value = value - value.utcoffset()
            return value.strftime('%Y-%m-%dT%H:%M:%S')
        if type(value) in (datetime, datetime.date):
            ret = value.isoformat()
        elif isinstance(value, primitive):
            ret = value
        elif hasattr(value, '__iter__'):
            ret = []
            for v in value:
                if isinstance(v, An):
                    serialized = v.as_json()
                    ret.append(serialized)
        elif isinstance(value, An):
            ret = value.as_json()
        else:
            ret = value

        return ret

class TestServiceFactory(ServiceFactory):
    def get_config(self):
        config = super(TestServiceFactory, self).get_config()
        config.update({
            'SQLALCHEMY_DATABASE_URI':'sqlite:///:memory:',
            'SESSION_SECRET_KEY':'ASJAFLSDFJOWEJIFOWEJF',
            'IS_DEBUG': True,
            'UPLOAD_FOLDER':'/tmp/upload'
        })
        return config