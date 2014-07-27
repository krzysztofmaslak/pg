__author__ = 'root'

from pg import model

__author__ = 'root'

class EventService:
     def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

     def persist(self, event):
        if isinstance(event, model.Event):
            model.base.db.session.add(event)
            model.base.db.session.commit()
            return event
        else:
            raise TypeError("Expected Event type in EventService.persist %s"%type(event))