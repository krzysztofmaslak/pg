__author__ = 'xxx'

from pg import model

class UserService:

    def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

    def find_by_username(self, username):
        return model.User.query.filter(model.User.username == username).first()

    def find_by_activation_hash(self, activation_hash):
        return model.User.query.filter(model.User.activation_hash==activation_hash).first()

    def find_by_reset_hash(self, reset_hash):
        return model.User.query.filter(model.User.reset_hash==reset_hash).first()

    def find_by_id(self, id):
        return model.User.query.get(id)

    def add_user(self, u):
        if isinstance(u, model.User)==False:
            raise TypeError("Expected User type in UserService.add_user actual %s"%type(u))

        model.base.db.session.add(u)
        model.base.db.session.commit()
