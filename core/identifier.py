#!/usr/bin/python

class Identifier:
    def __init__(self):
        self.ids = []
        self.current_id = 0

    def assign(self, document, article):
        self.ids.append({"document": document, "article": article})
        self.current_id += 1
        return self.current_id - 1

    def retrieve(self, id):
        return self.ids[id]
