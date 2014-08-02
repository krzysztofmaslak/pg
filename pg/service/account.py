from datetime import date
from pg import model

__author__ = 'krzysztof.maslak'

class AccountService:
    dictionary = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Z", "X", "C", "V", "B", "N", "M", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

    def is_not_used(self, hash):
        o = model.Account.query.filter(model.Account.hash == hash).first()
        return o is None

    def find_by_hash(self, hash):
        return model.Account.query.filter(model.Account.hash==hash).first()

    def find_by_id(self, id):
        return model.Account.query.get(id)
 
    def generate_hash(self):
        year = self.dictionary[int(str(date.today().year)[3:])]
        month = self.dictionary[date.today().month]
        day = self.dictionary[date.today().day]
        hash = 'S'+year+month+day
        if self.is_not_used(hash):
            return hash
        for jstr in self.dictionary:
            if self.is_not_used(hash+jstr):
                return hash+jstr
        for jstr in self.dictionary:
            for kstr in self.dictionary:
                if self.is_not_used(hash+jstr+kstr):
                    return hash+jstr+kstr
        for jstr in self.dictionary:
            for kstr in self.dictionary:
                for lstr in self.dictionary:
                    if self.is_not_used(hash+jstr+kstr+lstr):
                        return hash+jstr+kstr+lstr
        for jstr in self.dictionary:
            for kstr in self.dictionary:
                for lstr in self.dictionary:
                    for mstr in self.dictionary:
                        if self.is_not_used(hash+jstr+kstr+lstr+mstr):
                            return hash+jstr+kstr+lstr+mstr
        raise RuntimeError('Failed to find hash')

    def find_by_name(self, name):
        return model.Account.query.filter(model.Account.name == name).first()

    def save(self, account):
        if isinstance(account, model.Account):
            account.hash = self.generate_hash()
            model.base.db.session.add(account)
            model.base.db.session.commit()
        else:
            raise TypeError('Expected Account type in AccountService.save actual %s'%type(account))
