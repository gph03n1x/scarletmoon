#!/usr/bin/python
import operator

from core.queries.porter import PorterStemmer
from core.queries.query import sort_query
from core.ranking.tfidf import results_tfidf
from core.queries.logic import intersect, union, exempt
from core.terminal import results_menu


class ExtendedPorterStemmer(PorterStemmer):
    def stem_words(self, words):
        return [self.stem(word, 0, len(word)-1) for word in words]


def simple_search(pts, td, queries, multi_query_mode=False):
    # Improve search with info in case a word doesnt existx
    tf_idf = results_tfidf()
    total_results = set()
    operation = intersect

    if not multi_query_mode:
        queries = [queries]

    for query in queries:
        query = sort_query(query)

        token = query[0]
        stemmed_token = pts.stem(token, 0, len(token)-1)
        try:
            query_result, idf = td.find(stemmed_token)
        except TypeError:
            results = set()
        else:
            tf_idf.add_idf(idf, stemmed_token)
            tf_idf.add_documents(query_result)
            results = query_result.get_value()

        for enum, query_part in enumerate(query[1:]):
            query_part = pts.stem(query_part, 0, len(query_part)-1)

            if query_part.lower() == ":or:":
                operation = union

            if query_part.lower() == ":not:":
                operation = exempt

            else:
                if len(query_part) > 0:
                    try:
                        query_result, idf = td.find(query_part)
                    except TypeError:
                        pass
                    else:
                        tf_idf.add_idf(idf, query_part)
                        tf_idf.add_documents(query_result)

                        results = operation(results, query_result.get_value())

        if results is not None:
            total_results.update(results)

    else:
        results = tf_idf.calc_tf_idf(total_results)
        results =  [(td.identifier.retrieve(result), results[result]) for result in results]

        if results is not None and len(results) > 0:

            results_menu(sorted(results, key=operator.itemgetter(1), reverse=True))

        else:
            print("[-] No results found")
