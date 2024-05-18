import nltk
from geotext import GeoText
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist

CORPORA_LIST = [
    'stopwords',
    'words',
    'reuters',
    'brown',
    'gutenberg',
    'names',
    'webtext',
    'nps_chat',
    'inaugural',
    'wordnet',
    'movie_reviews'
]

class WordDifficulty:

    def __init__(self):
        self.download_corpora()
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        self.words = set(nltk.corpus.words.words())
        self.names = set(nltk.corpus.names.words())

        all_synsets = list(nltk.corpus.wordnet.all_synsets())
        all_wordnet_words = []
        for synset in all_synsets:
            all_wordnet_words.extend(synset.lemma_names())
        self.wordnet_words = set(all_wordnet_words)

        self.word_freq = {
            "words": FreqDist(nltk.corpus.words.words()),
            "wordnet_words": FreqDist(all_wordnet_words),
            "movie_reviews": FreqDist(nltk.corpus.movie_reviews.words()),
            "reuters": FreqDist(nltk.corpus.reuters.words()),
            "brown": FreqDist(nltk.corpus.brown.words()),
            "gutenberg": FreqDist(nltk.corpus.gutenberg.words()),
            "webtext": FreqDist(nltk.corpus.webtext.words()),
            "nps_chat": FreqDist(nltk.corpus.nps_chat.words()),
            "inaugural": FreqDist(nltk.corpus.inaugural.words()),
        }
        self.lemmatizer = WordNetLemmatizer()

    def download_corpora(self):
        for corpora in CORPORA_LIST:
            nltk.download(corpora)

    def evaluate_word_difficulty(self, word):
        word = word.lower()
        base_form = self.to_base_form(word)

        value = self.score_word_difficulty(word)
        sum_eval = value
        if base_form != word:
            value_base = self.score_word_difficulty(base_form)
            if value_base:
                sum_eval = max(sum_eval, value_base) if sum_eval else value_base
        return sum_eval

    def score_word_difficulty(self, word):
        word = word.lower()

        # if word is an easy stop word, just return a high number
        if word in self.stop_words:
            return 500
    
        eval_result = self.eval_word(word)
        if not self.is_a_word(word, eval_result):
            return
        sum_eval = sum(eval_result.values())
        return sum_eval

    def eval_word(self, word):
        word = word.lower()
        return {corpus: freq[word] for corpus, freq in self.word_freq.items()}

    def is_a_proper_noun(self, word):
        geo = GeoText(word.title())
        if geo.cities or geo.countries or geo.nationalities or word in self.names:
            return True
        return False

    def is_a_word(self, word, eval_result):
        # Check if word is a number
        if word.isnumeric():
            return False
        
        # Check if word is a proper noun (people or city names)
        if self.is_a_proper_noun(word):
            return False
        
        # Check if word is a very commonly used word e.g. "the", "of"
        if any(value in self.stop_words for value in [word, word.title()]):
            return True
        
        # # Check if word frequency is above zero for non-movie reviews
        # non_movie_reviews_eval = sum(value for key, value in eval_result.items() if key not in ["movie_reviews"])
        # if not non_movie_reviews_eval:
        #     return False
        # Check if word appears only once in corpus. Likely not a word or very obscure

        # Check if word appears more than once in the corpus.
        # If it appears only once, it's likely not a word or very obscure.
        return sum(eval_result.values()) > 1

    def to_base_form(self, word):
        base_word = self.slang_to_normal(word)
        base_word = self.lemmatize(base_word, 'n')
        base_word = self.lemmatize(base_word, 'v')
        
        return base_word

    def lemmatize(self, word, speech_type):
        return self.lemmatizer.lemmatize(word, pos=speech_type)

    def slang_to_normal(self, word):
        if word.endswith("in") and f"{word}g" in self.words:
            return f"{word}g"
        return word