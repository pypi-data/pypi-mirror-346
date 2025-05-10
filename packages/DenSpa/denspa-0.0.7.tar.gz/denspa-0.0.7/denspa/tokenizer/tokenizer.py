import functools
from nltk.stem.snowball import SnowballStemmer


class Tokenizer:

    def __init__(self, stop_words=[], lang=None):
        ALL_PUNCTUATIONS = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        if lang=="de":
            from spacy.lang.de.stop_words import STOP_WORDS
            from spacy.lang.de import German
            self.nlp = German()
            self.stemmer = SnowballStemmer(language='german')
            self.stemmer.stemmer._GermanStemmer__step2_suffixes += ("in",)
            self.stop_words = list(ALL_PUNCTUATIONS) + ([] if stop_words is None else stop_words+list(STOP_WORDS) )
        else:
            from spacy.lang.en.stop_words import STOP_WORDS
            from spacy.lang.en import English

            self.nlp = English()
            self.stemmer = SnowballStemmer(language='english')
            self.stop_words = list(ALL_PUNCTUATIONS) + ([] if stop_words is None else stop_words+list(STOP_WORDS) )
        self.lang = lang

    def tokenize(self, text):
        return [t.text for t in self.nlp.tokenizer(text) if len(t.text.strip())>0 and t.text.lower() not in self.stop_words]

    @functools.lru_cache(maxsize=1000)
    def stem(self,word):
        if self.lang=="de":
            return self.stemmer.stem(self.stemmer.stem(word))
        else:
            return self.stemmer.stem(word)