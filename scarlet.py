#!/usr/bin/python

import re
import pickle
import heapq
import operator
import json
from core.btree import KeyTree
from vendor.porter import PorterStemmer
from core.parsers.SGM import reuters_SGM_processor
from core.queries.querying import simple_search
from core.structs.categorizer import FirstLetterSplitter
from core.ngrams import query_combinations, NGramIndex

from flask import Flask, request, Response

STORAGE = "storage/tokentree.pickle"
app = Flask(__name__)
pts = PorterStemmer()


try:
    with open(STORAGE, 'rb') as pickle_file:
        print("[*] Loading pickle file")
        td = pickle.load(pickle_file)
except IOError:
    print("[-] Creating a new inverted index")
    td = FirstLetterSplitter(KeyTree, NGramIndex(2))


@app.route("/search", methods=['GET'])
def text_search():
    original_query = request.args.get('query').lower()
    # TODO: simple search is bugged atm, fix later
    query = [part for part in re.split('\s+', original_query) if part]

    if "*" in original_query:
        # suggestions time yay:
        parts = []
        for token in query:
            if "*" in token:
                wn = td.ngram_index.wildcard_ngrams(token)
                unfiltered_results = td.ngram_index.suggestions(wn)
                filtered_results = td.ngram_index.post_filtering(token, unfiltered_results)
                print(filtered_results)
                parts.append(filtered_results)
            else:
                parts.append([token])

        queries = query_combinations(parts)
        return Response(json.dumps(simple_search(pts, td, queries)), status=200, mimetype='application/json')

    else:
        return Response(json.dumps(simple_search(pts, td, [query])), status=200, mimetype='application/json')


@app.route("/stats", methods=['GET'])
def scarlet_stats():
    limit = 100
    nodes = td.traverse()

    json_response = {
        "top_frequencies": [
            [result[0], result[1]] for result in heapq.nlargest(limit, nodes, key=operator.itemgetter(1))
        ],
        "size": td.size(),
        "limit": limit

     }
    return Response(json.dumps(json_response), status=200, mimetype='application/json')


@app.route("/index", methods=['GET'])
def index_data():
    match = request.args.get('file').lower()
    print("[*] Parsing: " + match)
    parsed_articles = reuters_SGM_processor(match)
    print("[*] Adding:  " + match)
    for parsed_article in parsed_articles:
        td.update_tree(parsed_article)


@app.route("/suggest", methods=['GET'])
def suggest_corrections():
    original_query = request.args.get('file').lower()

    query = [part for part in re.split('\s+', original_query) if part]
    parts = []
    for token in query:
        if "*" in token:
            wn = td.ngram_index.wildcard_ngrams(token)
            unfiltered_results = td.ngram_index.suggestions(wn)
            filtered_results = td.ngram_index.post_filtering(token, unfiltered_results)
            # print(filtered_results)
            parts.append(filtered_results)
        else:
            parts.append([token])

    queries = query_combinations(parts)
    for query in queries:
        print("[*] " + " ".join(query))


if __name__ == "__main__":
    app.run(debug=True)

