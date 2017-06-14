#!/usr/bin/python
import string
from core.identifier import Identifier

class FirstLetterSplitter:
    """
    A tree per letter, digit, misc.
    """
    def save(self):
        pass

    def __init__(self, structure, ngram_index):
        self.ngram_index = ngram_index
        self.structs = {}
        self.count = 0
        self.identifier = Identifier()
        for letter in string.ascii_lowercase:
            self.structs[letter] = structure(self)
        for digit in string.digits:
            self.structs[digit] = structure(self)
        self.structs['misc'] = structure(self)

    def __getitem__(self, first_letter):
        first_letter = first_letter[0]  # Can accept strings too that way.
        if first_letter in self.structs:
            return self.structs[first_letter]
        return self.structs['misc']

    def update_tree(self, document):
        tokens = document.frequencies
        id = self.identifier.assign(*document.identifier())
        for token in tokens:
            self.count += 1
            term_freq = tokens[token] / document.total_tokens
            self[token].add(token, id, term_freq)

        tokens = document.tokens
        for token in tokens:
            self.ngram_index.index_token(token)

    def traverse(self):
        nodes = []
        for key in self.structs:
            nodes += self.structs[key].traverse()
        return nodes

    def find(self, token):
        return self[token].find(token)

    def visualize_tree(self):
        for key in self.structs:
            self.structs[key].visualizeTree(key)

    def size(self, category=None):
        if category is None:
            return sum(self.structs[key].size for key in self.structs)
        elif category in self.structs:
            return self.structs[category].size
