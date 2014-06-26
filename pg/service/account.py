from pg import model

__author__ = 'krzysztof.maslak'

class AccountService:
    def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

    def save(self, account):
        if isinstance(account, model.Account):
            model.base.db.session.add(account)
            model.base.db.session.commit()
        else:
            raise TypeError('Expected Account type in AccountService.save actual %s'%type(account))