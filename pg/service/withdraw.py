__author__ = 'xxx'

from pg import model

class WithdrawService:

    def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

    def save(self, w):
        if isinstance(w, model.Withdrawal)==False:
            raise TypeError("Expected Withdrawal type in WithdrawService.save actual %s"%type(w))

        model.base.db.session.add(w)
        model.base.db.session.commit()
