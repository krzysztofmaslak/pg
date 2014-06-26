from pg import model

__author__ = 'krzysztof.maslak'

class EmailService:

    def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

    def save(self, email):
        if isinstance(email, model.Email):
            model.base.db.session.add(email)
            model.base.db.session.commit()
            return email
        else:
            raise TypeError("Expected Email type in EmailService.save %s"%type(email))