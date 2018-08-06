#!/usr/bin/python
import heapq
import json
import operator
import pickle
import re

from flask import Flask, Response, redirect, request

from celery import Celery
from moon.ngrams import query_combinations, suggest_if_needed
from moon.plugins import PluginsSeeker
from moon.queries.querying import simple_search
from moon.structs.categorizer import NamedIndexes
from moon.tokens import ExtendedPorterStemmer

STORAGE = "storage/tokentree.pickle"

app = Flask(__name__)
# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

pts = ExtendedPorterStemmer()
PluginsSeeker.load_core_plugins('parsers')
PluginsSeeker.load_core_plugins('query')

STATS_LIMIT = 100
"""
parser = argparse.ArgumentParser(description="Rend a spatial data database/application")
parser.add_argument("-nl", "--no-loading", action="store_true", default=False)
args = parser.parse_args()
td = None

if not args.no_loading:
"""
try:
    with open(STORAGE, 'rb') as pickle_file:
        print("[*] Loading pickle file")
        td = pickle.load(pickle_file)
except IOError:
    td = NamedIndexes()

############################################
#               FLASK ROUTES               #
############################################


@app.route("/search", methods=['GET'])
def text_search():
    original_query = request.args.get('query')
    index_name = request.args.get('name')
    print(index_name)
    if not original_query:
        return "form boi"
    result = get_results.delay(index_name, original_query).wait()
    return Response(json.dumps(result), status=200, mimetype='application/json')


@app.route("/stats", methods=['GET'])
def scarlet_stats():
    index_name = request.args.get('name')
    result = get_stats.delay(index_name).get()
    return Response(json.dumps(result), status=200, mimetype='application/json')


@app.route("/index", methods=['POST'])
def index_data():
    print(request.data)
    match = request.get_json().get('filename')
    url = request.get_json().get('origin_url')
    index_name = request.get_json().get('name')

    add_to_index.delay(index_name, match, url)
    return Response(json.dumps({"status": 200}))


@app.route("/suggest", methods=['GET'])
def suggest_corrections():
    index_name = request.args.get('name')
    original_query = request.args.get('query').lower()
    result = get_suggestions.delay(index_name, original_query).get()
    return Response(json.dumps(result), status=200, mimetype='application/json')


@app.route("/", methods=['GET'])
def redirect_to_search():
    return redirect("/search", code=302)

############################################
#               CELERY TASKS               #
############################################


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, overwrite_token_tree)


@celery.task
def overwrite_token_tree():
    print("############# Saving token tree #############")
    with open(STORAGE, 'wb') as pickle_file:
        pickle.dump(td, pickle_file)


@celery.task
def add_to_index(index, match, url):
    print("[*] Parsing: " + match)
    handler = PluginsSeeker.find_appropriate_parser(match)
    parsed_articles = handler.parse_document(match)
    print("[*] Adding:  " + match)
    for parsed_article in parsed_articles:
        td[index].update_tree(parsed_article, url)


@celery.task
def get_results(index, original_query):
    original_query = PluginsSeeker.process_query(original_query)
    print(original_query)
    query = [suggest_if_needed(td[index], part) for part in re.split('\s+', original_query.lower()) if part]

    if "*" in original_query:
        queries = query_combinations(query)
        result = simple_search(pts, td[index], queries)

    else:
        result = simple_search(pts, td[index], [query])
    return result


@celery.task
def get_stats(index):
    limit = max(STATS_LIMIT, td[index].size())
    nodes = td[index].traverse()
    json_response = {
        "top_frequencies": [
            [result[0], result[1]] for result in heapq.nlargest(limit, nodes, key=operator.itemgetter(1))
        ],
        "size": td[index].size(),  # TODO might be bugged
        "limit": limit

    }
    return json_response


@celery.task
def get_suggestions(index, original_query):
    query = [suggest_if_needed(td[index], part) for part in re.split('\s+', original_query) if part]
    queries = query_combinations(query)
    return [" ".join(query) for query in queries]


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
