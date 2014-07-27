import datetime

__author__ = 'root'

from pg import model


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

     def find_offer_traffic_for(self, account_id, from_date_str, to_date_str):
        from_date = datetime.datetime.strptime(from_date_str, '%Y-%m-%d')
        to_date = datetime.datetime.strptime(to_date_str+' 23:59:59', '%Y-%m-%d %H:%M:%S')
        events = model.Event.query.filter(model.Event.account_id==account_id, model.Event.creation_date>from_date, model.Event.creation_date<to_date).all()
        all_offers_traffic = {}
        for event in events:
            if event.hash is not None:
                offer_traffic = all_offers_traffic[event.hash]
                if offer_traffic is None:
                    offer = self.ioc.new_offer_srvice().find_by_hash(event.hash)
                    offer_traffic.count = 1
                    offer_traffic.title = offer.title
                else:
                    offer_traffic.count += 1
        return all_offers_traffic