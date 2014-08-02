from flask.ext.mail import Mail
from flask.ext.script import Manager
from werkzeug.security import generate_password_hash
from apscheduler.scheduler import Scheduler
import requests
from factory import ServiceFactory
from pg import app, model

gateway = app.App(ioc=ServiceFactory())
app = gateway.create_app()
manager = Manager(app)
sched = Scheduler(coalesce=True)

@sched.interval_schedule(hours=2)
def load_currencies():
    print('Processing currencies')
    currencies = gateway.ioc.new_currency_service().list()
    for c in currencies:
        if c.code!='eur':
            print("Find currency rate "+c.code)
            exchange = float(requests.get("http://quote.yahoo.com/d/quotes.csv?s=eur" + c.code + "=X&f=l1&e=.csv").text)
            rate = model.CurrencyRate(c.code, exchange)
            gateway.ioc.new_currency_service().save_rate(rate)

processing_emails = False

@sched.interval_schedule(minutes=2)
def process_emails():
    global processing_emails
    if processing_emails:
        return
    processing_emails = True
    gateway.ioc.new_email_service().process_emails()
    processing_emails = False

sched.start()

@manager.command
def init_db():
    gateway.init_db()

@manager.command
def add_root():
    a = model.Account()
    a.lang = 'en'
    a.name = 'elittleangel'
    u = model.User('dublin.krzysztof.maslak@gmail.com', generate_password_hash('abcd'))
    u.active = True
    a.users.append(u)
    gateway.ioc.new_account_service().save(a)
    # TODO create start currencies
    # TODO add all countries
    for code in ['au', 'at', 'be', 'ca', 'hr', 'cz', 'dk', 'fi', 'fr', 'de', 'gi', 'gb', 'gr', 'gl', 'gg', 'va',
                 'hk', 'hu', 'is', 'ie', 'im', 'it', 'jp', 'je', 'li', 'lt', 'lu', 'nl', 'nz', 'no', 'pl', 'pt',
                 'ru', 'sg', 'sk', 'za', 'es', 'se', 'ch', 'uk', 'us']:
        gateway.ioc.new_country_service().save(model.Country(code))
    for code in ['aud', 'cad', 'chf', 'dkk', 'eur', 'gbp', 'nok', 'nzd', 'pln', 'sek', 'usd']:
        gateway.ioc.new_currency_service().save_currency(model.Currency(code, 1))

if __name__ == '__main__':
    manager.run()
