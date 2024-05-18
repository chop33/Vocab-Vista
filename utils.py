from bs4 import BeautifulSoup
import re

class Utils:

    def document_item_to_string(item):
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        text = [para.get_text() for para in soup.find_all('p')]
        return ''.join(text)

    def contains_upper(string):
        return any([c.isupper() for c in string])

    def getWords(text):
        return re.compile('[\w\-]+').findall(text)