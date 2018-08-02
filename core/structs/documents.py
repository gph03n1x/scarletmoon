#!/usr/bin/python
from collections import Counter

from core.tokens import tokenizer
from vendor.porter import PorterStemmer


class document:
    def __init__(self, doc_name, title, text):
        """
        tokenizes the document, counts the occurances of each token,
        :param doc_name:
        :param title:
        :param text:
        """
        pts = PorterStemmer()
        self.doc_name = doc_name
        self.title = title
        self.text = text
        self.tokens = tokenizer(self.title + " " + self.text)
        self.total_tokens = len(self.tokens)
        self.frequencies = Counter(list(pts.stem(token.lower(), 0, len(token)-1) for token in self.tokens))
        self.tokens = set(self.tokens)

    def identifier(self):
        return self.doc_name, self.title

    def get_content(self):
        return self.title + self.text

    def __str__(self):
        return "Doc(name={0}, title={1}, text={2})".format(self.doc_name, self.title, self.text)

    def __repr__(self):
        return str(self)
