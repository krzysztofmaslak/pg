from pg import model

__author__ = 'xxx'


class ContactService:

    def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

    def list(self):
        return model.Currency.query.all()

    def save_conctact(self, contact):
        if isinstance(contact, model.Contact):
            model.base.db.session.add(contact)
            model.base.db.session.commit()
            return contact
        else:
            raise TypeError("Expected Contact type in ContactService.save_conctact %s"%type(contact))
