#!/usr/bin/python
import heapq
import json
import operator
import pickle
import random
import re
import string
import sys

from core.btree import KeyTree
from core.ngrams import NGramIndex, query_combinations
from core.parsers.parser import PluginsSeeker
from core.queries.querying import simple_search
from core.structs.categorizer import FirstLetterSplitter
from flask import Flask, Response, redirect, request
from vendor.porter import PorterStemmer

if len(sys.argv) > 2:
    STORAGE = "{0}".format(sys.argv[2])

else:
    STORAGE = "storage/3F9UOCMRXXWP.pickle"

app = Flask(__name__)
pts = PorterStemmer()

PluginsSeeker.load_core_plugins()
print(PluginsSeeker.plugins)


try:
    with open(STORAGE, 'rb') as pickle_file:
        print("[*] Loading pickle file")
        td = pickle.load(pickle_file)
except IOError:
    print("[-] Creating a new inverted index")
    name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
    STORAGE = "storage/{0}.pickle".format(name)
    td = FirstLetterSplitter(KeyTree, NGramIndex(2))


@app.route("/search", methods=['GET'])
def text_search():
    original_query = request.args.get('query')

    # TODO: simple search is bugged atm, fix later due to using ':'
    if not original_query:
        return "form boi"

    query = [part for part in re.split('\s+', original_query.lower()) if part]

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


@app.route("/index", methods=['POST'])
def index_data():
    # TODO: think about it because if the indexer is restricted it cannot reach for the fs
    print(request.data)
    match = request.get_json().get('filename')
    print("[*] Parsing: " + match)
    handler = PluginsSeeker.find_handler(match)
    parsed_articles = handler.parse_document(match)
    print("[*] Adding:  " + match)
    for parsed_article in parsed_articles:
        td.update_tree(parsed_article)
    # need to store token tree again
    return Response(json.dumps({"status": 200}))


@app.route("/suggest", methods=['GET'])
def suggest_corrections():
    original_query = request.args.get('query').lower()

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
    return Response(json.dumps([" ".join(query) for query in queries]), status=200, mimetype='application/json')


@app.route("/", methods=['GET'])
def redirect_to_search():
    return redirect("/search", code=302)


if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', debug=True)
    except KeyboardInterrupt:
        with open(STORAGE, 'wb') as pickle_file:
            pickle.dump(td, pickle_file)
