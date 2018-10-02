#!/usr/bin/python
import math
import ast
import os.path


KEY_LEN, TERM_OCCUR_LEN, DOC_DICTIONARY_LEN = 50, 50, 250
LINE_LENGTH = KEY_LEN + TERM_OCCUR_LEN + DOC_DICTIONARY_LEN
SEP_CHAR = '&^'
FILL_CHAR = '~'


class CSVBTree:
    def __init__(self,name, rows):
        self.name = name
        self.rows = 0
        # if
        with open(self.name, 'r') as csv_file:
            self.rows = sum([1 for line in csv_file])

    def next_middle(self, level=1):
        return self.rows / (2 ** level)

    @staticmethod
    def row_to_csv(key, term_occurance, doc_freq_dict):
        remaining_key = (KEY_LEN - len(key) - len(SEP_CHAR)) * FILL_CHAR
        remaining_term = (TERM_OCCUR_LEN - len(str(term_occurance)) - len(SEP_CHAR)) * FILL_CHAR
        # -1 because we add newline
        remaining_dict = (DOC_DICTIONARY_LEN - len(str(doc_freq_dict)) - 1) * FILL_CHAR

        return f'{remaining_key}{key}&^{remaining_term}' \
               f'{term_occurance}&^{remaining_dict}{str(doc_freq_dict)}\n'

    @staticmethod
    def csv_to_row(row):
        vals = [val.strip(f'{FILL_CHAR}\n') for val in row.split(SEP_CHAR)]
        key, occurance, doc_freq_dict = vals
        return key, int(occurance), ast.literal_eval(doc_freq_dict)

    def update_row(self, key, value, doc_freq, term_occurrences):
        pass

    def add_row(self, key, value, doc_freq, term_occurrences):
        pass

    def find_row(self, key):
        print(self.rows)
        input()
        with open(self.name, 'r') as csv_file:
            pass
            row_id = 0
            direction = 1
            iteration = 1
            while True:
                row_id, row_key, *_ = row_id + direction * self.next_middle(iteration)
                if key == row_key:
                    return row_id
                elif key > row_key:
                    direction = -1
                else:
                    direction = 1
                iteration += 1


class KeyNode:
    """
    A keynode a structure that includes a term and
    the documents this term is found along with the frequency in
    each document and also tracks how many times this word was found.
    """
    def __init__(self, key, value, doc_freq, term_freq):
        self.left = None
        self.right = None
        self.key = key
        self.freq = term_freq
        self.documents = {value: doc_freq}

    def get_value(self):
        """
        returns the document identifiers where this word was found.
        :return: set
        """
        return set(self.documents.keys())

    def update(self, value, doc_freq, term_freq):
        """
        adds a document-article identifier and the frequency this word was found there.
        :param value:
        :param doc_freq:
        :param term_freq:
        :return:
        """
        self.freq += term_freq
        self.documents[value] = doc_freq

    def idf(self, number_of_tokens):
        """
        returns the idf log(N/(1+frequency))
        :param number_of_tokens:
        :return:
        """
        return math.log(number_of_tokens / (1 + self.freq))

    def __str__(self):
        return "Node(key={0}, freq={1}, docs={2})".format(self.key, self.freq, str(self.documents))

    def __repr__(self):
        return str(self)

    def get_next(self, key):
        """
        :param key:
        :return:
        """
        if key < self.key:
            return self.left, self
        return self.right, self

    def set_children(self, key, value, doc_freq, term_freq):
        """
        :param key:
        :param value:
        :param doc_freq:
        :param term_freq:
        :return:
        """
        if key < self.key:
            self.left = KeyNode(key, value, doc_freq, term_freq)
        else:
            self.right = KeyNode(key, value, doc_freq, term_freq)


class KeyTree:
    def __init__(self, parent=None):
        self.parent = parent
        self.root = None
        self.size = 0

    def get_doc_count(self):
        """
        returns the count of tokens in a tree.
        :return:
        """
        if self.parent is None:
            return self.size
        return self.parent.count

    def add(self, key, value, doc_freq, term_freq):
        """
        adds a document to the token-tree, along with the document frequency and the term frequency.
        :param key:
        :param value:
        :param doc_freq:
        :param term_freq:
        :return:
        """
        if self.root is None:
            self.root = KeyNode(key, value, doc_freq, term_freq)
            self.size += 1
            return

        node = self.root
        while True:

            if node.key == key:
                node.update(value, doc_freq, term_freq)
                break

            node, parent = node.get_next(key)

            if not node:
                parent.set_children(key, value, doc_freq, term_freq)
                break

    def find(self, key):
        """
        looks for a key-node.
        :param key:
        :return:
        """
        node = self.root
        while node:
            # print(node.key)
            if key == node.key:
                return node, node.idf(self.get_doc_count())
            node, _ = node.get_next(key)

        return None, 0  # default idf if the token doesnt exist

    def delete_tr(self):
        """
        deletes the tree using the garbage collector
        :return:
        """
        self.root = None

    def traverse(self):
        if self.root is None:
            return []

        queue = [self.root]
        nodes = []
        while queue:
            node = queue.pop()
            nodes.append((node.key, node.freq))
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return nodes
