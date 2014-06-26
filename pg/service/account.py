from pg import Account, db

__author__ = 'krzysztof.maslak'

class AccountService:
    def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

    def save(self, account):
        if isinstance(account, Account):
            db.session.add(account)
            db.session.commit()
        else:
            raise TypeError('Expected Account type in AccountService.save actual %s'%type(account))