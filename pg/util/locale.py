__author__ = 'root'

class LocaleUtil:
    def get_localized_title(self, item, lang):
        if lang=='fr':
            if item.title_fr is not None:
                return item.title_fr
            else:
                return item.title_en
        else:
            if item.title_en is not None:
                return item.title_en
            else:
                return item.title_fr

    def get_localized_description(self, item, lang):
        if lang=='fr':
            if item.description_fr is not None and len(item.description_fr)>0:
                return item.description_fr
            else:
                return item.description_en
        else:
            if item.description_en is not None and len(item.description_en)>0:
                return item.description_en
            else:
                return item.description_fr