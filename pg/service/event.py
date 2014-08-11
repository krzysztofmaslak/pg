import datetime

__author__ = 'root'

from pg import model, util

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
        print('listing events from %s to %s total %s'%(from_date, to_date, len(events)))
        account = self.ioc.new_account_service().find_by_id(account_id)
        all_offers_traffic = {}
        for event in events:
            if event.hash is not None:
                if event.hash not in all_offers_traffic:
                    offer = self.ioc.new_offer_service().find_by_hash(event.hash)
                    offer_traffic = {'count':1, 'hash':offer.hash}
                    traffic_title = util.LocaleUtil().get_localized_title(offer, account.lang)
                    offer_traffic['title']=traffic_title
                    all_offers_traffic[event.hash]=offer_traffic
                else:
                    offer_traffic = all_offers_traffic[event.hash]
                    offer_traffic['count'] = 1 + offer_traffic['count']
        traffic_list = []
        for k in all_offers_traffic:
            traffic_list.append(all_offers_traffic[k])
        traffic_list.sort(key=lambda x: x['count'], reverse=True)
        return traffic_list
