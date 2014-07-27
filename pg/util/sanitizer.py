__author__ = 'root'

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.convert_charrefs=False
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def html_to_text(html):
    if html is not None:
        parser = MyHTMLParser()
        parser.feed(html)
        return parser.get_data()
    else:
        return html