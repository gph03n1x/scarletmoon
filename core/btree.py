#!/usr/bin/python
import math


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
        :param frequency:
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
        if key < self.key:
            return self.left
        return self.right, self



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


            if key < node.key:
                if node.left is not None:
                    node = node.left
                    continue
                else:
                    node.left = KeyNode(key, value, doc_freq, term_freq)
                    self.size += 1
                    break

            elif node.key == key:
                node.update(value, doc_freq, term_freq)
                break
            else:
                if node.right is not None:
                    node = node.right
                    continue

                else:
                    node.right = KeyNode(key, value, doc_freq, term_freq)
                    self.size += 1
                    break

    def find(self, key):
        """
        looks for a key-node.
        :param key:
        :return:
        """
        node = self.root
        while node:
            if key == node.key:
                return node, node.idf(self.get_doc_count())
            node, _ = node.get_next(key)

        return None

    def delete_tr(self):
        """
        deletes the tree using the garbage collector
        :return:
        """
        self.root = None

    def traverse(self):
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
