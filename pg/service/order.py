from datetime import date
import random
from pg.util import sanitizer

__author__ = 'xxx'
from pg.exception import quantity_not_available
from pg import model

class OrderService:
    dictionary = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Z", "X", "C", "V", "B", "N", "M", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

    def __init__(self, ioc, logger):
        super().__init__()
        self.ioc = ioc
        self.logger = logger

    def find_by_id(self, order_id):
        return model.Order.query.filter(model.Order.id == order_id).first()

    def refund_order(self, order):
        if isinstance(order, model.Order):
            order.refund_payment = 1;
            model.base.db.session.commit()
        else:
            raise TypeError("Expected Order type in OrderService.refund_order %s"%type(order))

    def find_paid_orders_count(self, account):
        if isinstance(account, model.Account):
            return model.Order.query.filter(model.Order.payment_status == 'Completed', model.Order.account_id == account.id).count()
        else:
            raise TypeError("Expected Account type in OrderService.find_orders_count %s"%type(account))

    def find_by_page(self, account, page):
        if isinstance(account, model.Account):
            return model.Order.query.filter(model.Order.payment_status == 'Completed', model.Order.account_id == account.id).order_by(model.Order.creation_date.desc()).paginate(page, 10, False).items
        else:
            raise TypeError("Expected Account type in OrderService.find_by_page %s"%type(account))

    def get_order_total_reduced_by_fee(self, order):
        order_total = order.total
        variable_fee = order_total*4.0/100.0
        fixed_fee = 0.40
        total_fee = variable_fee+fixed_fee
        order_net = order_total-total_fee
        self.logger.info("Calculated fee for order %s [total=%s, fee=%s, net=%s]"%(order.order_number, order_total, total_fee, order_net))
        return order_net

    def process_paid_order(self, o):
        if isinstance(o, model.Order)==False:
            raise TypeError("Expected Order type in OrderService.process_paid_order actual %s"%type(o))
        o.total = self.find_order_total(o)
        order_net = self.get_order_total_reduced_by_fee(o)
        o.fee = o.total - order_net
        o.offer.account.balance += order_net
        o.payment_status = 'Completed'
        offer = model.Offer.query.filter(model.Offer.id==o.offer_id).first()
        if offer is None:
            raise RuntimeError("Couldn't find offer for offer id %s"%o.offer_id)
        for item in o.items:
            if item.variations is not None and item.variations.count()>0:
                for variation in item.variations:
                   for offer_item in offer.items:
                       if offer_item.id==item.offer_item_id:
                           for offer_variation_item in offer_item.variations:
                               if offer_variation_item.id==variation.offer_item_variation_id:
                                   offer_variation_item.quantity = offer_variation_item.quantity - variation.quantity
            else:
                for offer_item in offer.items:
                    if offer_item.id==item.offer_item_id:
                        offer_item.quantity = offer_item.quantity - item.quantity
        model.base.db.session.commit()

    def find_order_total(self, order):
        if isinstance(order, model.Order)==False:
            raise TypeError("Expected Order type in OrderService.find_order_total %s"%type(order))
        total = 0.0
        shipping = 0.0
        for i in order.items:
            if i.variations is not None and i.variations.count()!=0:
                for v in i.variations:
                    total = total+(v.quantity*(v.net+v.tax))
                    if v.quantity==1:
                        shipping = shipping + v.shipping
                    else:
                        shipping = shipping + v.shipping
                        for c in range(v.quantity-1):
                            if v.shipping_additional is not None:
                                shipping = shipping + v.shipping_additional
                            else:
                                shipping = shipping + v.shipping
            else:
                total = total+(i.quantity*(i.net+i.tax))
                if i.quantity==1:
                    shipping = shipping + i.shipping
                else:
                    shipping = shipping + i.shipping
                    for c in range(i.quantity-1):
                        if i.shipping_additional is not None:
                            shipping = shipping + i.shipping_additional
                        else:
                            shipping = shipping + i.shipping
        return total + shipping

    def save(self, payment):
        o = model.Order()
        o.order_number = self.generate_order_number()
        o.offer_id = payment.offer_id
        if hasattr(payment, 'subscribe'):
            o.subscribe = payment.subscribe
        o.payment_method = payment.payment_method
        o.currency = payment.currency
        if hasattr(payment, 'country'):
            o.country = payment.country
        o.lang = payment.lang

        b = model.Billing()
        b.first_name = sanitizer.html_to_text(payment.billing.first_name)
        b.last_name = sanitizer.html_to_text(payment.billing.last_name)
        b.address1 = sanitizer.html_to_text(payment.billing.address1)
        if hasattr(payment.billing, 'address2'):
            b.address2 = sanitizer.html_to_text(payment.billing.address2)
        b.country = payment.billing.country
        b.city = sanitizer.html_to_text(payment.billing.city)
        b.postal_code = sanitizer.html_to_text(payment.billing.postal_code)
        if hasattr(payment.billing, 'county'):
            b.county = sanitizer.html_to_text(payment.billing.county)
        b.email = sanitizer.html_to_text(payment.billing.email)
        b.same_address = payment.billing.same_address
        o.billing.append(b)

        if payment.shipping is not None and b.same_address == False:
            s = model.Shipping()
            s.first_name = sanitizer.html_to_text(payment.shipping.first_name)
            s.last_name = sanitizer.html_to_text(payment.shipping.last_name)
            s.address1 = sanitizer.html_to_text(payment.shipping.address1)
            if hasattr(payment.shipping, 'address2'):
                s.address2 = sanitizer.html_to_text(payment.shipping.address2)
            s.country = payment.shipping.country
            s.city = sanitizer.html_to_text(payment.shipping.city)
            s.postal_code = sanitizer.html_to_text(payment.shipping.postal_code)
            if hasattr(payment.shipping, 'county'):
                s.county = sanitizer.html_to_text(payment.shipping.county)
            if hasattr(payment.shipping, 'email'):
                s.email = sanitizer.html_to_text(payment.shipping.email)
            if hasattr(payment.shipping, 'company'):
                s.company = sanitizer.html_to_text(payment.shipping.company)
            if hasattr(payment.shipping, 'phone_number'):
                s.phone_number = sanitizer.html_to_text(payment.shipping.phone_number)
            o.shipping.append(s)
        offer_service = self.ioc.new_offer_service()
        offer = offer_service.find_by_id(payment.offer_id)
        if offer is None:
            raise ValueError("Couldn't find offer by id:"+payment.offer_id)
        if payment.items is None or len(payment.items)==0:
            raise ValueError("No items specified")
        o.account_id = offer.account_id
        # validate requested availability
        for item_dto in payment.items:
            if hasattr(item_dto, 'variation_id'):
                item = self.find_item_by_id(offer.items, item_dto.id)
                if item is not None and item.status==1:
                    variations = []
                    oi = model.OrderItem(o, item.title, item_dto.quantity, item.net, item.tax, item.shipping)
                    if hasattr(item, 'shipping_additional'):
                        oi.shipping_additional = item.shipping_additional
                    oi.multivariate = item.multivariate
                    item_variation = self.find_item_by_id(item.variations, item_dto.variation_id)
                    if item_variation is not None and item_variation.status==1 and item_variation.id==item_dto.selection:
                        if item_dto.quantity>item_variation.quantity:
                            raise quantity_not_available.QuantityNotAvailable("Trying to buy more products then are available")
                        else:
                            oiv = model.OrderItemVariation(oi, item_variation.title, item_dto.quantity, item_variation.net, item_variation.tax, item_variation.shipping)
                            if hasattr(item_variation, 'shipping_additional'):
                                oiv.shipping_additional = item_variation.shipping_additional
                            variations.append(oiv)
                    oi.variations = variations
                    o.items.append(oi)
                else:
                    raise ValueError("Couldn't find offer item for id:"+item_dto.id)
            else:
                if item_dto.quantity is not None and item_dto.quantity!=0:
                    item = self.find_item_by_id(offer.items, item_dto.id)
                    if item is not None and item.status==1:
                        if item.variations is not None and item.variations.count()!=0:
                            raise ValueError("Requesting item where there is variation selection")
                        else:
                            if item_dto.quantity>item.quantity:
                                raise quantity_not_available.QuantityNotAvailable("Trying to buy more products then are available")
                            else:
                                oi = model.OrderItem(o, item.title, item_dto.quantity, item.net, item.tax, item.shipping)
                                oi.shipping_additional = item.shipping_additional
                                oi.multivariate = item.multivariate
                                o.items.append(oi)
                    else:
                        raise ValueError("Couldn't find offer item for id: %s"%item_dto.id)
                else:
                    raise ValueError("No quantity specified or variation")


        o.total = self.find_order_total(o)
        model.base.db.session.add(o)
        model.base.db.session.commit()
        return o

    def generate_order_number(self):
        for i in range(300):
            year = self.dictionary[int(str(date.today().year)[3:])]
            month = self.dictionary[date.today().month]
            day = self.dictionary[date.today().day]
            hash = year+month+day
            hash = hash+self.dictionary[random.randint(1, len(self.dictionary)-1)]
            hash = hash+self.dictionary[random.randint(1, len(self.dictionary)-1)]
            hash = hash+self.dictionary[random.randint(1, len(self.dictionary)-1)]
            o = model.Order.query.filter(model.Order.order_number==hash).first()
            if o is None:
                return hash
        raise ValueError("Couldn't generate order number")

    def find_item_by_id(self, items, item_id):
        if items is not None:
            for i in items:
                if i.id == item_id:
                    return i
        return None