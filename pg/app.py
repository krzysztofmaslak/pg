from flask.ext.mail import Mail

__author__ = 'xxx'

from flask import Flask
from pg import rest, wsgi, payments, model

DEFAULT_BLUEPRINTS = [
    rest.offer,
    rest.offer_item,
    rest.offer_item_variation,
    rest.payment,
    rest.login_blueprint,
    rest.order,
    rest.register_rest,
    rest.withdraw,
    wsgi.wsgi_blueprint,
    payments.striper.stripe_rest,
    payments.paypal.paypal_init,
    payments.paypal.paypal_success,
    payments.paypal.ipn
]


class App:

    def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

    def create_app(self):
        self.app = Flask(__name__)
        self.configure_logging(self.app)
        self.configure_mail(self.app)
        self.configure_session(self.app)
        self.configure_blueprints(self.app, DEFAULT_BLUEPRINTS)
        self.configure_extensions(self.app)
        self.ioc.app = self.app
        return self.app

    def configure_mail(self, app):
        app.config.update(
            MAIL_SERVER='localhost',
            MAIL_PORT=25,
            MAIL_USE_SSL=False,
            MAIL_USERNAME = 'you@google.com',
            MAIL_PASSWORD = 'GooglePasswordHere'
            )
        self.ioc.mail = Mail(app)

    def configure_blueprints(self, app, blueprints):
        for blueprint in blueprints:
            blueprint.ioc = self.ioc
            blueprint.logger = app.logger
            app.register_blueprint(blueprint)

    def configure_extensions(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = self.ioc.get_config()['SQLALCHEMY_DATABASE_URI']
        model.base.db.init_app(app)

    def configure_session(self, app):
        app.secret_key = self.ioc.get_config()['SESSION_SECRET_KEY']

    def configure_logging(self, app):
        app.debug = self.ioc.get_config()['IS_DEBUG']
        if not app.debug:
            import logging
            from logging.handlers import TimedRotatingFileHandler
            file_handler = TimedRotatingFileHandler("run", when='D')
            file_handler.setLevel(logging.WARNING)
            app.logger.addHandler(file_handler)
        self.ioc.logger = app.logger

    def init_db(self):
        with self.app.app_context():
            # Extensions like Flask-SQLAlchemy now know what the "current" app
            # is while within this block. Therefore, you can now run........
            model.base.db.drop_all()
            model.base.db.create_all()

