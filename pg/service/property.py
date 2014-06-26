__author__ = 'xxx'

from pg import model

class PropertyService:

    def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

    def find_value_by_code(self, account, code):
        if isinstance(account, model.Account)==False:
            raise TypeError("Expected Account type in PropertyService.find_value_by_code %s"%type(account))

        return model.Property.query.filter(model.Property.account_id == account.id, model.Property.code==code).first().value