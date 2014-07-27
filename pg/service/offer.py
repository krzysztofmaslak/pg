from datetime import date
from pg.util import sanitizer

__author__ = 'xxx'

from pg import model

class OfferService:
    dictionary = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Z", "X", "C", "V", "B", "N", "M", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

    def is_not_used(self, hash):
        o = model.Offer.query.filter(model.Offer.hash == hash).first()
        return o is None

    def find_by_id(self, offer_id):
        return model.Offer.query.filter(model.Offer.status == 1, model.Offer.id == offer_id).first()

    def find_by_page(self, account, page):
        if isinstance(account, model.Account):
            return model.Offer.query.filter(model.Offer.status == 1, model.Offer.account_id == account.id).paginate(page, 10, False).items
        else:
            raise TypeError("Expected Account type in OfferService.find_by_page %s"%type(account))

    def find_by_hash(self, hash):
        return model.Offer.query.filter(model.Offer.hash == hash).first()

    def find_offers_count(self, account):
        if isinstance(account, model.Account):
            return model.Offer.query.filter(model.Offer.status == 1, model.Offer.account_id == account.id).count()
        else:
            raise TypeError("Expected Account type in OfferService.find_offers_count %s"%type(account))

    def generate_hash(self):
        year = self.dictionary[int(str(date.today().year)[3:])]
        month = self.dictionary[date.today().month]
        day = self.dictionary[date.today().day]
        hash = year+month+day
        if self.is_not_used(hash):
            return hash
        for jstr in self.dictionary:
            if self.is_not_used(hash+jstr):
                return hash+jstr
            for kstr in self.dictionary:
                if self.is_not_used(hash+jstr+kstr):
                    return hash+jstr+kstr
                for lstr in self.dictionary:
                    if self.is_not_used(hash+jstr+kstr+lstr):
                        return hash+jstr+kstr+lstr
                    for mstr in self.dictionary:
                        if self.is_not_used(hash+jstr+kstr+lstr+mstr):
                            return hash+jstr+kstr+lstr+mstr
        raise RuntimeError('Failed to find hash')

    def save_offer(self, account, offer_dto):
        if isinstance(account, model.Account)==False:
            raise TypeError("Expected Account type in OfferService.save_offer %s"%type(account))
        o = model.Offer.query.filter(model.Offer.id == offer_dto.id, model.Offer.account_id == account.id).first()
        if o is None:
            raise RuntimeError("Couldn't find offer for offer id %s and account id %s"%(offer_dto.id, account.id))
        if o.status==0:
            o.hash = self.generate_hash()
        o.status = 1
        o.title = sanitizer.html_to_text(offer_dto.title)
        o.currency = offer_dto.currency
        if o.items is not None and len(o.items.all())>0:
            for item in o.items:
                offer_item_dto = self.find_item_by_id(item.id, offer_dto.items)
                if offer_item_dto is None:
                    o.items.remove(item)
        if o.items is not None and len(o.items.all())>0:
            for item in o.items:
                offer_item_dto = self.find_item_by_id(item.id, offer_dto.items)
                if offer_item_dto is not None:
                    item.title = sanitizer.html_to_text(offer_item_dto.title)
                    item.status = 1

                    item.multivariate = offer_item_dto.multivariate
                    if item.multivariate==1:
                        if item.variations is not None and len(item.variations.all())>0:
                            for iv in item.variations:
                                iv_dto = self.find_item_by_id(iv.id, offer_item_dto.variations)
                                if iv_dto is None:
                                    item.variations.remove(iv)
                            for iv in item.variations:
                                iv_dto = self.find_item_by_id(iv.id, offer_item_dto.variations)
                                if iv_dto is not None:
                                   iv.title = iv_dto.title
                                   iv.quantity = iv_dto.quantity
                                   iv.net = iv_dto.net
                                   if hasattr(iv_dto, 'tax'):
                                    iv.tax = iv_dto.tax
                                   iv.shipping = iv_dto.shipping
                                   if hasattr(iv_dto, 'shipping_additional'):
                                    iv.shipping_additional = iv_dto.shipping_additional
                                   iv.status = 1
                    else:
                        item.quantity = offer_item_dto.quantity
                        item.net = offer_item_dto.net
                        if hasattr(offer_item_dto, 'tax'):
                            item.tax = offer_item_dto.tax
                        item.shipping = offer_item_dto.shipping
                        if hasattr(offer_item_dto, 'shipping_additional'):
                            item.shipping_additional = offer_item_dto.shipping_additional


        model.base.db.session.commit()
        return o

    def find_item_by_id(self, id, items):
        if items is not None:
            for item in items:
                if item.id==id:
                    return item
        return None

    def new_offer(self, account):
        if isinstance(account, model.Account)==False:
            raise TypeError("Expected Account type in OfferService.new_offer %s"%type(account))
        o = model.Offer(account)
        model.base.db.session.add(o)
        model.base.db.session.commit()
        return o

    def new_offer_item(self, account, offer_id):
        o = model.Offer.query.filter(model.Offer.id == offer_id).first()
        if isinstance(account, model.Account)==False:
            raise TypeError("Expected Account type in OfferService.new_offer_item %s"%type(account))
        if o.account_id!=account.id:
            raise RuntimeError("Trying to save offer for different account")
        oi = model.OfferItem(o)
        model.base.db.session.add(oi)
        model.base.db.session.commit()
        return oi

    def new_offer_item_variation(self, account, offer_item_id):
        oi = model.OfferItem.query.filter(model.OfferItem.id == offer_item_id).first()
        if isinstance(account, model.Account)==False:
            raise TypeError("Expected Account type in OfferService.new_offer_item %s"%type(account))
        if oi.offer.account_id!=account.id:
            raise RuntimeError('Tried to save offer variation for other users offer')
        oiv = model.OfferItemVariation(oi)
        model.base.db.session.add(oiv)
        model.base.db.session.commit()
        return oiv

    def delete_offer(self, account, offer_id):
        o = model.Offer.query.filter(model.Offer.id == offer_id, model.Offer.account_id == account.id).first()
        if isinstance(account, model.Account)==False:
            raise TypeError("Expected Account type in OfferService.new_offer_item %s"%type(account))
        if o is None:
            raise RuntimeError('No offer to delete')
        model.base.db.session.delete(o)
        model.base.db.session.commit()

    def list(self):
        return model.Offer.query.all()

