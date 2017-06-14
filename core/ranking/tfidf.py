#!/usr/bin/python


class results_tfidf:
    def __init__(self):
        self.tfidf = {}
        self.idf = {}
        self.docs = {}

    def add_documents(self, doc_object):
        self.docs[doc_object.key] = doc_object.documents

    def add_idf(self, idf, term):
        self.idf[term] = idf

    def calc_tf_idf(self, documents):
        for doc in documents:
            self.tfidf[doc] = 0
            for term in self.idf:
                #print(term+":" + str(self.docs[term][doc]*self.idf[term]))
                try:
                    self.tfidf[doc] += self.docs[term][doc]*self.idf[term]
                except KeyError:
                    pass
        return self.tfidf
