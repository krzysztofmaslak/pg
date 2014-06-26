__author__ = 'xxx'

from pg import model

class UserService:

    def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

    def find_by_username(self, username):
        return model.User.query.filter(model.User.username == username).first()

    def add_user(self, u):
        if isinstance(u, model.User)==False:
            raise TypeError("Expected User type in UserService.add_user actual %s"%type(u))

        model.base.db.session.add(u)
        model.base.db.session.commit()
