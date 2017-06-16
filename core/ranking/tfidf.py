#!/usr/bin/python


class results_tfidf:
    """
    Keeps track of each document and it's associated ranking
    """
    def __init__(self):
        self.tfidf = {}
        self.idf = {}
        self.docs = {}

    def add_documents(self, doc_object):
        """
        Adds documents to the docs dictionary
        :param doc_object:
        :return:
        """
        self.docs[doc_object.key] = doc_object.documents

    def add_idf(self, idf, term):
        """
        Adds a term's idf to the idf dictionary
        :param idf:
        :param term:
        :return:
        """
        self.idf[term] = idf

    def calc_tf_idf(self, documents):
        """
        Calculates each documents tf-idf ranking and then returns the
        tf-idf dictionary
        :param documents:
        :return:
        """
        for doc in documents:
            self.tfidf[doc] = 0
            for term in self.idf:
                #print(term+":" + str(self.docs[term][doc]*self.idf[term]))
                try:
                    self.tfidf[doc] += self.docs[term][doc]*self.idf[term]
                except KeyError:
                    pass
        return self.tfidf
