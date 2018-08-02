#!/usr/bin/python
import string
from core.identifier import assign


class FirstLetterSplitter:
    """
    Creates a token-tree per letter to categorize tokens based on the first letter of each token.
    There is a tree for every letter, every digit, and a misc tree for everything else.
    """

    def __init__(self, structure, ngram_index):
        self.ngram_index = ngram_index
        self.structs = {}
        self.count = 0
        for letter in string.ascii_lowercase:
            self.structs[letter] = structure(self)
        for digit in string.digits:
            self.structs[digit] = structure(self)
        self.structs['misc'] = structure(self)

    def __getitem__(self, first_letter):
        """
        returns the appropriate tree for the token we are looking for.
        :param first_letter:
        :return:
        """
        first_letter = first_letter[0]  # Can accept strings too that way.
        if first_letter in self.structs:
            return self.structs[first_letter]
        return self.structs['misc']

    def update_tree(self, document):
        """
        updates the tree with a new document.
        :param document:
        :return:
        """
        tokens = document.frequencies
        id = assign(*document.identifier())
        for token in tokens:
            self.count += 1
            doc_freq = tokens[token] / document.total_tokens

            self[token].add(token, id, doc_freq, tokens[token])

        tokens = document.tokens
        for token in tokens:
            self.ngram_index.index_token(token)

    def traverse(self):
        """
        traversing through every token-tree. Expensive on memory.
        :return:
        """
        nodes = []
        for key in self.structs:
            nodes += self.structs[key].traverse()
        return nodes

    def find(self, token):
        """
        looks for a token key-node
        :param token:
        :return:
        """
        return self[token].find(token)

    def size(self, category=None):
        """
        gets the size of the token-trees
        :param category:
        :return:
        """
        if category is None:
            return sum(self.structs[key].size for key in self.structs)
        elif category in self.structs:
            return self.structs[category].size
