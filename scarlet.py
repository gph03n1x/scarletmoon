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
from core.ngrams import NGramIndex, query_combinations, suggest_if_needed
from core.parsers.parser import PluginsSeeker
from core.queries.querying import simple_search
from core.tokens import ExtendedPorterStemmer
from core.structs.categorizer import FirstLetterSplitter

from flask import Flask, Response, redirect, request

from celery import Celery

STORAGE = "storage/FMZ3W5793C0S.pickle"

app = Flask(__name__)
# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

pts = ExtendedPorterStemmer()

PluginsSeeker.load_core_plugins()
print(PluginsSeeker.plugins)

STATS_LIMIT = 100

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
    if not original_query:
        return "form boi"
    result = get_results.delay(original_query).get()
    return Response(json.dumps(result), status=200, mimetype='application/json')


@app.route("/stats", methods=['GET'])
def scarlet_stats():
    result = get_stats.delay().get()
    return Response(json.dumps(result), status=200, mimetype='application/json')


@app.route("/index", methods=['POST'])
def index_data():
    print(request.data)
    match = request.get_json().get('filename')
    add_to_index.delay(match)
    return Response(json.dumps({"status": 200}))


@app.route("/suggest", methods=['GET'])
def suggest_corrections():
    original_query = request.args.get('query').lower()
    result = get_suggestions.delay(original_query).get()
    return Response(json.dumps(result), status=200, mimetype='application/json')


@app.route("/", methods=['GET'])
def redirect_to_search():
    return redirect("/search", code=302)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, overwrite_token_tree.s(''))


@celery.task
def overwrite_token_tree(arg):
    print("############# Saving token tree #############")
    with open(STORAGE, 'wb') as pickle_file:
        pickle.dump(td, pickle_file)


@celery.task
def add_to_index(match):
    print("[*] Parsing: " + match)
    handler = PluginsSeeker.find_handler(match)
    parsed_articles = handler.parse_document(match)
    print("[*] Adding:  " + match)
    for parsed_article in parsed_articles:
        td.update_tree(parsed_article)

@celery.task
def get_results(original_query):
    query = [suggest_if_needed(td, part) for part in re.split('\s+', original_query.lower()) if part]

    if "*" in original_query:
        queries = query_combinations(query)
        result = simple_search(pts, td, queries)

    else:
        result = simple_search(pts, td, [query])
    return result


@celery.task
def get_stats():
    limit = max(STATS_LIMIT, td.size())
    nodes = td.traverse()

    json_response = {
        "top_frequencies": [
            [result[0], result[1]] for result in heapq.nlargest(limit, nodes, key=operator.itemgetter(1))
        ],
        "size": td.size(),
        "limit": limit

    }
    return json_response


@celery.task
def get_suggestions(original_query):
    query = [suggest_if_needed(td, part) for part in re.split('\s+', original_query) if part]
    queries = query_combinations(query)
    return [" ".join(query) for query in queries]


if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', debug=True)
    except KeyboardInterrupt:
        with open(STORAGE, 'wb') as pickle_file:
            pickle.dump(td, pickle_file)
