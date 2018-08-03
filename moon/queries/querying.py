#!/usr/bin/python
import heapq
import operator

from moon.identifier import retrieve_by_id
from moon.queries.logic import exempt, intersect, union
from moon.ranking.tfidf import results_tfidf

priorities = {
    "<and>": 2,
    "<or>": 1,
    "<not>": 2
}

operations = {
    "<and>": intersect,
    "<or>": union,
    "<not>": exempt
}


def sort_query(query, default_op="<or>"):
    """
    sorts a query based on the boolean priorities.
    :param: testing <or> not something <not> hype <or> random <not> python
    :return: ['something', '<and>', 'testing', '<or>', 'not', '<or>', 'random', '<not>', 'hype', '<not>', 'python']
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

    return " ".join([heapq.heappop(heap)[1] for _ in range(len(heap))]).split(" ", 1)[1].split()


def simple_search(stemmer, token_index, queries):
    """
    Default search, finds results on each token, applies logic based on the
    query then represents the results based on their tf-idf score.
    :param stemmer:
    :param token_index: tokenindex
    :param queries:
    :return:
    """
    tf_idf = results_tfidf()
    total_results = set()
    operation = intersect

    for query in queries:
        query = sort_query(query)
        token = query[0]

        stemmed_token = stemmer.stem_word(token)

        query_result, idf = token_index.find(stemmed_token)
        tf_idf.add_idf(idf, stemmed_token)

        if query_result is None:
            results = set()

        else:
            tf_idf.add_documents(query_result)
            results = query_result.get_value()

        for enum, query_part in enumerate(query[1:]):

            if query_part.lower() in operations.keys():
                operation = operations[query_part]
                continue

            query_part = stemmer.stem_word(query_part)

            query_result, idf = token_index.find(query_part)
            tf_idf.add_idf(idf, query_part)

            if query_result is None:
                value = set()
            else:
                value = query_result.get_value()
                tf_idf.add_documents(query_result)

            results = operation(results, value)

        if results is not None:
            total_results.update(results)

    else:
        results = tf_idf.calc_tf_idf(total_results)
        results = [(retrieve_by_id(result), results[result]) for result in results]

        if results is not None and len(results) > 0:
            return sorted(results, key=operator.itemgetter(1), reverse=True)
        else:
            return []
