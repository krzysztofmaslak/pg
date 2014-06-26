from pg.app import db

__author__ = 'xxx'

from ..model import User, Currency, CurrencyRate, Country


class CountryService:

    def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

    def find_all(self):
        return Country.query.all()

    def save(self, country):
        if isinstance(country, Country):
            db.session.add(country)
            db.session.commit()
            return country
        else:
            raise TypeError("Expected Country type in CountryService.save %s"%type(country))
