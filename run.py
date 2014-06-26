from flask.ext.script import Manager
from werkzeug.security import generate_password_hash
from apscheduler.scheduler import Scheduler
import requests
from factory import ServiceFactory
from pg.app import App
from pg.model import User, CurrencyRate, Country, Currency
from pg.model.account import Account
from pg.model.property import Property

app = App(ioc=ServiceFactory())
manager = Manager(app.create_app())
sched = Scheduler()

@sched.cron_schedule(hour=2)
def load_currencies():
    print('Processing currencies')
    currencies = app.ioc.new_currency_service().list()
    for c in currencies:
        if c.code!='eur':
            print("Find currency rate "+c.code)
            exchange = float(requests.get("http://quote.yahoo.com/d/quotes.csv?s=eur" + c.code + "=X&f=l1&e=.csv").text)
            rate = CurrencyRate(c.code, exchange)
            app.ioc.new_currency_service().save_rate(rate);
sched.start()

@manager.command
def init_db():
    app.init_db()

@manager.command
def add_root():
    with app.app.app_context():
        a = Account()
        a.properties.append(Property(a, 'invoice', 'invoice.issue.city', ''))
        u = User('dublin.krzysztof.maslak@gmail.com', generate_password_hash('abcd'))
        a.users.append(u)
        app.ioc.new_account_service().save(a)
        # TODO create start currencies
        # TODO add all countries
        for code in ['au', 'at', 'be', 'ca', 'hr', 'cz', 'dk', 'fi', 'fr', 'de', 'gi', 'gb', 'gr', 'gl', 'gg', 'va',
                     'hk', 'hu', 'is', 'ie', 'im', 'it', 'jp', 'je', 'li', 'lt', 'lu', 'nl', 'nz', 'no', 'pl', 'pt',
                     'ru', 'sg', 'sk', 'za', 'es', 'se', 'ch', 'uk', 'us']:
            app.ioc.new_country_service().save(Country(code))
        for code in ['aud', 'cad', 'chf', 'dkk', 'eur', 'gbp', 'nok', 'nzd', 'pln', 'sek', 'usd']:
            app.ioc.new_currency_service().save_currency(Currency(code, 1))

if __name__ == '__main__':
    manager.run()
