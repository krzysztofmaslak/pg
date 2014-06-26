from pg import model

__author__ = 'xxx'

class CountryService:

    def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

    def find_all(self):
        return model.Country.query.all()

    def save(self, country):
        if isinstance(country, model.Country):
            model.base.db.session.add(country)
            model.base.db.session.commit()
            return country
        else:
            raise TypeError("Expected Country type in CountryService.save %s"%type(country))
