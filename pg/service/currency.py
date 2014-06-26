from pg import model

__author__ = 'xxx'


class CurrencyService:

    def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

    def list(self):
        return model.Currency.query.all()

    def save_currency(self, currency):
        if isinstance(currency, model.Currency):
            model.base.db.session.add(currency)
            model.base.db.session.commit()
            return currency
        else:
            raise TypeError("Expected Currenty type in CurrencyService.save_currency %s"%type(currency))

    def save_rate(self, rate):
        if isinstance(rate, model.CurrencyRate):
            model.base.db.session.add(rate)
            model.base.db.session.commit()
            return rate
        else:
            raise TypeError("Expected CurrentyRate type in CurrencyService.save_rate %s"%type(rate))

    def convert(self, currency, total):
        rate = model.CurrencyRate.query.filter(model.CurrencyRate.code==currency).first().rate
        if currency=='aud':
            return rate*total
        elif currency=="gbp":
            return rate*total
        elif currency=="dkk":
            return rate*total
        elif currency=="nok":
            return rate*total
        elif currency=="sek":
            return rate*total
        elif currency=="usd":
            return rate*total
        elif currency=="cad":
            return rate*total
        elif currency=="nzd":
            return rate*total
        elif currency=="chf":
            return rate*total
        elif currency=="isk":
            return rate*total
        elif currency=="pln":
            return rate*total
        return total
