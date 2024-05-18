from ebooklib import epub
from utils import Utils
from word_difficulty import WordDifficulty
import json
import requests

HEADERS = {
    'Accept': 'application/json'
}

LIMIT = 5
BOOK_DOWNLOAD_PATH = 'downloads/book.epub'
TEXT_FILE_PATH = 'downloads/test'

class Helper:
    def __init__(self):
        self.wd = WordDifficulty()

    def download_book(self, ia_id):
        download_url = f'https://archive.org/download/{ia_id}/{ia_id}.epub'
        response = requests.get(download_url)

        with open(BOOK_DOWNLOAD_PATH, 'wb') as file:
            file.write(response.content)
        
        book = epub.read_epub(BOOK_DOWNLOAD_PATH)

        return book

    def retrieve_books_helper(self, query_string):
        search_url = f'https://openlibrary.org/search.json?q={query_string}&has_fulltext=true&language=eng&public_scan_b=true&fields=key,title,author_name,editions,editions.*&limit={LIMIT}'
        response = requests.get(search_url, headers=HEADERS).json()

        return response

    def retrieve_words_helper(self, ia_id):
        book = self.download_book(ia_id)
        
        text_content = ""
        for item in book.get_items():
            text_content += Utils.document_item_to_string(item)
        
        with open(TEXT_FILE_PATH, 'w', encoding='utf-8') as file:
            file.write(text_content)

        word_difficulty_mapping = {}

        words = Utils.getWords(text_content)

        for word in words:
            if word not in word_difficulty_mapping:
                word_difficulty_mapping[word] = self.wd.evaluate_word_difficulty(word)
        
        sorted_words = sorted([(value, word) for word, value in word_difficulty_mapping.items() if value and not Utils.contains_upper(word)])

        return json.dumps([word for _, word in sorted_words][:100])