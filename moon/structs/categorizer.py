#!/usr/bin/python
import string

from moon.btree import CSVBTree
from moon.identifier import assign
from moon.ngrams import NGramIndex


class NamedIndexes:

    def __init__(self, u_id):
        self.indexes = {}
        self.u_id = u_id

    def __getitem__(self, name):
        """
        returns the appropriate tree for the token we are looking for.
        :param first_letter:
        :return:
        """
        if name not in self.indexes:
            self.indexes[name] = FirstLetterSplitter(CSVBTree, NGramIndex(2), f"{self.u_id}-{name}")

        return self.indexes[name]


class FirstLetterSplitter:
    """
    Creates a token-tree per letter to categorize tokens based on the first letter of each token.
    There is a tree for every letter, every digit, and a misc tree for everything else.
    """

    def __init__(self, structure, ngram_index, u_id):
        self.ngram_index = ngram_index
        self.structs = {}
        self.count = 0
        for letter in string.ascii_lowercase:
            self.structs[letter] = structure(f"{u_id}-{letter}")
        for digit in string.digits:
            self.structs[digit] = structure(f"{u_id}-{digit}")
        self.structs['misc'] = structure(f"{u_id}-misc")

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

    def update_tree(self, document, url=""):
        """
        updates the tree with a new document.
        :param document:
        :param url:
        :return:
        """
        tokens = document.frequencies
        id = assign(*document.identifier(), url=url)
        for token in tokens:
            self.count += 1
            doc_freq = tokens[token] / document.total_tokens
            self[token].add(token.strip(), tokens[token],  id, doc_freq)

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
        return self[token].find(token.strip())

    def size(self, category=None):
        """
        gets the size of the token-trees
        :param category:
        :return:
        """
        if category is None:
            return sum(self.structs[key].rows for key in self.structs)
        elif category in self.structs:
            return self.structs[category].rows
