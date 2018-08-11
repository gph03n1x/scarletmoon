#!/usr/bin/python
import re

from vendor.porter import PorterStemmer
import settings

tokenizer_regex = re.compile('[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+',
                             re.MULTILINE)


STEM_ENABLED = settings.STEM_ENABLED


def tokenizer(text):
    """
    Tokenizes text into tokens.
    :param text:
    :return:
    """
    tokens = tokenizer_regex.findall(text)
    # filter(lambda s: len(s)>1, tokens)
    return tokens


class ExtendedPorterStemmer(PorterStemmer):

    """
    Extends the porter stemmer with a stem_words method.
    """

    def stem_words(self, words):
        """
        stems each token in list of tokens
        :param words
        :return: list of stemmed tokens
        """
        if STEM_ENABLED:
            return [self.stem(word, 0, len(word)-1) for word in words]
        return words

    def stem_word(self, word):
        if STEM_ENABLED:
            return self.stem(word, 0, len(word)-1)
        return word


if __name__ == "__main__":
    t = """Question: I want try - something.  Should I?
    Answer  : I'd assume so.  Give it a try.
    Aren't you in hurry ?"""
    tk = tokenizer(t)
    print(tk)
    """
    ['Question', 'I', 'want', 'try', 'something', 'Should', 'I', 'Answer', "I'd",
    'assume', 'so', 'Give', 'it', 'a', 'try', "Aren't", 'you', 'in', 'hurry']
    """
