#!/usr/bin/python

class Identifier:
    """
    Article Identifier
    Assigns a id kinda like sql auto increment works.
    """
    def __init__(self):
        self.ids = []
        self.current_id = 0

    def assign(self, document, article):
        """
        Adds a {"document": document, "article": article} to the ids list.
        knows the position through the current id
        :param document:
        :param article:
        :return:
        """
        self.ids.append({"document": document, "article": article})
        self.current_id += 1
        return self.current_id - 1

    def retrieve(self, id):
        return self.ids[id]
