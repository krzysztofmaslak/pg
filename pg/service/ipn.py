from pg import model

__author__ = 'root'

class IpnMessageService:
     def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

     def persist(self, ipn_message):
        if isinstance(ipn_message, model.IpnMessage):
            model.base.db.session.add(ipn_message)
            model.base.db.session.commit()
            return ipn_message
        else:
            raise TypeError("Expected Order type in IpnMessageService.persist %s"%type(ipn_message))

     def merge(self, ipn_message):
        if isinstance(ipn_message, model.IpnMessage):
            model.base.db.session.merge(ipn_message)
            model.base.db.session.commit()
            return ipn_message
        else:
            raise TypeError("Expected Order type in IpnMessageService.merge %s"%type(ipn_message))
