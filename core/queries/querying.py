#!/usr/bin/python
import heapq
import operator

from core.queries.porter import PorterStemmer
from core.ranking.tfidf import results_tfidf
from core.queries.logic import intersect, union, exempt
from core.terminal import results_menu

priorities = {
    ":and:": 1,
    ":or:": 1,
    ":not:": 2
}


def sort_query(query, default_op=":and:"):
    """
    sorts a query based on the boolean priorities.
    :param: testing :or: not something :not: hype :or: random :not: python
    :return: ['something', ':and:', 'testing', ':or:', 'not', ':or:', 'random', ':not:', 'hype', ':not:', 'python']
    """
    selected_priority = priorities[default_op]
    selected_operation = default_op
    heap = []
    for query_part in query:
        if query_part in priorities.keys():
            selected_priority = priorities[query_part]
            selected_operation = query_part
        else:
            heapq.heappush(heap, (selected_priority, selected_operation + " " + query_part))
            selected_priority = priorities[default_op]
            selected_operation = default_op

    return " ".join([heapq.heappop(heap)[1] for _iteration in range(len(heap))]).split(" ", 1)[1].split()


class ExtendedPorterStemmer(PorterStemmer):
    """
    Extends the porter stemmer with a stem_words method.
    """
    def stem_words(self, words):
        """
        stems each token in list of tokens
        :param words
        :return: list of stemmed tokens
        """
        return [self.stem(word, 0, len(word)-1) for word in words]


def simple_search(stemmer, token_index, queries, multi_query_mode=False):
    """
    Default search, finds results on each token, applies logic based on the
    query then represents the results based on their tf-idf score.
    :param stemmer:
    :param token_index: tokenindex
    :param queries:
    :param multi_query_mode:
    :return:
    """
    # TODO: Improve search with info in case a word doesnt existx
    tf_idf = results_tfidf()
    total_results = set()
    operation = intersect

    if not multi_query_mode:
        queries = [queries]

    for query in queries:
        query = sort_query(query)

        token = query[0]
        stemmed_token = stemmer.stem(token, 0, len(token) - 1)
        try:
            query_result, idf = token_index.find(stemmed_token)
        except TypeError:
            results = set()
        else:
            tf_idf.add_idf(idf, stemmed_token)
            tf_idf.add_documents(query_result)
            results = query_result.get_value()

        for enum, query_part in enumerate(query[1:]):
            query_part = stemmer.stem(query_part, 0, len(query_part) - 1)

            if query_part.lower() == ":or:":
                operation = union

            if query_part.lower() == ":not:":
                operation = exempt

            else:
                if len(query_part) > 0:
                    try:
                        query_result, idf = token_index.find(query_part)
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
        results =  [(token_index.identifier.retrieve(result), results[result]) for result in results]

        if results is not None and len(results) > 0:

            results_menu(sorted(results, key=operator.itemgetter(1), reverse=True))

        else:
            print("[-] No results found")
