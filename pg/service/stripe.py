from pg import model
import stripe

__author__ = 'xxx'


class StripeService:

    def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

    def save(self, stripe_message):
        if isinstance(stripe_message, model.StripeMessage)==False:
            raise TypeError("Expected StripeMessage type in StripeService.save actual %s"%type(stripe_message))

        model.base.db.session.add(stripe_message)
        model.base.db.session.commit()

    def charge(self, amount, currency, card, description):
        stripe.api_key = self.ioc.get_config()['stripe.secret']
        return stripe.Charge.create(
                amount=amount,
                currency=currency,
                card=card,
                description=description
            )