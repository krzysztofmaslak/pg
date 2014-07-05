from pg import model
import stripe

__author__ = 'xxx'


class PaypalService:

    def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

    def save(self, stripe_message):
        if isinstance(stripe_message, model.StripeMessage)==False:
            raise TypeError("Expected StripeMessage type in StripeService.save actual %s"%type(stripe_message))

        model.base.db.session.add(stripe_message)
        model.base.db.session.commit()

    def generate_init_html(self, order, payment_reference, basket_items, ipn_host, seller, paypal_url):
         html = """<html>
                <head></head>
                <body>
                <div>
                    <form id="paypalForm" action='"""+paypal_url+'/cgi-bin/webscr" method="post">'+"""
                    <input type="hidden" name="cmd" value="_cart"/>
                    <input type="hidden" name="custom" value='"""+payment_reference+"""'/>
                    <input type="hidden" name="upload" value="1"/>
                    <input type="hidden" name="business" value='"""+seller+"""'/>
                    <input type="hidden" name="currency_code" id="currency_code" value='"""+order.currency+"""'/>
                    """
         for item in basket_items:
            basket_items = basket_items+"""<input type="hidden" name="item_name_"""+item['index']+'" value="'+item['title']+'"/>'
            basket_items = basket_items+'<input type="hidden" name="amount_"'+item['index']+'" value="'+ item['value']+'"/>'
         html += """
                    <input type="hidden" name="item_number" value="BB-PROD1"/>
                    <input type="hidden" name="notify_url" value='"""+ipn_host+"""/pg/paypal/ipn'/>"""
         b = order.billing.first()
         html += """<input type="hidden" name="country_code" value='"""+b.country+"""'/>
            <input type="hidden" name="address1" value='"""+b.address1+"""'/>
            <input type="hidden" name="address2" value='"""+b.address2+"""'/>
            <input type="hidden" name="city" value='"""+b.city+"""'/>"""
         if b.county is not None and len(b.county)!=0:
            html = html + "<input type=\"hidden\" name=\"county\" value=\""+b.county+"\"/>"
         if b.postal_code is not None and len(b.postal_code)!=0:
            html = html + "<input type=\"hidden\" name=\"zip\" value=\""+b.postal_code+"\"/>"
         html = html+"""<input type="hidden" name="email" value='"""+b.email+"""'/>
        <input type="hidden" name="first_name" value='"""+b.first_name+"""'/>
        <input type="hidden" name="last_name" value='"""+b.last_name+"""'/>
        <input type="hidden" name="payer_email" value='"""+b.email+"""'/>
        <input type="hidden" name="payer_id" value='"""+b.id+"""'/>
        <script type="text/javascript">document.getElementById('paypalForm').submit()</script>
        </form>
        </div>
        </body>
        </html>"""
         return html